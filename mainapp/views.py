from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from .forms import LoginForm
import platform


def auth(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.data.get('login')
        password = form.data.get('password')
        if User.objects.filter(username=username, is_superuser=True):
            user = authenticate(username=username, password=password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect('/home')
    return render(request, 'login.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def machines(request):
    # TODO:add models for feature machines
    return render(request, 'machines.html')


@login_required
def cli(request):
    return render(request, 'cli.html')


@login_required
def sys_info(request):
    if request.method == 'GET':
        return JsonResponse({
            'sys': platform.system(),
            'architecture': platform.architecture(),
            'machine': platform.machine(),
            'node': platform.node(),
        })
