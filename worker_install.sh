#!/bin/sh

### tools version
NUCLEI_VERSION="3.3.4"
HTTPX_VERSION="1.6.8"
DALFOX_VERSION="2.9.3"
GOSPIDER_VERSION="1.1.6"
MAPCIDR_VERSION="1.1.34"
NAABU_VERSION="2.3.1"


### install tools

# nuclei
wget https://github.com/projectdiscovery/nuclei/releases/download/v${NUCLEI_VERSION}/nuclei_${NUCLEI_VERSION}_linux_amd64.zip -O nuclei.zip
unzip -p nuclei.zip nuclei > ~/.local/bin/nuclei && chmod 755 ~/.local/bin/nuclei

# httpx
wget https://github.com/projectdiscovery/httpx/releases/download/v${HTTPX_VERSION}/httpx_${HTTPX_VERSION}_linux_amd64.zip -O httpx.zip
unzip -p httpx.zip httpx > ~/.local/bin/httpx && chmod 755 ~/.local/bin/httpx

# dalfox
wget https://github.com/hahwul/dalfox/releases/download/v${DALFOX_VERSION}/dalfox_${DALFOX_VERSION}_linux_amd64.tar.gz -O dalfox.tar.gz
tar -xf dalfox.tar.gz -C ~/.local/bin/ dalfox && chmod 755 ~/.local/bin/dalfox

# gospider
wget https://github.com/jaeles-project/gospider/releases/download/v${GOSPIDER_VERSION}/gospider_v${GOSPIDER_VERSION}_linux_x86_64.zip -O gospider.zip
unzip -p gospider.zip gospider_v${GOSPIDER_VERSION}_linux_x86_64/gospider > ~/.local/bin/gospider && chmod 755 ~/.local/bin/gospider

# mapcidr       # path bug
# wget https://github.com/projectdiscovery/mapcidr/releases/download/v${MAPCIDR_VERSION}/mapcidr_${MAPCIDR_VERSION}_linux_amd64.zip -O mapcidr.zip
# unzip -p mapcidr.zip mapcidr > ~/.local/bin/mapcidr && chmod 755 ~/.local/bin/mapcidr

# naabu
# wget https://github.com/projectdiscovery/naabu/releases/download/v${NAABU_VERSION}/naabu_${NAABU_VERSION}_linux_amd64.zip -O naabu.zip
# unzip -p naabu.zip naabu > /usr/bin/naabu && chmod 755 /usr/bin/naabu