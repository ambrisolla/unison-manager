import  os
import  re
import  sys
import  shutil
import  signal
from    lib.job_manage      import __jobInfo__
from    lib.status_messages import StatusMessages
from    lib.load_settings   import LoadSettings

def Remove(**kwargs):
  ''' check job name '''
  job_name = kwargs['job_name']
  if re.search(' ', job_name) or job_name == '':
    print('error: invalid Unison job name')
    sys.exit(1)
  ''' get job status'''  
  job_info = __jobInfo__(
    job_name=job_name)
  if job_info['job_status']:
    ''' kill process '''
    pid = int(job_info['pid'])
    __killProcess__(pid)
  __removeProfile__(kwargs)
    
def __killProcess__(pid):
  try:
    ''' stop process '''
    message = f'stopping Unison process'
    StatusMessages(message=message)
    os.kill(pid, signal.SIGKILL)
    StatusMessages(message=message, status='success')
  except Exception as err:
    StatusMessages(message=message, status='fail')
    print(f'error: {str(err)}')
    sys.exit(1)
    
def __removeProfile__(kwargs):  
  job_name = kwargs['job_name']
  message = f'removing Unison {job_name} profile'
  StatusMessages(message=message)
  try:
    settings = LoadSettings()
    unison_profile_directory = settings['unison_profile_directory']
    profile_path = f'{unison_profile_directory}/{job_name}'
    if os.path.exists(profile_path):
      shutil.rmtree(profile_path)
      StatusMessages(message=message, status='success')
    else:
      StatusMessages(message=message, status='fail')
      print(f'error: profile path {profile_path} does not exist!')
      sys.exit(1)
    StatusMessages(message=message, status='success')
  except Exception as err:
    StatusMessages(message=message, status='fail')
    print(f'error: {str(err)}')
    sys.exit(1)