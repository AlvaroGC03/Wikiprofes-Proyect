from django.shortcuts import render, redirect 
from django.contrib.auth.models import User #Importamos el modelo de usuario de Django
from django.contrib.auth.forms import UserCreationForm #Importamos el formulario de creación de usuario de Django
from django.contrib import messages #Importamos el módulo de mensajes de Django
from django.contrib.auth.decorators import login_required #Importamos el decorador de autenticación de Django
from .models import Review, Profesor, Materia #Importamos el modelo Review
from .forms import ReviewForm, ProfesorForm, MateriaForm #Importamos el formulario ReviewForm
from django.contrib.admin.views.decorators import staff_member_required #Importamos el decorador de staff de Django


def registro(request):
    if request.method == 'POST': #Si se envió el formulario
        form = UserCreationForm(request.POST) #Creamos el formulario con los datos recibidos
        if form.is_valid(): #Si el formulario es válido
            form.save() #Guardamos el usuario en la base de datos
            username = form.cleaned_data.get('username') #Obtenemos el nombre de usuario
            messages.success(request, f'Cuenta creada para {username}!') #Mostramos un mensaje de éxito
            return redirect('login') #Redirigimos al usuario a la página de inicio de sesión
    else:
        form = UserCreationForm() #Creamos un formulario vacío
    return render(request, 'reviews/registro.html', {'form': form}) #Mostramos el formulario de registro

@login_required #Requerimos autenticación
def crear_review(request): 
    if request.method == 'POST': #Si se envió el formulario
        form = ReviewForm(request.POST) #Creamos el formulario con los datos recibidos
        if form.is_valid(): #Si el formulario es válido
            # Verificar si ya existe una reseña de este usuario para el profesor y la materia
            profesor = form.cleaned_data['profesor'] #Obtenemos el profesor de la reseña
            materia = form.cleaned_data['materia'] #Obtenemos la materia de la reseña
            user = request.user #Obtenemos el usuario autenticado
            if Review.objects.filter(profesor=profesor, materia=materia, user=user).exists(): #Si ya existe una reseña
                messages.error(request, 'Ya has realizado una reseña de este profesor en esta materia.') #Mostramos un mensaje de error
            else:
                review = form.save(commit=False) #Guardamos la reseña en la base de datos
                review.user = user #Asignamos el usuario autenticado a la reseña
                review.save() #Guardamos la reseña
                messages.success(request, 'reseña creada exitosamente!')
                return redirect('home')
    else:
        form = ReviewForm() #Creamos un formulario vacío
    return render(request, 'reviews/crear_review.html', {'form': form}) #Mostramos el formulario de creación de reseña

@staff_member_required #Requerimos que el usuario sea staff
def agregar_profesor(request):
    if request.method == 'POST':
        form = ProfesorForm(request.POST) #Creamos el formulario con los datos recibidos
        if form.is_valid(): #Si el formulario es válido
            form.save() #Guardamos el profesor en la base de datos
            messages.success(request, 'Profesor agregado correctamente!')
            return redirect('home')
    else:
        form = ProfesorForm() #Creamos un formulario vacío
    return render(request, 'reviews/agregar_profesor.html', {'form': form}) #Mostramos el formulario de creación de profesor

@staff_member_required
def agregar_materia(request):
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Materia agregada exitosamente!')
            return redirect('home')
    else:
        form = MateriaForm()
    return render(request, 'reviews/agregar_materia.html', {'form': form})

def home(request):
    query = request.GET.get('q', '')  # Captura el texto ingresado en la barra de búsqueda
    return render(request, 'reviews/home.html', {'query': query})