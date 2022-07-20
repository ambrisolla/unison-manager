import  os
import  sys
from    flask  import Flask

sys.path.append('.')
from    lib.load_settings import LoadSettings
from    lib.list import __getCreatedJobs__

app = Flask(__name__)

@app.route("/")
def show_data():
  try:
    settings                 = LoadSettings()
    unison_profile_directory = settings['unison_profile_directory']
    return {
      'data' : __getCreatedJobs__(unison_profile_directory)
    }, 200
  except Exception as err:
    return {
      'message' : str(err)
    }, 500