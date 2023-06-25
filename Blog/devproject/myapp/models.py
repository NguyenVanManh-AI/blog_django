from django.db import models
# from django.contrib.auth.models import AbstractUser

# Create your models here.
class Employee(models.Model):  
    name = models.CharField(max_length=100)  
    email = models.EmailField()  
    contact = models.CharField(max_length=15) 
   
    class Meta:  
        db_table = "tblemployee"

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)

    class Meta:
        db_table = "tbuser"

# # Provide unique related_name for groups and user_permissions fields
# User._meta.get_field('groups').related_name = 'custom_user_groups'
# User._meta.get_field('user_permissions').related_name = 'custom_user_user_permissions'