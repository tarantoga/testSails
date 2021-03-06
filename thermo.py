import sys
import serial
import urllib
import urllib2
from urllib2 import URLError
from daemon import runner

class App():
	
	def __init__(self):
		self.stdin_path = '/dev/null'
		self.stdout_path = '/tmp/thermo.log'
		self.stderr_path = '/tmp/thermo.log'
		self.pidfile_path = '/tmp/thermo.pid'
		self.pidfile_timeout = 5
		
	def run(self):
		urlSample = 'http://localhost:1337/sample/create'
		urlDevice = 'http://localhost:1337/device/set'
		urlData = 'http://localhost:1337/data/create'
		ser = serial.Serial('/dev/ttyAMA0', 9600)
		while True:	
			data = ser.read(12)
			try:
				params = urllib.urlencode({
								  'message': data
								  })
				urllib2.urlopen(urlData, params).read()
				sensor = data[1:3]
				command = data[3:]
				if command.startswith('TMPA'):
					stmp = data[-5:]
					ftmp = float(stmp)
					params = urllib.urlencode({
								  'device': sensor,
								  'value': ftmp,
								  })
					urllib2.urlopen(urlSample, params).read()
				elif command.startswith('BATT'):
					sbatt = data[-5:-1]
					fbatt = float(sbatt)
					params = urllib.urlencode({
								'name': sensor,
								'batt': fbatt,
								})
					urllib2.urlopen(urlDevice, params).read()
			except URLError as e:
			    if hasattr(e, 'reason'):
			        print('Failed to reach a server.')
			        print('Reason: ', e.reason)
			    elif hasattr(e, 'code'):
			        print('The server couldn\'t fulfill the request.')
			        print('Error code: ', e.code)
					
app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()

