import re
import os
import sys
import subprocess         as      sb
from lib.load_settings    import  LoadSettings
from lib.status_messages  import StatusMessages

def Execute(**kwargs):
  ''' load global settings '''
  settings = LoadSettings(fullpath=kwargs['fullpath'])
  job_name = kwargs['job_name']
  ''' print message '''
  message = f'starting Unison job {job_name}'
  StatusMessages(message=message)
  ''' check if job_name has one or more " " character'''
  if re.search(' ', job_name) or job_name == '':
    StatusMessages(message=message, status='fail')
    print('erro: Invalid job name!')
    sys.exit(1)
  else:
    ''' job_name validated, checking if profile exists '''
    profile_full_path = settings['unison_profile_directory']
    if not os.path.exists(f'{profile_full_path}/{job_name}/job.prf'):
      StatusMessages(message=message, status='fail')
      print('error: Profile file doesn\'t exists!')
      sys.exit(1)
    else:
      ''' profile file exists '''
      ps = ['ps', '-ef']
      list_process = sb.run(ps, stdout=sb.PIPE, stderr=sb.PIPE, text=True)
      if list_process.returncode != 0:
        StatusMessages(message=message, status='fail')
        print(f'error: error executing command')
        print(f'{str(list_process.stderr)}')
        sys.exit(1)
      else:
        is_running = True in [ bool(re.search(f'/usr/bin/unison profiles/{job_name}/job.prf',x)) \
          for x in list_process.stdout.split('\n') ]
        if is_running:
          StatusMessages(message=message, status='fail')
          print(f'error: Job {job_name} already is running!')          
        else:          
          os.system(f'/usr/bin/unison profiles/{job_name}/job.prf > /dev/null 2> /dev/null &')
          StatusMessages(message=message, status='success')