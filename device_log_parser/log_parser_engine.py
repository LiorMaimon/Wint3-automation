
from time import sleep
import sys
# from Demos.win32console_demo import stdin, stdout,
from fabric import Connection, Config
import paramiko
from paramiko import SSHClient, AutoAddPolicy


# SSH tunnel parameters
local_port = 31315
host = '192.168.1.14'
# host = 'proxy8.remoteiot.com'
user_name = 'w3d'

client = SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
key = paramiko.ECDSAKey.from_private_key_file('./lior_ecdsa')
client.connect(hostname=host, port=local_port, username='w3d', pkey=key)


# Optionally, send data via STDIN, and shutdown when done
docker_cmd = 'cd /home/w3d/wint3-os; docker compose logs -f --tail 10 cloud'
docker_cmd = 'cd /home/w3d/wint3-os; dcl modbus'
docker_cmd = 'source /home/w3d/.profile; docker compose logs -f --tail 10 algo | grep ERROR'

#docker_cmd = 'export | grep COMPOSE'

xstdin, xstdout, xstderr = client.exec_command('source /home/w3d/.profile')
print(f'STDOUT: {xstdout.read().decode("utf8")}')
print(f'STDERR: {xstderr.read().decode("utf8")}')

'''stdin, stdout, stderr = client.exec_command('echo "$DATA_DIR"')
print(f'STDOUT: {xstdout.read().decode("utf8")}')
print(f'STDERR: {xstderr.read().decode("utf8")}')
'''

ystdin, ystdout, ystderr = client.exec_command(docker_cmd)
while True:
    output = ystdout.read(80).decode('utf-8')
    print(output)

# Print output of command. Will wait for command to finish.
print(f'STDOUT: {ystdout.read().decode("utf8")}', end="")
print(f'STDERR: {ystderr.read().decode("utf8")}')


# c = Connection(host=host, user=user_name, port=local_port, connect_kwargs={'key_filename': './lior_ecdsa'})
#
# with c.cd('wint3-os'):
#     result2 = c.run('docker compose logs -f --tail 100', hide=True)
#     print(result2.stdout)
#     print("hoi")