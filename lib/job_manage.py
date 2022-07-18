import re
import os
import sys
import signal
import subprocess         as      sb
from lib.load_settings    import  LoadSettings
from lib.status_messages  import  StatusMessages

def Start(**kwargs):
  try:
    job_name = kwargs['job_name']
    job_info = __jobInfo__(fullpath=kwargs['fullpath'],job_name=job_name)
    running = job_info['job_status']
    message = f'starting Unison job [{job_name}]'
    if not running:    
      StatusMessages(message=message)
      try:
        os.system(f'/usr/bin/unison profiles/{job_name}/job.prf > /dev/null 2> /dev/null &')
        StatusMessages(message=message, status='success')
      except Exception as err:
        StatusMessages(message=message, status='fail')
        print(f'error: {str(err)}')
        sys.exit(1)
    else:
      StatusMessages(message=message, status='warning')
      print(f'info: Job {job_name} is already running!')
      sys.exit(0)
  except Exception as err:
    StatusMessages(message=message, status='fail')
    print(f'erro: {str(err)}')
    sys.exit(1)
    
def Stop(**kwargs):
  try:
    job_name = kwargs['job_name']
    job_info = __jobInfo__(fullpath=kwargs['fullpath'],job_name=job_name)
    running = job_info['job_status']
    message = f'stopping Unison job [{job_name}]'
    if running:
      pid = int(job_info['pid'])
      os.kill(pid, signal.SIGKILL)
      StatusMessages(message=message, status='success')  
    else:
      StatusMessages(message=message, status='warning')
      print('info: Job is not running!')
      sys.exit(0)
  except Exception as err:
    StatusMessages(message=message, status='fail')
    print(f'erro: {str(err)}')
    sys.exit(1)

def __jobInfo__(**kwargs):
  try:
    ''' load global settings '''
    settings = LoadSettings()
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
        ps = ['ps', '-ef']
        list_process = sb.run(ps, stdout=sb.PIPE, stderr=sb.PIPE, text=True)
        if list_process.returncode != 0:
          print(f'error: error executing command')
          print(f'{str(list_process.stderr)}')
          sys.exit(1)
        else:
          '''return data ''' 
          full_process_name = f'/usr/bin/unison profiles/{job_name}/job.prf'
          is_running = True in [ bool(re.search(full_process_name,x)) \
            for x in list_process.stdout.split('\n') ]
          if is_running:
            ''' is running, get PID '''
            pgrep = ['pgrep', '-f', full_process_name]
            ps = sb.run(pgrep, stderr=sb.PIPE, stdout=sb.PIPE, text=True)
            if ps.returncode != 0:
              print(f'error: {str(ps.stderr)}')
              sys.exit(1)
            else:
              pid = ps.stdout.replace('\n','')
              return {
                'job_status' : True,
                'pid' : pid
              }
          else:
              return {
                'job_status' : False
              }
  except Exception as err:
    print(f'erro: {str(err)}')
    sys.exit(1)
          
          