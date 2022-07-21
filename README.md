![This is an image](https://www.influxdata.com/wp-content/uploads/IPtables-logo.jpg)
# VPS protection

Vps protection is a simple module to automate server protection easily with python.


## Download
Use git to download.

```bash
git clone https://github.com/mohtadi-adouani/protection_vps_using_iptables
```


## Installation

Use shell to install.

```bash
python3 setup.py
```


## Usage

```python
import vps_protection as vpsp

# Allow SSH connections on tcp port 22
vpsp.ssh(22)
    
# Set default policies for INPUT, FORWARD and OUTPUT chains
vpsp.set_default_policies():

    # Set access for localhost
vpsp.set_access_localhost()

# ACCEPT packets belonging to established and related connections
vpsp.set_established_and_related():

# Allwo FTP on port 21
vpsp.ftp(21)

# allow http and https on port 80 and 443
vpsp.http(80,443)

# Allow SSH connections on tcp port 2222
vpsp.ssh(2222)

```

## Reference
Using [iptables tutorial ](https://portal-clienti.dedicatserver.ro/knowledgebase/1/SetariorSettings-firewall---iptable.html)


