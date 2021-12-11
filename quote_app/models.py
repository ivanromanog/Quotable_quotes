from django.db import models
from datetime import datetime
import re, bcrypt

# Create your models here.

EMAIL_REGEX = re.compile('^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4})')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['email'])
        if len(postData['nombre']) < 2:
            errors['nombre'] = "Nombre debe tener mas de 2 caracteres de largo."
        if len(postData['apellido']) < 2:
            errors['apellido'] = "Apellido debe tener mas de 2 caracteres de largo."
        if len(postData['password']) < 8:
            errors['password'] = "Contraseña debe tener mas de 8 caracteres de largo."
        elif postData['password'] != postData['confirm_password']:
            errors['password'] = "Contraseña no coincide."
        if len(postData['email']) < 1:
            errors['reg_email'] = "Email no puede quedar vacio."
        elif not EMAIL_REGEX.match(postData['email']):
            errors['reg_email'] = "Por favor entre una direccion de email valida."
        elif check:
            errors['reg_email'] = "Direccion de email ya esta resgitrada."
        return errors
    
    def login_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['login_email'])
        if not check:
            errors['login_email'] = "Email no ha sido registrado."
        else:
            if not bcrypt.checkpw(postData['login_password'].encode(), check[0].password.encode()):
                errors['login_email'] = "Email y contraseña no coinciden."
        return errors

class User(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData['quotee']) < 2:
            errors['quotee'] = "Cita debe tener al menos 2 caracteres de largo."
        if len(postData['message']) < 10:
            errors['message'] = "Mensaje debe tener al menos 10 caracteres de largo."
        return errors

class Quote(models.Model):
    quotee = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="has_created_quotes", on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="favorited_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()