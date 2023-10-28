import sys
import subprocess
from subprocess import Popen, PIPE
import shlex
import json
found = None
session = subprocess.Popen(shlex.split('/home/ubuntu/.nvm/versions/node/v8.9.4/bin/pm2 jlist'), stdout=PIPE, stderr=PIPE)
stdout, stderr = session.communicate()
if len(sys.argv) > 1:
	process = sys.argv[1]
else:
	process = 'not defined'
	print "Usage: ./monitor.py <process_name> <metric_name/all>[optional]"
	print "If not 'metric_name' or 'all' is not passed, process status will be returned"
	found = 2
if len(sys.argv) > 2:
	metric = sys.argv[2]
else:
	metric = None
if stderr:
	raise Exception("Error "+str(stderr))
json_data = json.loads(stdout)

for x in json_data:
	if process in x['name']:
		#print x['name']
		found = 1
		if metric:
			if metric == "all":
				for key, value in x['pm2_env']['axm_monitor'].iteritems():
					print key, ":", value['value']
			else:
				try: print x['pm2_env']['axm_monitor'][metric]['value']
				except: 
					print "\nSpecified metric does not exist for this process. Metric names are CASE SENSITIVE."
					print "Valid axm_monitor metrics for this process are:"
					for key, value in x['pm2_env']['axm_monitor'].iteritems():
						print key
		else:
			print x['pm2_env']['status']
if not found:
	print "Specified process '"+ process+ "' was not found."
