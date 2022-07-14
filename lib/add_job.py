import os
import re
import sys
import paramiko
from lib.status_messages import StatusMessages
from lib.load_settings import LoadSettings

def AddUnisonJob(**kwargs):
  # load settings
  settings = LoadSettings(fullpath=kwargs['fullpath'])
  # call functions
  __checkConnectionWithRemoteServer__(
    remote_server=kwargs['args']['remote_server'])
  __createLocalDirectory__(
    directory=kwargs['args']['directory'])
  __createRemoteDirectory__(
    directory=kwargs['args']['directory'],
    remote_server=kwargs['args']['remote_server'],
    fullpath=kwargs['fullpath'])
  __createUnisonProfile__(
    directory=kwargs['args']['directory'],
    remote_server=kwargs['args']['remote_server'],
    fullpath=kwargs['fullpath'],
    job_name=kwargs['args']['job_name'],
    unison_profile_directory=settings['unison_profile_directory'])
  __createScheduleAtCron__(
    job_name=kwargs['args']['job_name'],
    unison_contrab_path=settings['unison_contrab_path'],
    unison_crontab_default_schedule=settings['unison_crontab_default_schedule'])
  
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
    
def __createUnisonProfile__(directory,remote_server,fullpath,job_name,unison_profile_directory):
  message=f'creating Unison profile'
  try:
    if os.path.exists(f'{unison_profile_directory}/{job_name}'):
      StatusMessages(message=message,status='fail')  
      print(f'error: Unison profile directory {unison_profile_directory}/{job_name} already exists!')
      sys.exit(1)
    else:
      os.makedirs(f'{unison_profile_directory}/{job_name}')
    template_file = f'{fullpath}/conf/unison_profile.template'
    tf = open(template_file, 'r').read()
    profile = tf.\
      replace('__LOCAL_PATH__',f'{directory}').\
      replace('__REMOTE_SERVER__',f'{remote_server}').\
      replace('__LOG_FILE__',f'{unison_profile_directory}/{job_name}/job.log')
    pf = open(f'{unison_profile_directory}/{job_name}/job.prf', 'w')
    pf.write(profile)
    pf.close()
    StatusMessages(message=message,status='success')
  except Exception as err:
    StatusMessages(message=message,status='fail')
    print(f'error: {str(err)}')
    sys.exit(1)
    
def __createScheduleAtCron__(job_name,unison_contrab_path,unison_crontab_default_schedule):
  try:
    message=f'creating Unison job schedule at crontab'
    if os.path.exists(f'{unison_contrab_path}/unison_{job_name}'):
      StatusMessages(message=message,status='fail')    
      print(f'error: file {job_name} already exists!')
      sys.exit(1)
    else:
      cf = open(f'/etc/cron.d/unison_{job_name}', 'a')
      cf.write('# Added by unisonManager.py\n')
      cf.write(f'{unison_crontab_default_schedule} root /usr/bin/unisonManager --exec {job_name}\n')
      cf.close()
    StatusMessages(message=message,status='success')  
  except Exception as err:
    StatusMessages(message=message,status='fail')
    print(f'error: {str(err)}')
    sys.exit(1)