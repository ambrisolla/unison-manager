import  os
from    lib.load_settings import LoadSettings


def StartApp():
	try:
		settings      = LoadSettings()
		exporter_port = settings['exporter_port']
		fullpath      = settings['fullpath']
		''' set environments '''
		os.environ['FLASK_APP'] = f'{fullpath}/lib/exporter_app.py'
		os.system(f'flask run --host 0.0.0.0 --port {exporter_port} &')
	except Exception as err:
		print(f'error: {str(err)}')