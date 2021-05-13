import json
import platform
import time
from channels.generic.websocket import AsyncWebsocketConsumer
from paramiko.ssh_exception import AuthenticationException
import paramiko


class WSConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = ''
        self.login = ''
        self.password = ''
        self.port = 0
        self.ip = ''
        self.client = paramiko.SSHClient()
        self.ssh = None

    async def connect(self):
        await self.accept()
        await self.send(json.dumps({
            'sys': platform.system(),
            'architecture': platform.architecture(),
            'machine': platform.machine(),
            'node': platform.node(),
        }))

    async def disconnect(self, code):
        self.client.close()

    async def receive(self, text_data=None, bytes_data=None):
        data_json = json.loads(text_data)
        command = data_json['cmd']
        if command == 'login':
            self.ip, self.port, self.login = data_json['data']
            await self.send(json.dumps({'message': [self.ip, self.port, self.login]}))
        elif command == 'password':
            password = data_json['password']
            self.password = password
            try:
                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.client.connect(
                    hostname=self.ip,
                    port=self.port,
                    username=self.login,
                    password=self.password,
                )
                self.ssh = self.client.invoke_shell()
                self.ssh.send('')
                self.ssh.send('')
                time.sleep(1)
                await self.send(json.dumps({'message': self.ssh.recv(60000).decode('utf-8')}))

            except AuthenticationException:
                await self.send(json.dumps({'message': 'Authentication failed'}))
                await self.disconnect(401)

        elif command and data_json['is_command']:
            command += ' ' + ' '.join(data_json['args'])
            self.ssh.send(f"{command}\n")
            self.ssh.settimeout(0.1)
            data = self.ssh_output()

            await self.send(json.dumps({'message':data}))

    def ssh_output(self):
        output = ""
        while True:
            try:
                part = self.ssh.recv(60000).decode('utf-8')
                output += part
                time.sleep(0.1)
            except:
                break
        return "\r\n".join(output.split('\r\n')[:-1])