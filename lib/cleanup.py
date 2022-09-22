import re
import os
import glob
import sys
import shutil
import paramiko
from lib.load_settings    import LoadSettings
from lib.status_messages  import StatusMessages
from lib.job_manage       import Start, Stop
from lib.list             import __getCreatedJobs__

def CleanUpAll(**kwargs):
  try:
    settings = LoadSettings()
    profile_data = __getCreatedJobs__(unison_profile_directory=settings['unison_profile_directory'])
    for data in profile_data:
      if data['profile_status']:
        job_name = data['job_name']
        CleanUp(job_name=job_name)
  except Exception as err:
    print(f'error: {str(err)}')
    sys.exit(1)

def CleanUp(**kwargs):
  try:
    job_name = kwargs['job_name']
    settings = LoadSettings()
    fullpath=settings['fullpath']
    unison_profile_directory = settings['unison_profile_directory']
    ''' stop job '''
    Stop(
      fullpath=fullpath,
      job_name=job_name
    )
    ''' load profile file '''
    profile_file = open(f'{unison_profile_directory}/{job_name}/job.prf', 'r').readlines()
    local_path = profile_file[0].replace('\n','').split('=')[1].replace(' ','')
    remote_path = profile_file[1].replace('\n','').split('=')[1].replace(' ','')
    ''' remove local tmp.unison files '''
    __findAndRemoveLocalTmpFiles(local_path)
    __findAndRemoveRemoteTmpFiles(remote_path)
    Start(
      fullpath=fullpath,
      job_name=job_name
    )
  except Exception as err:
    print(f'error: {str(err)}')
    sys.exit(1)
    
def __findAndRemoveLocalTmpFiles(directory):
  message = 'removing local unison.tmp files'
  StatusMessages(message=message)
  try:
    tmp_files = glob.glob(f'{directory}/**/.*.unison.tmp', recursive=True)
    for file in tmp_files:
      if os.path.isfile(file):
        os.remove(file)
      elif os.path.isdir(file):
        shutil.rmtree(file)
    StatusMessages(message=message, status='success')
  except Exception as err:
    StatusMessages(message=message, status='fail')
    print(f'error: {str(err)}')
    ##sys.exit(1)
    
def __findAndRemoveRemoteTmpFiles(remote):
  message = 'removing remote unison.tmp files'
  settings = LoadSettings()
  fullpath=settings['fullpath']
  StatusMessages(message=message)
  try:
    remote_server    = remote.split('//')[1]
    remote_directory = '/{}'.format(remote.split('//')[2])
    ''' SSH config ''' 
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_server, timeout=10)
        # transfer auxiliar script
    temporary_script = '/tmp/unison_auxiliar_script.sh'
    scp = ssh.open_sftp()
    scp.put(f'{fullpath}/conf/unison_auxiliar_script.sh', temporary_script)
    scp.close()
    stdin, stdout, stderr = ssh.exec_command(f'bash {temporary_script} --remove-temp-files {remote_directory}')
    retcode = stdout.channel.recv_exit_status()
    if retcode == 0:
      StatusMessages(message=message, status='success')
    elif retcode == 2:
      StatusMessages(message=message, status='fail')
      print(f'error: Directory {remote_directory} does not exists!')
      ## sys.exit(1)
    elif retcode == 1:
      StatusMessages(message=message, status='fail')
      print(f'error: {stderr}')
      ## sys.exit(1)
  except Exception as err:
    StatusMessages(message=message, status='fail')
    print(f'error: {str(err)}')
    ##sys.exit(1)
  