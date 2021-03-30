from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.contrib import messages
from .forms import LoginForm, MachineForm
from .models import Machine
import platform
import json
import paramiko

COMMAND = ''
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def auth(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.data.get('login')
        password = form.data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect('/home')
    return render(request, 'login.html', {'form': form})


@login_required
def sys_info(request):
    if request.method == 'GET':
        return JsonResponse({
            'sys': platform.system(),
            'architecture': platform.architecture(),
            'machine': platform.machine(),
            'node': platform.node(),
        })


class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html', )


class MachinesView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        machines = Machine.objects.all()
        context = {'machines': machines}
        return render(request, 'machines.html', context=context)


class AddMachineView(LoginRequiredMixin, CreateView):
    form_class = MachineForm
    template_name = 'add_machine.html'

    def form_valid(self, form):
        form.save(commit=True)
        return HttpResponseRedirect('/home')


class DeleteMachineView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        ip = kwargs.get('ip_addr')
        port = kwargs.get('port')
        machine = Machine.objects.get(ip_address=ip, port=port)
        machine.delete()
        # messages.add_message(request, messages.INFO, f"Machine with ip {ip}:{port} was deleted")
        return HttpResponseRedirect('/machines')


class CLIView(LoginRequiredMixin, View):
    template_name = 'cli.html'

    def get(self, request, *args, **kwargs):
        global COMMAND
        if request.method == 'GET' and request.META['CONTENT_TYPE'] == 'application/json; charset=utf-8':
            output = ''
            if COMMAND:
                stdin, stdout, stderr = client.exec_command(COMMAND, get_pty=True)
                output = ''.join(iter(stdout.readline, ''))
            return JsonResponse({'message': output})
        return render(request, 'cli.html')

    def post(self, request, *args, **kwargs):
        global COMMAND
        request_body = json.loads(request.body)
        if request_body['cmd'] == 'login':
            return HttpResponse('success')

        elif request_body['cmd'] == 'password':
            username, password = request_body['user']
            ip_addr = kwargs.get('ip_addr')
            client.connect(ip_addr, username=username, password=password)

        else:
            COMMAND = request_body['cmd'] + ' ' + ' '.join(request_body['args'])
        return HttpResponse('ok')
