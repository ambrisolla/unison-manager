import re
import os
import sys
import subprocess as sb
from lib.load_settings import loadSettings

def Execute(**kwargs):
  ''' load global settings '''
  settings = loadSettings(fullpath=kwargs['fullpath'])
  job_name = kwargs['job_name']
  ''' check if job_name has one or more " " character'''
  if re.search(' ', job_name) or job_name == '':
    print('erro: Invalid job name!')
    sys.exit(1)
  else:
    ''' job_name validated, checking if profile exists '''
    profile_full_path = settings['unison_profile_directory']
    if not os.path.exists(f'{profile_full_path}/{job_name}/job.prf'):
      print('error: Profile file doesn\'t exists!')
      sys.exit(1)
    else:
      ''' profile file exists '''
      print(f'/usr/bin/unison profiles/{job_name}/job.prf')
      os.system(f'/usr/bin/unison profiles/{job_name}/job.prf')
      print(f'info: job {job_name} started!')
    
