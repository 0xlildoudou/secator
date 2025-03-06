import click
import yaml

from secator.decorators import task
from secator.runners import Command
from secator.tasks._categories import VulnHttp
from secator.output_types import Tag, Vulnerability, Info
from secator.definitions import (
    OUTPUT_PATH,
    CONFIDENCE,
    CVSS_SCORE,
    DESCRIPTION,
    EXTRA_DATA,
    MATCHED_AT,
    NAME,
    REFERENCES,
    SEVERITY,
    TAGS,
    URL,
    PROVIDER,
)


@task()
class wpprobe(VulnHttp):
    """Fast WordPress plugin enumeration tool written in Go."""

    cmd = "wpprobe"

    file_flag = "-f"
    input_flag = "-u"
    input_type = URL
    opt_prefix = "--"

    opts = {
        "mode": {
            "type": click.Choice(["scan", "update", "update-db"]),
            "default": "scan",
            "help": "WPProbe mode",
        },
        "f": {"type": str, "help": "Targets list path"},
    }

    output_types = [Vulnerability, Tag]

    install_cmd = "go install github.com/Chocapikk/wpprobe@latest"
    install_github_handle = "Chocapikk/wpprobe"
    profile = "io"

    output_map = {
        Vulnerability: {
            NAME: lambda x: f"{x.get('name', '')} {x.get('version', '')}",
            DESCRIPTION: lambda x: "\n".join(
                [v.get("title", "") for v in x.get("vulnerabilities", [])]
            ),
            SEVERITY: lambda x: x.get("severity", "info"),
            CONFIDENCE: lambda x: "high" if x.get("version") else "low",
            CVSS_SCORE: lambda x: [v.get("cvss_score") for v in x.get("vulnerabilities", [])],
            MATCHED_AT: lambda x: str(x.get("url", "")),
            TAGS: lambda x: [v.get("cve") for v in x.get("vulnerabilities", [])],
            REFERENCES: lambda x: [v.get("cve_link") for v in x.get("vulnerabilities", [])],
            EXTRA_DATA: lambda x: {
                "auth_type": x.get("auth_type"),
                "cvss_vector": [v.get("cvss_vector") for v in x.get("vulnerabilities", [])],
            },
            PROVIDER: "wpprobe",
        },
    }

    @staticmethod
    def on_init(self):
        self.output_path = (
            self.get_opt_value(OUTPUT_PATH)
            or f"{self.reports_folder}/.outputs/{self.unique_name}.json"
        )
        self.cmd += f" -o {self.output_path}"
        
    @staticmethod
    def on_start(self):
        mode = self.get_opt_value("mode")
        cmd_parts = self.cmd.split()
        cmd_parts = [part for part in cmd_parts if part not in ["scan", "update", "update-db", "--mode"]]
        cmd_parts.insert(1, mode)
        self.cmd = " ".join(cmd_parts)

    @staticmethod
    def on_cmd_done(self):
        if not self.output_path:
            yield Info(message="No output path set. Skipping result parsing.")
            return

        yield Info(message=f"JSON results saved to {self.output_path}")

        with open(self.output_path, "r") as f:
            results = yaml.safe_load(f)

        target = str(results.get("url", ""))

        for name, plugins in results.get("plugins", {}).items():
            for plug in plugins:
                version = plug.get("version", "")
                yield Tag(
                    name=f"{name} {version}",
                    match=target,
                )

                for severity, details in plug.get("severities", {}).items():
                    for vuln in details:
                        for v in vuln.get("vulnerabilities", []):
                            confidence = "high" if version else "low"
                            yield Vulnerability(
                                matched_at=target,
                                name=f"Wordpress plugin - {name} {version} outdated",
                                severity=severity,
                                confidence=confidence,
                                references=[v.get("cve_link")],
                                tags=[v.get("cve")],
                                extra_data={"Auth type": vuln.get("auth_type", "N/A")},
                                provider="wpprobe",
                            )
