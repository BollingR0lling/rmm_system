from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import View
from django.views.generic.edit import CreateView
from .forms import LoginForm, MachineForm
from .models import Machine
import platform
import json


def auth(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.data.get('login')
        password = form.data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect('/home')
    return render(request, 'login.html', {'form': form})


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
        ip = form.data.get('ip_address')
        data = []
        with open("/app/ci/targets.json") as file:
            data = json.load(file)
            # data[0] - is dict
            data[0]['targets'].append(f'{ip}:9100')
        with open("/app/ci/targets.json", 'w') as file:
            file.write(json.dumps(data))
        return HttpResponseRedirect('/machines')


class DeleteMachineView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ip = kwargs.get('ip_addr')
        port = kwargs.get('port')
        machine = Machine.objects.get(ip_address=ip, port=port)
        machine.delete()
        return HttpResponseRedirect('/machines')


class WSview(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ip = kwargs.get('ip_addr')
        port = kwargs.get('port')
        machine = Machine.objects.get(ip_address=ip, port=port)
        return render(request, 'cli.html', context={'machine': machine})
