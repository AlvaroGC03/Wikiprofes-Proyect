from django.urls import path #Importamos la función path de Django
from django.contrib.auth import views as auth_views #Importamos las vistas de autenticación de Django
from . import views #Importamos las vistas de nuestra aplicación


urlpatterns = [
    path('', views.home, name='home'), #Ruta para la página de inicio
    path('registro/', views.registro, name='registro'), #Ruta para el registro de usuarios
    path('login/', auth_views.LoginView.as_view(template_name='reviews/login.html', redirect_authenticated_user=True), name='login'), #Ruta para el inicio de sesión
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), #Ruta para el cierre de sesión
    path('review/create/', views.crear_review, name='crear_review'), #Ruta para la creación de reseñas
    path('profesor/agregar/', views.agregar_profesor, name='agregar_profesor'), #Ruta para la creación de profesores
    path('materia/agregar/', views.agregar_materia, name='agregar_materia'), #Ruta para la creación de materias
    path('profesores/', views.lista_profesores, name='lista_profesores'), #Ruta para la lista de profesores
    path('profesor/<int:profesor_id>/', views.perfil_profesor, name='perfil_profesor'),
    path('materias/', views.lista_materias, name='lista_materias'),
    path('materia/<int:materia_id>/', views.perfil_materia, name='perfil_materia'), #Ruta para el perfil de un profesor
]
