<h1 align="center">unisonManager</h1>
<div align="center">
  <b>unisonManager</b> is a Python script to be used to manage <a href='https://github.com/bcpierce00/unison' target='_blank'>Unison File Syncronizer</a> process.
</div>
<div align="center">
  <sub>Built by <a href="https://www.linkedin.com/in/brisolla/">Andre Muzel Brisolla</a>
</div>

# Contents
- [About Unison](#Unison)
- [Features](#Features)
- [Test environment](#Test-environment)
- [Prerequisites](#Prerequisites)
- [Install](#Install)
- [Options](#Options)

# Unison
<a href='https://github.com/bcpierce00/unison' target='_blank'>Unison</a> is a file-syncronization tool. If you need a solution to keep your data up-to-date between two servers, <b>Unison</b> is a great choice.

# Features
- Run an automated installation of Unison
- Manage Unison job profiles

# Test environment
<b>unisonManager</b> has been tested on the Operating System below:
  - Ubuntu 22.04
  - Debian 11
  - Centos 8
  - Oracle Linux 8

# Prerequisites
To use <b>unisonManager</b> we need to solve some dependencies.
 - Python 3
 - PIP 3
 - PIP packages: paramiko, pyyaml, requests and tabulate
 - SSH communication between servers without password

### Install Python/PIP 3
 Install Python 3 on Debian-based Linux:
 ```bash
  $ apt update && apt install python3 python3-pip -y
 ```
 Install Python 3 on RedHat-based Linux:
 ```bash
  $ yum install python39 python39-pip -y
 ```

### Install PIP packages

```bash
$ pip install paramiko pyyaml requests tabulate
```

### Configure SSH to communicate without password between servers.
The transfer process uses SSH for communication between servers. So we need to create an SSH key and copy it to remote server.<p>
Create SSH key:
```bash
$ ssh-keygen -t rsa # do not put password
```
Copy the SSH key to the remote server:
```bash
ssh-copy-id -i ~/.ssh/id_rsa root@[REMOTE_SERVER_ADDRESS]
```

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
### `--install-unison`
Install Unison.<p>
Example:
```bash
$ unisonManager --install-unison
```

### `--add-job`
Add a new Unison job. This option needs to be used with `--job-name`, `--remote-server`, and `--directory` options.<p>
Example:
```bash
$ unisonManager --add-job --job-name mysql_files --directory=/data/mysql_files \
  --remote-server [REMOTE_SERVER_ADDRESS]
```
By convention, use the same name to indentify <b>--job-name</b> and <b>--directory</b>.

When process has been finished, all sctructure necessary to syncronize the data will be created in local and remote server.

### `--job-name [JOB_NAME]` (to be used with --add-job)
Specify a job name when creating a new Unison job.

### `--directory [DIRECTORY]` (to be used with --add-job)
Specify a directory when creating a new Unison job.

### `--remote-server [REMOTE_SERVER]` (to be used with --add-job)
Specify a remote server when creating a new Unison job.

### `--list`
List status of created jobs.<p>
Example:
```bash
$ unisonManager --list
```

### `--start [JOB_NAME]`
Start a Unison job.<p>
Example:
```bash
$ unisonManager --start [JOB_NAME]
```

### `--stop [JOB_NAME]`
Stop a Unison job.<p>
Example:
```bash
$ unisonManager --stop [JOB_NAME]
```

### `--remove`
Remove a Unison job. PS: This action only removes the Unison profile, it does not remove any data where the data is synced.<p>
Example:
```bash
$ unisonManager --remove [JOB_NAME]
```

### `--cleanup  [JOB_NAME]`
This action stops the job process, removes all .unison.tmp and starts job process.<p>
Example:
```bash
$ unisonManager --cleanup [JOB_NAME]
```

### `--cleanup-all`
This action executes the same of '--cleanup' option, but in all jobs.<p>
Example:
```bash
$ unisonManager --cleanup-all
```
