import os
import sys
import requests
import tarfile
from lib.status_messages import StatusMessages
from lib.load_settings   import LoadSettings

def InstallUnison(**kwargs):
  ''' load global settings '''
  settings = LoadSettings()
  __downloadFile__(install_source=settings['install_source'])
  __checkIfUnisonIsInstalled__(install_destiny=settings['install_destiny'])
  __extractFiles__(install_destiny=settings['install_destiny'])
  __setSymbolicLink__(install_destiny=settings['install_destiny'])
  __createProfileDir__(unison_profile_directory=settings['unison_profile_directory'])
    
def __downloadFile__(install_source):
  message='downloading Unison'
  StatusMessages(message=message)
  res = requests.get(install_source)
  if res.status_code == 200:
    temp_file = '/tmp/unison_temp_file.tar.gz'
    tf = open(temp_file, 'wb')
    tf.write(res.content)
    tf.close()
    StatusMessages(message=message, status='success')
  else:
    StatusMessages(message=message, status='fail')
    reason = res.reason
    print(f'erro: {reason}')
    sys.exit(1)

def __checkIfUnisonIsInstalled__(install_destiny):
  message = 'checking if Unison is installed'
  StatusMessages(message=message)
  try:
    if os.path.exists(install_destiny):
      StatusMessages(message=message, status='fail')
      print('error: Unison already installed!')
      sys.exit(1)
    else:
      StatusMessages(message=message, status='success')
  except Exception as err:
    StatusMessages(message=message, status='danger')
    print(f'erro: {str(err)}')
    sys.exit(1)

def __extractFiles__(install_destiny):
  message='extracting files'
  StatusMessages(message=message)
  try:
    temp_file = '/tmp/unison_temp_file.tar.gz'
    tar_file = tarfile.open(temp_file, 'r')
    tar_file.extractall(path=install_destiny)
    StatusMessages(message=message, status='success')
  except Exception as err:
    StatusMessages(message=message, status='fail')
    print(f'erro: {str(err)}')
    sys.exit(1)

def __setSymbolicLink__(install_destiny):
  message='creating symbolic links'
  StatusMessages(message=message)
  try:
    os.symlink(f'{install_destiny}/bin/unison', '/usr/local/bin/unison')
    StatusMessages(message=message,status='success')
  except Exception as err:
    StatusMessages(message=message,status='fail')
    print(f'erro: {str(err)}')
    sys.exit(1)
    
def __createProfileDir__(unison_profile_directory):
  message='creating profile directory'
  StatusMessages(message=message)
  try:
    os.makedirs(unison_profile_directory)
    StatusMessages(message=message,status='success')
  except Exception as err:
    StatusMessages(message=message,status='fail')
    print(f'erro: {str(err)}')
    sys.exit(1)