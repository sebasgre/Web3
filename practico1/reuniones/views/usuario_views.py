from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from reuniones.models.Usuario import Usuario


def lista_usuarios(request):
    template = loader.get_template('reuniones/usuarios/list.html')
    lista = Usuario.objects.all()
    context = {
        'usuarios': lista
    }
    return HttpResponse(template.render(context, request))


def make_password_sha1(password):
    import hashlib
    return hashlib.sha1(password.encode('utf-8')).hexdigest()


def create_usuarios(request):
    if request.method == 'GET':
        return render(request, 'reuniones/usuarios/create.html', {})
    obj_usuario = Usuario()
    obj_usuario.first_name = request.POST["first_name"]
    obj_usuario.last_name = request.POST["last_name"]
    obj_usuario.username = request.POST["username"]
    obj_usuario.email = request.POST["email"]
    obj_usuario.password = make_password_sha1(request.POST["password"])
    obj_usuario.save()

    return HttpResponseRedirect(reverse('usuario.list'))


def edit_usuarios(request, id):
    obj_usuario = Usuario.objects.filter(pk=id)
    if obj_usuario.count() == 0:
        return HttpResponseRedirect(reverse('usuario.list'))
    obj_usuario = obj_usuario.first()
    if request.method == 'GET':
        return render(
            request,
            'reuniones/usuarios/edit.html',
            {"usuario": obj_usuario}
        )
    obj_usuario.first_name = request.POST["first_name"]
    obj_usuario.last_name = request.POST["last_name"]
    obj_usuario.username = request.POST["username"]
    obj_usuario.email = request.POST["email"]
    obj_usuario.password = request.POST["password"]
    obj_usuario.save()

    return HttpResponseRedirect(reverse('usuario.list'))


def delete_usuarios(request, id):
    obj_usuario = Usuario.objects.filter(pk=id)
    if obj_usuario.count() == 0:
        return HttpResponseRedirect(reverse('usuario.list'))
    obj_usuario.delete()

    return HttpResponseRedirect(reverse('usuario.list'))
