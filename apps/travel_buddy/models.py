from django.db import models
import re
from datetime import datetime
import bcrypt

now = str(datetime.now())

class UserManager(models.Manager):
    def regValidator(self, form):
        errors = {}
        if len(form['username']) == 0:
            errors['username'] = 'Username cannot be blank'
        elif len(form['username']) < 3:
            errors['username'] = 'Username must be atleast three characters'
        else:
            users = User.objects.filter(username=form['username'])
            if users:
                errors['username'] = "User is already in database"
        if len(form['name']) == 0:
            errors['name'] = 'Name cannot be blank'  
        if len(form['password']) == 0:
            errors['password'] = 'Password cannot be blank'
        elif len(form['password']) < 8:
            errors['password'] = 'Password must be atleast eight characters'
        if form['confirm_password'] != form['password']:
            errors['confirm_password'] = 'Passwords do not match!'
        return errors

    def loginValidator(self, form):
        errors = {}
        if len(form['pwd']) == 0:
            errors['pwd'] = 'Password cannot be blank'
        if len(form['user_name']) == 0:
            errors['user_name'] = 'Username cannot be blank' 
        else:
            users = User.objects.filter(username=form['user_name'])
            if not users:
                errors['user_name'] = 'This user doesnt exist. Please register!'
            elif not bcrypt.checkpw(form['pwd'].encode(), users[0].password.encode()):
                errors['pwd'] = 'Wrong password'
        return errors
        
class TravelManager(models.Manager):
    def travelValidator(self, form):
        print(form)
        errors = {}      
        if len(form['destination']) == 0:
            errors['destination'] = 'Destination cannot be blank'
        if len(form['description']) == 0:
            errors['description'] = 'Description cannot be blank'
        if len(form['travelstart']) == 0:
            errors['travelstart'] = 'Start date cannot be blank'
        elif form['travelstart'] < now:
            errors['travelstart'] = 'Theres no planning trips for the past'
        elif form['travelstart'] > form['travelend']:
            errors['travelstart'] = 'Can not schedule a departure after a return'
        if len(form['travelend']) == 0:
            errors['travelend'] = 'End date cannot be blank'
        elif form['travelend'] < form['travelstart']:
            errors['travelend'] = 'Can not schedule a return before a departure'
        elif form['travelend'] == form['travelstart']:
            errors['travelend'] = 'Can not leave and return same day, No Teleporting.....yet'
        return errors
            
class User(models.Model):
    username = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Travel(models.Model):
    destination = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    added_by = models.ForeignKey(User, related_name='travel', on_delete=models.CASCADE)
    travelstart = models.DateField()
    travelend = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TravelManager()
    


class Join(models.Model):
    user = models.ForeignKey(User, related_name='trip', on_delete=models.CASCADE)
    travel = models.ForeignKey(Travel, related_name='trip', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)