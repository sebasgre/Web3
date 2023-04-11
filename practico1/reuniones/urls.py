from django.urls import path

from reuniones.views import reunion_views, login_views, register_views
from reuniones.views import usuario_views


urlpatterns = [
    path('login', login_views.login_view, name="login"),
    path('register', register_views.register_view, name="register"),
    path('logout', login_views.logout_view, name="logout"),
    path('reuniones/list', reunion_views.lista_reuniones, name="reunion.list"),
    path('reuniones/usuarioList', reunion_views.lista_reuniones_usuario, name="reunion.list.usuario"),
    path('reuniones/create', reunion_views.create_reuniones, name="reunion.create"),
    path('reuniones/edit/<int:id>', reunion_views.edit_reuniones, name="reunion.edit"),
    path('reuniones/delete/<int:id>', reunion_views.delete_reuniones, name="reunion.delete"),
    path('usuarios/list', usuario_views.lista_usuarios, name="usuario.list"),
    path('usuarios/create', usuario_views.create_usuarios, name="usuario.create"),
    path('usuarios/edit/<int:id>', usuario_views.edit_usuarios, name="usuario.edit"),
    path('usuarios/delete/<int:id>', usuario_views.delete_usuarios, name="usuario.delete"),
]