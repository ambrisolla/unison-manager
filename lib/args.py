import re
import sys
import argparse

def arg_parser():
  parser = argparse.ArgumentParser(allow_abbrev=False)
  ''' create arguments '''
  parser.add_argument('--install',       help='Install Unison',                          action='store_true')
  parser.add_argument('--add-job',       help='Add a new Unison job',                    action='store_true')
  parser.add_argument('--name',          help='Job name (used with --add-job)',          dest="job_name")
  parser.add_argument('--remote-server', help='Remote server (used with --add-job)',     dest="remote_server")
  parser.add_argument('--directory',     help='Directory to sync (used with --add-job)', dest='directory')
  parser.add_argument('--list',          help='List Unison jobs',                        action='store_true')
  parser.add_argument('--exec',          help='Execute a Unison job',                    dest='exec_job')
  parser.add_argument('--remove',        help='Remove Unison job',                       dest='remove_job')
  args = vars(parser.parse_args())
  
  ''' set arguments dependency '''
  add_jobs_dependency = [
    'job_name',
    'directory',
    'remote_server' ]
  ''' check if arguments to be used with --add-job was passed ''' 
  if args['add_job']:
    for arg in add_jobs_dependency:
      if args[arg] == None:
        print(f'error: Parameter [{arg}] not found!')
        sys.exit(1)
    ''' check if some argument is empty  '''
    empty_value = '' in [ args[x] for x in add_jobs_dependency ]
    if empty_value:
      print('error: Empty values is not allowed!')
      sys.exit(1)
    values_with_space = True in [ bool(re.search(' ',args[x])) for x in add_jobs_dependency ]
    if values_with_space:
      print('error: Values with spaces is not allowed!')
    ''' values was validated! '''
    print('add job')
  else:
    if args['job_name'] != None or args['directory'] != None or args['remote_server'] != None:
      ''' check if arguments to be used with --add-job was passed ''' 
      print('error: You passed an argument to use with "--add-job" argument!\n')
      parser.print_help()
      sys.exit(1)
    true_arguments = [ x for x in args if args[x] ]
    if len(true_arguments) > 1:
      print('Error: You need to pass only one argument!')
      sys.exit(1)
    else:
      ''' install Unison on server '''
      if args['install']:
        print('install unison')
    
  
  