from django.db import models
from datetime import datetime
import re, bcrypt

from django.db.models.deletion import CASCADE
# Create your models here.
# EMAIL_REGEX = re.compile(r'^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4}')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator_registration(self, postData):
        errors = {}
        already_exist = User.objects.filter(email=postData['email']) #?
        if len(postData['first_name'])<2:
            errors['first_name']  = "first name must be more than 2 characters"

        if len(postData['password'])<8:
            errors['password'] = "password must be atleas 8 characters"
        elif postData['password'] != postData['confirm_password']:
            errors['password'] = "Paswords do not match"

        if len(postData['email'])<1:
            errors['email'] = "email cannot be blank"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        elif already_exist:
            errors['email'] = "email already exist"

        # user_birthday  = datetime.strptime(postData['birthday'], '%Y-%m-%d')     
        # age = (datetime.now() - user_birthday).days/365 
        # print("User age", age)
        # if age<1:
        #     errors['birthday'] = "must be older than 1 years old"

        return errors

    def validator_login(self, postData):
        errors={}
        check_user_exist = User.objects.filter(email = postData['email'])
        
        if  not EMAIL_REGEX.match(postData['email']):
            errors['login_email'] = "Invalid email address"
        elif not check_user_exist:
            errors['login_email'] = "You are not registered"
        else:
            if not bcrypt.checkpw( postData['password'].encode() , check_user_exist[0].password.encode() ):
                errors['login_email'] = "Wrong password"
        return errors


class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors={}

        if len(postData['quoted_by'])<1:
            errors['quoted_by'] = "Quoted_by should be 2 or more characters"
        if len(postData['quote'])<10:
            errors['quote'] = "Quote should be 10 or more characters"
        return errors




class User(models.Model):
    first_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password=models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = UserManager()


class Quote(models.Model):
    quoted_by = models.CharField(max_length=255)
    quote = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, related_name="user_quoutes", on_delete=CASCADE)
    favorit_users = models.ManyToManyField(User, related_name="user_favorit_quoptes")
    objects = QuoteManager()


