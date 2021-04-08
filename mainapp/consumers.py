import json
import platform

from channels.generic.websocket import WebsocketConsumer
import paramiko


class WSConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = ''
        self.login = ''
        self.password = ''
        self.port = 0
        self.ip = ''
        self.client = paramiko.SSHClient()

    def connect(self):
        self.accept()
        self.send(json.dumps({
            'sys': platform.system(),
            'architecture': platform.architecture(),
            'machine': platform.machine(),
            'node': platform.node(),
        }))

    def disconnect(self, code):
        self.client.close()
        pass

    def receive(self, text_data=None, bytes_data=None):
        data_json = json.loads(text_data)
        command = data_json['cmd']
        if command == 'login':
            self.ip, self.port, self.login = data_json['data']
            self.send(json.dumps({'message': [self.ip, self.port, self.login]}))
        elif command == 'password':
            password = data_json['password']
            self.password = password
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.ip,
                port=self.port,
                username=self.login,
                password=self.password,
            )
            self.send(json.dumps({'message': 'success'}))
        elif command and data_json['args']:
            command += ' ' + ' '.join(data_json['args'])
            stdin, stdout, stderr = self.client.exec_command(command, get_pty=True)
            output = ''.join(iter(stdout.readline, ''))
            self.send(json.dumps({'message': output}))
