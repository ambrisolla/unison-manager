import re
import sys
import argparse
from lib.install        import InstallUnison
from lib.add_job        import AddUnisonJob
from lib.job_manage     import Start, Stop
from lib.load_settings  import LoadSettings
from lib.list           import List
from lib.remove         import Remove
from lib.cleanup        import CleanUp, CleanUpAll
from lib.exporter       import StartApp

def arg_parser():
  # load global settings
  settings = LoadSettings()
  parser = argparse.ArgumentParser(allow_abbrev=False)
  ''' create arguments '''
  parser.add_argument('--install-unison', help='Install Unison',                                action='store_true'  )
  parser.add_argument('--add-job',        help='Add a new Unison job',                          action='store_true'  )
  parser.add_argument('--job-name',       help='Job name (used with --add-job)',                dest="job_name"      )
  parser.add_argument('--remote-server',  help='Remote server (used with --add-job)',           dest="remote_server" )
  parser.add_argument('--directory',      help='Directory to sync (used with --add-job)',       dest='directory'     )
  parser.add_argument('--list',           help='List Unison jobs',                              action='store_true'  )
  parser.add_argument('--start',          help='Start a Unison job',                            dest='start_job'     )
  parser.add_argument('--stop',           help='Stop a Unison job',                             dest='stop_job'      )
  parser.add_argument('--remove',         help='Remove Unison job',                             dest='remove_job'    )
  parser.add_argument('--cleanup',        help='Cleanup temporary files from a specific job',   dest='cleanup_job'   )
  parser.add_argument('--cleanup-all',    help='Cleanup temporary files from all jobs',         action='store_true'  )
  parser.add_argument('--exporter',       help='Export process status'                ,         action='store_true'  )
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
    ''' values was validated! Add Unison job'''
    AddUnisonJob(args=args)
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
      if args['install_unison']:
        ''' Install Unison '''
        InstallUnison()
      elif args['start_job']:
        ''' Start a Unison job '''
        Start(
          job_name=args['start_job'])
      elif args['stop_job']:
        ''' Stop a Unison job '''
        Stop(
          job_name=args['stop_job'])
      elif args['list']:
        List()
      elif args['remove_job']:
        Remove(job_name=args['remove_job'])
      elif args['cleanup_job']:
        CleanUp(job_name=args['cleanup_job'])
      elif args['cleanup_all']:
        CleanUpAll(job_name=args['cleanup_job'])
      elif args['exporter']:
        StartApp()
        