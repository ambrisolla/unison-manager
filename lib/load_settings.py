import os
import yaml
import sys

def loadSettings(fullpath):
  config_file = f'{fullpath}/conf/settings.yaml'
  if os.path.exists(config_file):
    yaml_data = open(config_file, 'r').read()
    data = yaml.safe_load(yaml_data)
    return data
  else:
    print(f'erro: {config_file} doesn\'t exists!')
    sys.exit(1)