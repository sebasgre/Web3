import hashlib

from django.contrib import messages
from django.shortcuts import redirect, render

from reuniones.models.Usuario import Usuario


def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Verifica que las contraseñas coincidan
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Hashea la contraseña del usuario
        hashed_password = make_password_sha1(password1)

        # Crea un nuevo usuario
        usuario = Usuario(first_name=first_name, last_name=last_name, username=username, email=email, password=hashed_password)
        usuario.save()

        # Redirige al usuario a la página de inicio de sesión
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    # Si la solicitud es GET, muestra el formulario de registro
    return render(request, 'reuniones/login/inicio.html')


def make_password_sha1(password):
    return hashlib.sha1(password.encode('utf-8')).hexdigest()
