import re
import os
import sys
from lib.load_settings  import LoadSettings

def List(fullpath):
  settings = LoadSettings(fullpath=fullpath)
  __getCreatedJobs__(unison_profile_directory=settings['unison_profile_directory'])
  
  
def __getCreatedJobs__(unison_profile_directory):
  try:
    profile_dirs = [ b for a,b,c in os.walk(f'{unison_profile_directory}')][0]
    profile_data = []
    for dir in profile_dirs:
      if not os.path.exists(f'{unison_profile_directory}/{dir}/job.prf'):
        profile_data.append({
          'job_name' : dir
        })
      else:
        pf = open(f'{unison_profile_directory}/{dir}/job.prf', 'r').read().split('\n')
        for line in pf:
          if re.search('^root', line) and not re.search('ssh', line): # root local
            local_directory = line.split('=')[-1].replace(' ','')
          elif re.search('^root', line) and re.search('ssh', line): # root local
            remote_directory = line.split('=')[-1].replace(' ','')
        profile_data.append({
          'job_name' : dir,
          'local_directory' : local_directory,
          'remote_directory' : remote_directory
        })
    print(profile_data)
    ## PAROU AQUI. FALTA COLETAR INFORMACOES DOS LOGS DAS TRANSFERENCIAS PARA INCLUIR NA LISTA
  except Exception as err:
    print(f'error: {str(err)}')
    sys.exit(1)