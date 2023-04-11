from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse

from reuniones.models.Asistente import Asistente
from reuniones.models.Reunion import Reunion
from reuniones.models.Usuario import Usuario


def lista_reuniones(request):
    if 'username' in request.session:
        return HttpResponseRedirect(reverse('reunion.list.usuario'))

    template = loader.get_template('reuniones/reuniones/list.html')
    try:
        lista = Reunion.objects.all()
        lista_usuarios = Usuario.objects.all()
        context = {
            'reuniones': lista,
            'usuarios': lista_usuarios
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print(e)
        return HttpResponseServerError("Error al cargar la lista de reuniones")


def lista_reuniones_usuario(request):
    template = loader.get_template('reuniones/login/userList.html')
    try:
        usuario = Usuario.objects.get(username=request.session['username'])
        # traeme todas las reuniones donde el usuario es dueño o asistente
        lista = Reunion.objects.filter(dueño=usuario) | Reunion.objects.filter(asistentes=usuario)
        context = {
            'reuniones': lista
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print(e)
        return HttpResponseServerError("Error al cargar la lista de reuniones")


def create_reuniones(request):
    if request.method == 'GET':
        lista_usuarios = Usuario.objects.all()
        return render(
            request,
            'reuniones/reuniones/create.html',
            {"usuarios": lista_usuarios}
        )

    dueño_id = request.POST.get('dueño')
    asistentes_ids = request.POST.getlist('asistentes')
    try:
        dueño = Usuario.objects.get(pk=dueño_id)
        print(dueño)
    except Usuario.DoesNotExist:
        return HttpResponseRedirect(reverse('reunion.list'))
    reunion = Reunion(
        nombre_reunion=request.POST['nombre_reunion'],
        fecha_hora=request.POST['fecha_hora'],
        dueño=dueño,
    )
    reunion.save()

    print(reunion.id)

    asistentes = Usuario.objects.filter(pk__in=asistentes_ids)
    for asistente in asistentes:
        Asistente.objects.create(
            reunion=reunion,
            asistente=asistente,
        )

    return HttpResponseRedirect(reverse('reunion.list'))


def edit_reuniones(request, id):
    obj_reunion = Reunion.objects.filter(pk=id)
    if obj_reunion.count() == 0:
        return HttpResponseRedirect(reverse('reunion.list'))
    obj_reunion = obj_reunion.first()
    if request.method == 'GET':
        lista_usuarios = Usuario.objects.all()
        asistentes = [a.asistente.id for a in obj_reunion.asistente_set.all()]
        return render(
            request,
            'reuniones/reuniones/edit.html',
            {
                "reunion": obj_reunion,
                "usuarios": lista_usuarios,
                "asistentes_seleccionados": asistentes,
            }
        )

    obj_usuario = Usuario.objects.filter(pk=request.POST["dueño"])
    if obj_usuario.count() == 0:
        return HttpResponseRedirect(reverse('reunion.list'))

    obj_reunion.nombre_reunion = request.POST["nombre_reunion"]
    obj_reunion.fecha_hora = request.POST["fecha_hora"]
    obj_reunion.dueño = obj_usuario.first()
    obj_reunion.save()

    if "asistentes" not in request.POST:
        user_ids = []
    else:
        user_ids = [int(id) for id in request.POST.getlist("asistentes")]
    obj_usuario_asistentes = Usuario.objects.filter(pk__in=user_ids)

    # Eliminar asistentes antiguos
    obj_reunion.asistente_set.all().delete()

    # Agregar nuevos asistentes
    asistentes = [
        Asistente(reunion=obj_reunion, asistente=user)
        for user in obj_usuario_asistentes
    ]
    Asistente.objects.bulk_create(asistentes)

    return HttpResponseRedirect(reverse('reunion.list'))


def delete_reuniones(request, id):
    obj_reunion = Reunion.objects.filter(pk=id)
    if obj_reunion.count() == 0:
        return HttpResponseRedirect(reverse('reunion.list'))
    obj_reunion.delete()

    return HttpResponseRedirect(reverse('reunion.list'))
