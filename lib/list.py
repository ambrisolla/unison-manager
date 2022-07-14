import re
import os
import sys
from lib.load_settings  import LoadSettings
from tabulate import tabulate

def List(fullpath):
  settings = LoadSettings(fullpath=fullpath)
  __getCreatedJobs__(unison_profile_directory=settings['unison_profile_directory'])
  
  
def __getCreatedJobs__(unison_profile_directory):
  try:
    profile_dirs = [ b for a,b,c in os.walk(f'{unison_profile_directory}')][0]
    profile_data = []
    data = {}
    for job_name in profile_dirs:
      if not os.path.exists(f'{unison_profile_directory}/{job_name}/job.prf'):
        profile_data.append({
          'job_name' : job_name,
          'local_directory' : '---',
          'remote_directory' : '---',
          'status' : '---'
        })
      else:
        pf = open(f'{unison_profile_directory}/{job_name}/job.prf', 'r').read().split('\n')
        for line in pf:
          if re.search('^root', line) and not re.search('ssh', line): # root local
            local_directory = line.split('=')[-1].replace(' ','')
          elif re.search('^root', line) and re.search('ssh', line): # root local
            remote_directory = line.split('=')[-1].replace(' ','')
        profile_data.append({
          'job_name' : job_name,
          'local_directory' : local_directory,
          'remote_directory' : remote_directory,
          'status' : __getJobStatus__(job_name,unison_profile_directory)
        })
    __outputTable__(profile_data)
    ## PAROU AQUI. FALTA COLETAR INFORMACOES DOS LOGS DAS TRANSFERENCIAS PARA INCLUIR NA LISTA
  except Exception as err:
    print(f'error: {str(err)}')
    sys.exit(1)

def __getJobStatus__(job_name,unison_profile_directory):
  try:
    log_file = f'{unison_profile_directory}/{job_name}/job.log'
    if os.path.exists(log_file):
      log_data = open(log_file, 'r').readlines()
      for line in log_data:
        print(line)
    else:
      return 'log file doesn\'t exists!'
    return 'a'
  except Exception as err:
    print(f'error: {str(err)}')
    sys.exit(1)

def __outputTable__(data):
  try:
    output_list = []
    keys = [ x for x in data[0] ]
    output_list.append(keys)
    for i in data:
      item_list = []
      for key in keys:
        item_list.append(i[key])
      output_list.append(item_list)
    print(tabulate(output_list,headers="firstrow",tablefmt="psql"))

  except Exception as err:
    print(f'error: {str(err)}')
    sys.exit(1)