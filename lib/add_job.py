import paramiko



def AddUnisonJob(**kwargs):
  __checkConnectionWithRemoteServer__(remote_server=kwargs['args']['remote_server'])
  
  
  
def __checkConnectionWithRemoteServer__(remote_server):
  try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_server, timeout=10)
    stdin, stdout, stderr = ssh.exec_command('uname -a')
    print(stdout.read().decode('utf-8'))
  except Exception as err:
    print(f'error: {str(err)}')

