from django.shortcuts import render, redirect
from main.forms import ContactForm, RegisterForm
from main.models import Contact, Flan
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from main.models import UserProfile


def index(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context = {
            'flanes': []
            }
        if user_profile.user_type == 'free':
            context['flanes'] = Flan.objects.filter(type_flan='free')
        elif user_profile.user_type == 'premium':
            context['flanes'] = Flan.objects.filter(type_flan='free') | Flan.objects.filter(type_flan='premium')
        elif user_profile.user_type == 'diamond':
            context['flanes'] = Flan.objects.filter(type_flan='free') | Flan.objects.filter(type_flan='premium') | Flan.objects.filter(type_flan='diamond')
        return render(request, 'index.html', context)
    else:
        flanes_publicos = Flan.objects.filter(type_flan='free')
        context = {
            'flanes': flanes_publicos,
            }
        return render(request, 'index.html', context)

@login_required
def welcome(request):
    flanes_privados = Flan.objects.filter(is_private=True)
    context = {'flanes': flanes_privados}
    return render(request, 'welcome.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'GET':
        form = ContactForm()                    # Se crea una instancia del formulario ContactForm sin datos iniciales.
        context = {'form': form}                # Se crea un contexto que contiene el formulario vacío.
        return render(request, 'contact.html', context) # Se renderiza la plantilla 'contact.html' con el contexto.
    else:
        form = ContactForm(request.POST)        # Se crea una instancia de ContactForm con los datos enviados en la solicitud POST.
        if form.is_valid():                     # Se verifica si los datos del formulario son válidos.
            Contact.objects.create(
                **form.cleaned_data
            )                                   # Esta es la forma de pedirle a un modelo que cree un registro usando los datos de un formulario
            return redirect('/success')         # Si el formulario es válido, se redirige al usuario a la URL '/success'.
        context = {'form': form}                # Se crea un contexto que contiene el formulario con los datos (válidos o no).
        return render(request, 'contact.html', context) # Se vuelve a renderizar la plantilla con el contexto actualizado.

def prices(request):
    if request.user.has_perm('main.delete_flan'):
        messages.warning(request, "Puedes borrar flanes")
        return render(request, 'prices.html')
    else:
        return render(request, 'prices.html')

def ayuda(request):
    return render(request, 'ayuda.html')

def success(request):
    return render(request, 'success.html')

def logout_view(request):
    logout(request)
    messages.warning(request, "¡Has salido exitosamente!")
    return redirect('/')

class LoginViewPropia(SuccessMessageMixin ,LoginView):
    success_message = 'Bienvenido, '

# Esta vista solo la puede ver quien puede borrar flan
@permission_required('main.delete_flan')
def pruebas(request):
    return render(request, 'pruebas.html')

# Esta vista solo renderiza los tipos de suscripciones
def suscriptions(request):
    return render (request, 'registration/suscriptions.html')


def register_user(request, user_type):
    form = RegisterForm()
    context = {'form': form}
    
    if request.method == 'GET':
        return render(request, f'registration/register{user_type}.html', context)
    
    form = RegisterForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        if data['password'] != data['passRepeat']:
            messages.error(request, 'Ambas contraseñas deben ser iguales')
            return redirect(f'/register{user_type}')
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        UserProfile.objects.create(
            user=user,
            user_type=user_type
        )
        messages.success(request, '¡Usuario creado! por favor, inicie sesión')
        return redirect('/')
    
    context['form'] = form
    return render(request, f'registration/register{user_type}.html', context)

def registerfree(request):
    return register_user(request, 'free')

def registerpremium(request):
    return register_user(request, 'premium')

def registerdiamond(request):
    return register_user(request, 'diamond')