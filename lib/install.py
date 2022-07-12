from distutils.command.config import config
import os
import sys
import yaml
import requests
import tarfile


def InstallUnison(**kwargs):
  confs = __loadConfig__(kwargs)
  __downloadFile__(install_source=confs['install_source'])
  __extractFiles__(install_destiny=confs['install_destiny'])
  __setSymbolicLink__(install_destiny=confs['install_destiny'])
  

def __loadConfig__(kwargs):
  fullpath = kwargs['fullpath']
  config_file = f'{fullpath}/conf/install.yaml'
  if os.path.exists(config_file):
    yaml_data = open(config_file, 'r').read()
    data = yaml.safe_load(yaml_data)
    return {
      'install_destiny' : data['install_destiny'],
      'install_source' : data['install_source']
    }
  else:
    print(f'erro: {config_file} doesn\'t exists!')
    sys.exit(1)
  
def __downloadFile__(install_source):
  res = requests.get(install_source)
  if res.status_code == 200:
    temp_file = '/tmp/unison_temp_file.tar.gz'
    tf = open(temp_file, 'wb')
    tf.write(res.content)
    tf.close()
  else:
    reason = res.reason
    print(f'erro: {reason}')
    sys.exit(1)

def __extractFiles__(install_destiny):
  try:
    temp_file = '/tmp/unison_temp_file.tar.gz'
    tar_file = tarfile.open(temp_file, 'r')
    tar_file.extractall(path=install_destiny)
  except Exception as err:
    print(f'erro: {str(err)}')
    sys.exit(1)

def __setSymbolicLink__(install_destiny):
  try:
    os.symlink(f'{install_destiny}/bin/unison', '/usr/bin/unison')
  except Exception as err:
    print(f'erro: {str(err)}')
    sys.exit(1)