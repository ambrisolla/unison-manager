import re
import os
import sys
import subprocess         as     sb
from   tabulate           import tabulate
from   lib.load_settings  import LoadSettings

def List():
  settings = LoadSettings()
  data = __getCreatedJobs__(unison_profile_directory=settings['unison_profile_directory'])
  __outputTable__(data)

def __getCreatedJobs__(unison_profile_directory):
  try:
    profile_dirs = [ b for a,b,c in os.walk(f'{unison_profile_directory}')][0]
    profile_data = []
    data = {}
    if len(profile_dirs) == 0:
      print('No Unison job found!')
      sys.exit(1)
    for job_name in profile_dirs:
      if not os.path.exists(f'{unison_profile_directory}/{job_name}/job.prf'):
        profile_data.append({
          'job_name' : job_name,
          'profile_status' : False,
          'local_directory' : '---',
          'remote_directory' : '---',
          'copy_status' : '---',
          'job_status' : '---'
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
          'profile_status' : True,
          'local_directory' : local_directory,
          'remote_directory' : remote_directory,
          'copy_status' : __getJobCopyStatus__(job_name,unison_profile_directory),
          'job_status' : __getJobStatus__(job_name)
          
        })
    return profile_data
  except Exception as err:
    print(f'error: {str(err)}')
    sys.exit(1)

def __getJobCopyStatus__(job_name,unison_profile_directory):
  try:
    log_file = f'{unison_profile_directory}/{job_name}/job.log'
    if os.path.exists(log_file):
      ''' set variables '''
      copy_status = 'no copies'
      percent = ''
      log_data = open(log_file, 'r').readlines()
      
      for idx, line in enumerate(reversed(log_data)):
        '''  check if is Copying : [BGN] flag'''
        if re.search('BGN', line):
          copy_status = 1
          break
        elif re.search('END', line):
          copy_status = 'copy finished!'
          break
        elif re.search('Fatal error', line):
          copy_status = line
          break
        elif re.search('Unison', line) and  re.search('log started at', line):
          copy_status = 'no copies'
          break
        ''' get copy percent if copy_status == 1 '''
      if copy_status == 1:
        copy_status = 'copying'
        lines_before_begin_flag = []
        for idx,line in enumerate(reversed(log_data)):          
          lines_before_begin_flag.append(line)
          if re.search('BGN', line):
            break
        if re.search('[0-9]%',lines_before_begin_flag[0]):
          percent = lines_before_begin_flag[0]
        else:
          percent = '0%'
      return f'{copy_status} {percent}' 
    else:
      return 'log file doesn\'t exists!'
  except Exception as err:
    print(f'error: {str(err)}')
    sys.exit(1)

def __getJobStatus__(job_name):
  try:
    cmd = ['ps', '-ef']
    ps = sb.run(cmd, stderr=sb.PIPE, stdout=sb.PIPE, text=True)
    if ps.returncode != 0:
      print(f'error: {str(ps.stderr)}')
      sys.exit(1)
    else:
      job_status='stopped'
      for line in ps.stdout.split('\n'):
        if re.search(f'/usr/bin/unison profiles/{job_name}/job.prf', line):
          job_status =  'running'          
      return job_status
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
    
