from secator.config import CONFIG
from secator.decorators import task
from secator.runners import Command
from secator.definitions import (OUTPUT_PATH, PATH, HEADER, URL, TIMEOUT,
                                 PROXY, USERNAME, USER_AGENT)

@task()
class goscrape(Command):
    cmd = 'goscrape'
    input_types = [URL]
    input_flag = ''
    version_flag = '--version'

    opts = {
        'n': {'type': str, 'help': 'only include URLs with PERL Regular Expressions support'},
        'x': {'type': str, 'help': 'exclude URLs with PERL Regular Expressions support'},
        'o': {'type': str, 'help': 'output directory to write files to'},
        'd': {'type': int, 'help': 'download depth, 0 for unlimited [default: 10]'},
        'i': {'type': int, 'help': 'image quality, 0 to disable reencoding'},
        's': {'type': str, 'help': 'serve the website using a webserver'},
        'r': {'type': int, 'help': 'port to use for the webserver [default: 8080]'},
        'c': {'type': int, 'help': 'file containing the cookie content (ex: [{"name":"user","value":"123"}])'},
        '-savecookiefile': {'type': str, 'help': 'file to save the cookie content'},
        'v': {'is_flag': True, 'default': False, 'help': 'verbose output'}
    }

    opt_key_map = {
        HEADER: 'h',
        TIMEOUT: 't',
        PROXY: 'p',
        USERNAME: 'u',
        USER_AGENT: 'a'
    }

    install_version = 'v0.3.0'
    install_cmd = 'go install -v github.com/cornelk/goscrape@[install_version]'
    install_github_handle = 'cornelk/goscrape'