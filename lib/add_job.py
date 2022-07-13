import os
import sys
import paramiko
from lib.status_messages import StatusMessages


def AddUnisonJob(**kwargs):
  __checkConnectionWithRemoteServer__(remote_server=kwargs['args']['remote_server'])
  __createLocalDirectory__(directory=kwargs['args']['directory'])
  __createRemoteDirectory__(directory=kwargs['args']['directory'],remote_server=kwargs['args']['remote_server'],
    fullpath=kwargs['fullpath'])
  
def __checkConnectionWithRemoteServer__(remote_server):
  try:
    status_message=f'checking communication with {remote_server}'
    StatusMessages(message=status_message)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_server, timeout=10)
    stdin, stdout, stderr = ssh.exec_command('uname')
    stdout.read()
    StatusMessages(message=status_message, status='success')
  except Exception as err:
    StatusMessages(message=status_message, status='fail')
    print(f'error: {str(err)}')
    sys.exit(1)
    
def __createLocalDirectory__(directory):
  try:
    message=f'creating directory {directory}'
    StatusMessages(message=message)
    if os.path.exists(directory):
      StatusMessages(message=f'directory {directory} already exists',status='warning')
    else:
      os.makedirs(directory)
      StatusMessages(message=message,status='success')
  except Exception as err:
    StatusMessages(message=message,status='fail')
    print(f'error: {str(err)}')
    sys.exit(1)

def __createRemoteDirectory__(directory,remote_server,fullpath):
  message=f'creating directory {directory} in {remote_server}'
  try:
    StatusMessages(message=message)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_server, timeout=10)
    # transfer auxiliar script
    temporary_script = '/tmp/unison_auxiliar_script.sh'
    scp = ssh.open_sftp()
    scp.put(f'{fullpath}/conf/unison_auxiliar_script.sh', temporary_script)
    scp.close()
    stdin, stdout, stderr = ssh.exec_command(f'bash {temporary_script} --create-directory {directory}')
    retcode = stdout.channel.recv_exit_status()
    if retcode == 0:
      StatusMessages(message=message, status='success')  
    elif retcode == 1:
      StatusMessages(message=message, status='fail')  
      print(stderr)
      sys.exit(1)
    elif retcode == 2:
      StatusMessages(message=f'directory {directory} already exists in {remote_server}',status='warning')
  except Exception as err:
    StatusMessages(message=message,status='fail')
    print(f'error: {str(err)}')
    sys.exit(1)