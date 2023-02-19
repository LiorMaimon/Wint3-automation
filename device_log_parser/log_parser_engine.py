import paramiko
import re


# SSH tunnel parameters
local_port = 31315
remote_ip = '10.0.0.1'
remote_port = 22
ssh_username = 'user'
ssh_server = '192.168.1.14'