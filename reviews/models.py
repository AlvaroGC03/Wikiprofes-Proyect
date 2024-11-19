from django.db import models
from django.contrib.auth.models import User #Importamos el modelo de usuario de Django

# Modelo de Materia
class Materia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    profesores = models.ManyToManyField('Profesor', related_name='Materias')

    def __str__(self):
        return self.nombre

# Modelo de Profesor
class Profesor(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Modelo de Reseña
class Review(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='reviews')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    # Campos de puntuación (del 1 al 5)
    dominio = models.PositiveSmallIntegerField()
    puntualidad = models.PositiveSmallIntegerField()
    asistencia = models.PositiveSmallIntegerField()
    dificultad = models.PositiveSmallIntegerField()
    seguimiento = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('profesor', 'materia', 'user')  # Evita duplicados

    def __str__(self):
        return f'Review by {self.user.username} for {self.profesor.nombre}'

# Modelo de Reacción
class Reaccion(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField()  # True para like, False para dislike

    class Meta:
        unique_together = ('review', 'user')  # Evita múltiples reacciones

    def __str__(self):
        reaction_type = "Like" if self.is_like else "Dislike"
        return f'{reaction_type} by {self.user.username} on review {self.review.id}'

