# unisonManager
<b>unisonManager</b> is a Python script to be used to manage <a href='https://github.com/bcpierce00/unison' target='_blank'>Unison File Syncronizer</a> process.

# Unison
<a href='https://github.com/bcpierce00/unison' target='_blank'>Unison</a> is a file-syncronization tool. If you need a solution to keep your data up-to-date between two servers, <b>Unison</b> is a great choice.

# Prerequisites
To use <b>unisonManager</b> we need to solve some dependencies.
 - Python3.9+
 - PIP3.9+
 - PIP packages: paramiko, pyyaml, requests and tabulate

# Test environment
<b>unisonManager</b> has been tested on the Operating System below:
  - Ubuntu 22.04
  - Debian 11
  - Centos 7
  - Centos 8
  - Oracle Linux 7
  - Oracle Linux 8

# Install
The installation process is very simple. You just need to clone this repository and create a symbolic link.

Clone repo:
```shell
$ git clone https://github.com/brisa-dev/unison-manager.git /opt/unisonManager
```

Create a symbolic link:
```shell
$ ln -s /opt/unisonManager/unisonManager.py /usr/bin/unisonManager
```

# Options
### `--install-unison` :  This option will install <b>Unison</b>.