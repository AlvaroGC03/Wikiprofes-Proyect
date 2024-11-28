from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User #Importamos el modelo de usuario de Django
from django.contrib.auth.forms import UserCreationForm #Importamos el formulario de creación de usuario de Django
from django.contrib import messages #Importamos el módulo de mensajes de Django
from django.contrib.auth.decorators import login_required #Importamos el decorador de autenticación de Django
from .models import Review, Profesor, Materia #Importamos el modelo Review
from .forms import ReviewForm, ProfesorForm, MateriaForm #Importamos el formulario ReviewForm
from django.contrib.admin.views.decorators import staff_member_required #Importamos el decorador de staff de Django
from django.db.models import Avg, Q


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

    # Obtener las listas completas de profesores y materias
    profesores = Profesor.objects.all()
    materias = Materia.objects.all()

    # Inicializar resultados de búsqueda
    resultados_profesores = []
    resultados_materias = []

    if query:
        # Realizar la búsqueda si hay un término
        resultados_profesores = profesores.filter(nombre__icontains=query)
        resultados_materias = materias.filter(nombre__icontains=query)

    # Pasar todos los datos al contexto
    context = {
        'query': query,
        'resultados_profesores': resultados_profesores,
        'resultados_materias': resultados_materias,
        'profesores': profesores,  # Asegurarnos de incluir siempre la lista completa
        'materias': materias,      # Asegurarnos de incluir siempre la lista completa
    }

    return render(request, 'reviews/home.html', context)
def lista_profesores(request):
    profesores = Profesor.objects.all()  # Obtener todos los profesores
    return render(request, 'reviews/profesores.html', {'profesores': profesores})

def perfil_profesor(request, profesor_id):
    # Obtener el profesor por su ID
    profesor = get_object_or_404(Profesor, id=profesor_id)

    # Obtener todas las reseñas del profesor
    reviews = profesor.reviews.all()

    if reviews.exists():
        # Calcular el promedio general y el promedio por rubro
        promedio_general = (
            reviews.aggregate(
                avg_general=(
                    Avg('dominio') +
                    Avg('puntualidad') +
                    Avg('asistencia') +
                    Avg('dificultad') +
                    Avg('seguimiento')
                ) / 5
            )['avg_general']
        )
        promedio_dominio = reviews.aggregate(Avg('dominio'))['dominio__avg']
        promedio_puntualidad = reviews.aggregate(Avg('puntualidad'))['puntualidad__avg']
        promedio_asistencia = reviews.aggregate(Avg('asistencia'))['asistencia__avg']
        promedio_dificultad = reviews.aggregate(Avg('dificultad'))['dificultad__avg']
        promedio_seguimiento = reviews.aggregate(Avg('seguimiento'))['seguimiento__avg']
    else:
        # Si no hay reseñas, asignar 0 como promedio
        promedio_general = 0
        promedio_dominio = 0
        promedio_puntualidad = 0
        promedio_asistencia = 0
        promedio_dificultad = 0
        promedio_seguimiento = 0

    # Pasar los datos al template
    context = {
        'profesor': profesor,
        'reviews': reviews,
        'promedio_general': promedio_general,
        'promedio_dominio': promedio_dominio,
        'promedio_puntualidad': promedio_puntualidad,
        'promedio_asistencia': promedio_asistencia,
        'promedio_dificultad': promedio_dificultad,
        'promedio_seguimiento': promedio_seguimiento,
    }

    return render(request, 'reviews/perfil_profesor.html', context)

def lista_materias(request):
    materias = Materia.objects.all()
    return render(request, 'reviews/materias.html', {'materias': materias})

def perfil_materia(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id)
    reviews = materia.reviews.all()
    return render(request, 'reviews/perfil_materia.html', {
        'materia': materia,
        'reviews': reviews,
    })
