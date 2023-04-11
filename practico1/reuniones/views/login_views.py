import hashlib

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from reuniones.models.Usuario import Usuario


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        obj_usuario = Usuario.objects.filter(username=username).first()
        if obj_usuario is None:
            return HttpResponseRedirect(reverse('login'))

        hashed_password = make_password_sha1(password)
        if obj_usuario.password != hashed_password:
            return HttpResponseRedirect(reverse('login'))

        request.session['username'] = username
        return HttpResponseRedirect(reverse('reunion.list.usuario'))

    return render(request, 'reuniones/login/inicio.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def make_password_sha1(password):
    return hashlib.sha1(password.encode('utf-8')).hexdigest()