from django.contrib.messages.api import error
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Quote, User
import bcrypt

def index(request):
    return render(request, "index.html")

def register_user(request):
    errors = User.objects.validator_registration(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        User.objects.create(
            first_name = request.POST['first_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = user.id
        request.session['user_email'] = user.email
        request.session['greeting'] = user.first_name
        # messages.info(request, "User registered; log in now")
        messages.error(request, "Success")
        return redirect('/success')

def login_user(request):


    if request.method =='GET':
        return redirect('/')

    errors = User.objects.validator_login(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = user.id
        request.session['user_email'] = user.email
        request.session['greeting'] = user.first_name
        
        return redirect('/quotes')

def logout(request):
    del request.session['user_id']
    del request.session['user_email']
    return redirect('/')



def success(request):
    # error= User.objects.
    if 'user_id'in request.session:
    
        user = User.objects.get(id= request.session['user_id'])
        context={
            'user': user
        }
        return render(request, 'success.html', context)
    else:
        messages.error(request, "Sorry, you are not logged in!")
        return redirect('/')





def main(request):
    if 'user_id' in request.session:
        context={
            'quotes': Quote.objects.all(),
            'user': User.objects.get(id= request.session['user_id'])
        }
        return render(request,'quotes.html',context)
    else:
        messages.error(request, "Sorry, you are not logged in!")
        return redirect('/')


def create_quote(request):
    if 'user_id' not in request.session:
        return redirect('/')

    if request.method =="GET":
        return redirect('/quotes')
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors)>0:
        for key, vlaue in errors.items():
            messages.error(request,vlaue)
        return redirect('/quotes')
    
    #create a quote
    user = User.objects.get(id=request.session['user_id'])
    Quote.objects.create(
        quoted_by = request.POST['quoted_by'],
        quote = request.POST['quote'],
        user = user
    )
    return redirect('/quotes')

def user_profile(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id= user_id)
    context = {
        'user': user
    }
    return render(request, 'user_profile.html', context)

def render_edit(request, quote_id ):
    if 'user_id' not in request.session:
        return redirect('/')
    quote = Quote.objects.get(id = quote_id)
    context={
        'quote' :quote 
    }
    return render(request, 'render_edit.html', context)


def process_edit(request, quote_id):
    if request.method =="GET":
        return redirect('/quotes')
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors)>0:
        for key, vlaue in errors.items():
            messages.error(request,vlaue)
        return redirect(f'/quotes/{quote_id}')

    #create a quote
    user = User.objects.get(id=request.session['user_id'])
    quote_to_update = Quote.objects.get(id=quote_id)
    quote_to_update.quoted_by = request.POST['quoted_by']
    quote_to_update.quote = request.POST['quote']
    quote_to_update.save()


    return redirect('/quotes')


def process_delete(request, quote_id ):
    quote_to_delete = Quote.objects.get(id=quote_id)
    quote_to_delete.delete()
    return redirect('/quotes')


def favorit(request, quote_id):
    user = User.objects.get(id= request.session['user_id'])
    quote = Quote.objects.get(id=quote_id)
    user.user_favorit_quoptes.add(quote)
    return redirect('/quotes')



def unfavorit(request, quote_id):
    user = User.objects.get(id= request.session['user_id'])
    quote = Quote.objects.get(id=quote_id)
    user.user_favorit_quoptes.remove(quote)
    return redirect('/quotes')