from django.db import models

# Create your models here.

import re
import bcrypt 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def validate(self,form):
        errors={}

        if len(form['first_name']) < 3:
            errors['first_name'] = 'First Name must be at least 2 characters' 

        if len(form['last_name']) < 3:
            errors['last_name'] = 'Last Name must be at least 2 characters'

        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'

        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = 'Email already in use'

        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'

        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'

        return errors
        
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return user if bcrypt.checkpw(password.encode(), user.password.encode()) else None

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name=form['first_name'],
            last_name=form['last_name'],
            email=form['email'],
            password=pw,
        )


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()

class TripManager(models.Manager):
    def validate(self, form):
        errors = {}
        
        if len(form['destination']) < 5:
            errors['destination'] = 'Destination must be atleast 5 characters.'
    
        if len(form['plan']) < 5:
            errors['plan'] = 'Plan must be atleast 5 characters.'

        return errors


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    plan = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    traveler = models.ForeignKey(User, related_name='trip_uploaded', on_delete=models.CASCADE, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()