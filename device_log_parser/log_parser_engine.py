from time import sleep
from fabric import Connection, Config
import paramiko


# SSH tunnel parameters
local_port = 31315
host = '192.168.1.14'
user_name = 'w3d'

c = Connection(host=host, user=user_name, port=local_port, connect_kwargs={'key_filename': './lior_ecdsa'})

with c.cd('wint3-os'):
    result2 = c.run('docker compose logs -f --tail 100', hide=True)
    print(result2.stdout)
    print("hoi")