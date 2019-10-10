from flask import Flask, request
import paramiko


config = { 'hostname' : '37.140.192.54',
					'username' : 'u0829504',
					'password' : 'WcXUE!v9',
					'port' : 22}

app = Flask(__name__)


def ssh_request(cmd: str) -> str:
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(**config)
	stdin, stdout, stderr = client.exec_command(cmd)
	data = str((stdout.read() + stderr.read()).decode('utf-8'))
	client.close()
	return(data)


@app.route('/checks')
def checks():
	cmd = request.args.get('cmd')
	checks_output = {}
	host_avg_load = ssh_request('uptime').split('load average: ')[-1]
	host_avg_load = host_avg_load.split('\n')[0]
	checks_output["host_avg_load"] = host_avg_load
	checks_output["root_free_space"] = ssh_request('df -h').split('\n')[:-1]
	python_processes = ssh_request('ps ax | grep pyth').split('\n')[:-1]
	checks_output["python_processes"] = python_processes
	if cmd:
		cmd_output = {}
		cmd_output['cmd'] = ssh_request(cmd).split('\n')[:-1]
		return(cmd_output)
	return(checks_output)


if __name__=='__main__':
	app.run(debug=True)