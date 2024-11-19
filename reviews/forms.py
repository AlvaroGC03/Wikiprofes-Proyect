from django import forms # Importamos forms
from .models import Review, Profesor, Materia #Agregamos la clase Review

class ReviewForm(forms.ModelForm): #Creamos la clase ReviewForm que hereda de forms.ModelForm 
    class Meta: 
        model = Review
        fields = ['profesor', 'materia', 'comentario', 'dominio', 'puntualidad', 'asistencia', 'dificultad', 'seguimiento'] #Definimos los campos que se mostrarán en el formulario
        widgets = {
            'dominio': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'puntualidad': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'asistencia': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'dificultad': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'seguimiento': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

    # Validación personalizada para campos numéricos
    def clean_dominio(self):
        dominio = self.cleaned_data.get('dominio')
        if dominio < 1 or dominio > 5:
            raise forms.ValidationError("El dominio debe estar entre 1 y 5.")
        return dominio

    def clean_puntualidad(self):
        puntualidad = self.cleaned_data.get('puntualidad')
        if puntualidad < 1 or puntualidad > 5:
            raise forms.ValidationError("La puntualidad debe estar entre 1 y 5.")
        return puntualidad

    def clean_asistencia(self):
        asistencia = self.cleaned_data.get('asistencia')
        if asistencia < 1 or asistencia > 5:
            raise forms.ValidationError("La asistencia debe estar entre 1 y 5.")
        return asistencia

    def clean_dificultad(self):
        dificultad = self.cleaned_data.get('dificultad')
        if dificultad < 1 or dificultad > 5:
            raise forms.ValidationError("La dificultad debe estar entre 1 y 5.")
        return dificultad

    def clean_seguimiento(self):
        seguimiento = self.cleaned_data.get('seguimiento')
        if seguimiento < 1 or seguimiento > 5:
            raise forms.ValidationError("El seguimiento debe estar entre 1 y 5.")
        return seguimiento

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