# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import *
import re
import bcrypt
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def index (request) :  
    return render(request, 'pokeApp/index.html')

def register(request) :
    error = False
    context = {}
    print "in register"

    if request.method == "POST":
        print request.POST

        returnVal = Users.objects.register(request.POST)
        if returnVal['user'] :
            request.session['logged_in_user'] = returnVal['user'].id
            print "logged in user: ",request.session['logged_in_user']
            return redirect(reverse('poke:pokes'))
        else :
            for error in returnVal['errors'] :
                print error
                messages.error(request,error['message'],extra_tags=error['extra_tags'])
            return redirect(reverse("poke:home"))

def login (request):
    if request.method == "POST":
        returnVal = Users.objects.login(request.POST)
        if returnVal['user']:
            request.session['logged_in_user'] = returnVal['user'].id
            print "logged in user: ",request.session['logged_in_user']
            return redirect(reverse('poke:pokes'))
        else:
            for error in returnVal['errors'] :
                print error
                messages.error(request,error['message'],extra_tags=error['extra_tags'])
            return redirect(reverse('poke:home'))

def logout (request) :
    request.session.flush()
    return redirect(reverse('poke:home'))

def pokes(request):

    numPeople = 0
    user = __getLoggedUser(request)
    user_name = user.name
    print "user name: ", user_name

    # Get my pokers
    myPokerHistory = Pokes.objects.filter(receiver = user).order_by('-numPokesByPoker')
    numPeople = len(myPokerHistory)
    print myPokerHistory

    # Get other users that I can poke
    users = Users.objects.filter(~Q(id = user.id))
    print users
    context = {
        'numPeople' : numPeople,
        'user_name': user_name,
        'users' : users,
        'history' : myPokerHistory
    } 
    return render(request, 'pokeApp/pokes.html', context)

def pokeUser(request, userId) :

    if request.method == "POST":
        Pokes.objects.pokeUser(userId, request.session['logged_in_user'])

    return redirect(reverse('poke:pokes'))

# Private functions

def __getLoggedUser(request): 
    user = None
    id = request.session['logged_in_user']
    try:
        user = Users.objects.get(pk=id)
        return user
    except Users.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'You are not logged in. Please log in to continue')
        print "Not logged in"
        return redirect(reverse('wishList:home'))
    return user