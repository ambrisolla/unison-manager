import sys

def StatusMessages(**kwargs):
  message_size=60
  try:
    ''' set status message '''
    if 'status' not in kwargs:
      status = ''
    else:
      status = kwargs['status']
    ''' set message '''
    message = kwargs['message']
    ''' create a tring with spaces '''
    spaces = ''
    for s in range(0,message_size-len(message)):
      spaces = spaces + ' '
    if status != 'success' and status != 'warning' and status != 'fail':
      ''' if status var is != (success|warning|fail) print message without status '''
      print(f' - {message}...{spaces}\r', end='')
    else:
      ''' print message with status '''
      if status == 'success': 
        color = '\033[92m'
      elif status == 'warning':
        color = '\033[93m'
      elif status == 'fail':
        color = '\033[91m'
      reset_color = '\033[0m'
      status_message = f'{color}{status}{reset_color}'
      print(f' - {message}...{spaces} {status_message}')
  except Exception as err:
    print(str(err))
    sys.exit(1)
    
    
  
  
  