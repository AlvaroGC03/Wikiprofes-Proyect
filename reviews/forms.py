from django import forms # Importamos forms
from .models import Review, Profesor, Materia #Agregamos la clase Review

class ReviewForm(forms.ModelForm): #Creamos la clase ReviewForm que hereda de forms.ModelForm 
    class Meta: 
        model = Review
        fields = ['profesor', 'materia', 'comentario', 'dominio', 'puntualidad', 'asistencia', 'dificultad', 'seguimiento'] #Definimos los campos que se mostrarán en el formulario
        widgets = {
            'doimnio': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'puntualidad': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'asistencia': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'dificultad': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'seguimiento': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['nombre']

class MateriaForm(forms.ModelForm):
    profesores = forms.ModelMultipleChoiceField(
        queryset=Profesor.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Materia  # Asegúrate de que el modelo se llame Materia y no Subject
        fields = ['nombre', 'profesores']  # Incluye todos los campos de Materia que necesitas en el formulario