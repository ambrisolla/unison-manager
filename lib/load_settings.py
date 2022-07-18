import os
import yaml
import sys

def LoadSettings():
  fullpath = os.path.realpath(os.path.dirname(__file__))
  config_file = f'{fullpath}/../conf/settings.yaml'
  if os.path.exists(config_file):
    yaml_data = open(config_file, 'r').read()
    data = yaml.safe_load(yaml_data)
    data['fullpath'] = fullpath
    return data
  else:
    print(f'erro: {config_file} doesn\'t exists!')
    sys.exit(1)