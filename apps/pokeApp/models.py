# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

# Create your models here.
class UserManager(models.Manager) :
   

    def register(self,post):
        errorMsgs = []
        user = {}
        returnVal = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]')

        if post['name'] == "" :
            errorMsgs.append({'message': 'Name is required', 'extra_tags':"register"})
        elif len(post['name']) < 3 :
            errorMsgs.append({'message':'Name has to be minimum 3 characters long', 'extra_tags':"register"})

        if post['alias'] == "" :
            errorMsgs.append({'message':'alias is required', 'extra_tags':"register"})
        elif len(post['alias']) < 3 :
            errorMsgs.append({'message':'alias has to be minimum 3 characters long', 'extra_tags':"register"})

        if not post['alias']:
		    error = {'message': 'Email is required', 'extra_tags': 'register'}
		    errorMsgs.append(error)
        elif not EMAIL_REGEX.match(post['email']):
			error = {'message': 'Invalid email address', 'extra_tags': 'register'}
			errorMsgs.append(error)
		
        if post['password'] == "" :
            errorMsgs.append({'message':'password is required', 'extra_tags':"register"})
        elif len(post['password']) < 8:
            errorMsgs.append({'message':'Password has to be mininum 8 characters long', 'extra_tags':"register"})
            print "password less than 8"      
        elif post['password'] != post['confirm_password'] :
            errorMsgs.append({'message':'Passwords do not match.', 'extra_tags':"register"})
            print "password mismatch"

        if 'birth_date' not in post or post['birth_date'] == "":
		    error = {'message': 'Please select birth date', 'extra_tags': 'register'}
		    errorMsgs.append(error)
        # elif post['birth_date'] == "":
		# 	error = {'message': 'Invalid birth date', 'extra_tags': 'register'}
		# 	errorMsgs.append(error)

        try: 
            user = Users.objects.get(email = post['email'])
            print "user: ", user
            errorMsgs.append({'message':'User with {} email already exists.'.format(post['email']), 'extra_tags':"register"})
            print "user exists"
            error = True
        except Users.DoesNotExist:
            if (len(errorMsgs) == 0):
                hash1 = bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt())
                user = Users.objects.create(name=post['name'], alias=post['alias'], email=post['email'], password = hash1, birth_date=post['birth_date'], receivedPokes=0)
                print "added user"
                print "User does not exist"
                
        returnVal = {'user':user,'errors':errorMsgs}
        return returnVal

    def login (self, post) :
        errorMsgs = []
        user = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]')

        if post['login_email'] == "" :
            errorMsgs.append({'message':'username is required', 'extra_tags':"login"})
        if post['login_password'] == "" :
            errorMsgs.append({'message':'password is required', 'extra_tags':"login"})
        if not EMAIL_REGEX.match(post['login_email']) :
            errorMsgs.append({'message':'Invalid email', 'extra_tags':"login"})

        if (len(errorMsgs) == 0):
            try :
                user = Users.objects.get(email = post['login_email'])
                print user
                print user.password
                if bcrypt.checkpw(post['login_password'].encode(), user.password.encode()):
                    print "login successful"
                else: 
                    print "password mismatch"
                    errorMsgs.append({'message':'Incorrect User Id or Password. Please try again', 'extra_tags':'login'})
                    user = {}
            except Users.DoesNotExist:
                print "user not found"
                errorMsgs.append({'message':'Incorrect User Id or Password. Please try again', 'extra_tags':'login'})

        return {'user': user, 'errors': errorMsgs}

class PokeManager(models.Manager) :
    def pokeUser(self, receiverId, pokerId):
        # Get the receiver of the poke
        receiver = Users.objects.get(pk=receiverId)
        print "reciever: ", receiver
        # Get the poker
        poker =  Users.objects.get(pk=pokerId)

        # If this is receiver's first poke then create an entry in the Pokes table,
        # else update the poke count
        pokeEntry = Pokes.objects.filter(receiver=receiver, poker=poker)
        print "pokeEntry ", pokeEntry
        if (len(pokeEntry)==0) :
            newPoke = Pokes.objects.create(receiver=receiver, poker=poker, numPokesByPoker=1)
            print "Created new poke: ", newPoke
        else :
            pokeEntry[0].numPokesByPoker += 1
            pokeEntry[0].save()
            print "Updated poke: ", pokeEntry
        
        # Update receiver's receivedPokes
        receiver.receivedPokes += 1
        receiver.save() 

class Users(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=8)
    birth_date = models.DateTimeField('date hired')
    receivedPokes = models.IntegerField()
    objects = UserManager()
    def __str__(self):
        return "{} {} {} {}".format(self.name, self.alias, self.email, self.password) 

class Pokes(models.Model):
    name = models.CharField(max_length=255)
    receiver = models.ForeignKey('Users', related_name = "pokes")
    poker = models.ForeignKey('Users', related_name = "poked_by")
    numPokesByPoker = models.IntegerField()
    objects = PokeManager()
    def __str__(self):
        return "{} {} {}".format(self.receiver.name, self.poker.name, self.numPokesByPoker) 

