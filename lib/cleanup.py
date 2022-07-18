import re
import os
import sys
from lib.load_settings    import  LoadSettings
#from lib.status_messages  import  StatusMessages
from lib.job_manage       import  Start, Stop
def CleanUp(**kwargs):
  try:
    settings = LoadSettings()
    Stop(
      fullpath=settings['fullpath'],
      job_name=kwargs['job_name']
    )
    Start(
      fullpath=settings['fullpath'],
      job_name=kwargs['job_name']
    )
  except Exception as err:
    print(f'error: {str(err)}')