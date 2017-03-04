from django.shortcuts import render, redirect, HttpResponse
from models import User, Quote, Fav
from django.contrib import messages
from django.db.models import Count
# import datetime

def index(request):
	return render(request,'main.html')

def main(request):
	return render(request,'main.html')


def display(request):
    quote_list = Quote.objects.all()
    user_list = User.objects.all()
    fav_list = Fav.objects.all()
    context = {
        'quote_list': quote_list,
        'user_list': user_list,
        'fav_list': fav_list
    }
    return render(request, 'display.html', context)
    

def register(request):
    if request.method == "POST":
        user = User.objects.register(request.POST)
        if 'errors' in user:
            for error in user['errors']:
                messages.error(request, error)
            return redirect('/')
        if 'theuser' in user:
            request.session['theuser'] = user['theuser']
            request.session['alias'] = user['alias']
            request.session['userid'] = user['userid']
            return redirect('/quotes')

def login(request):
    if request.method == "POST":
        user = User.objects.login(request.POST)
        if 'errors' in user:
            for error in user['errors']:
                messages.error(request, error)
            return redirect('/')
        if 'theuser' in user:
            request.session['theuser'] = user['theuser']
            request.session['alias'] = user['alias']
            request.session['userid'] = user['userid']
            return redirect('/quotes')


def quotes(request):
	alluser = User.objects.all()
	all_favs = Fav.objects.all()#.exclude(fav_quote__id = request.session['userid'])#.filter(fav_user__id = request.session['userid'])
	others_list = Quote.objects.all().exclude(user__id = request.session['userid']) #.exclude(join__id = request.session['userid'])
	context = {
		'quote_list':others_list,
		'fav_list':all_favs,
		'alluser':alluser
	}
	return render(request, 'quotes.html', context)

def add_quote(request):
	if request.method == "POST":
		new_quote = Quote.objects.add_quote(request.POST, request.session['userid'])
		if 'errors' in new_quote:
			for error in new_quote['errors']:
				messages.error(request, error)
			return redirect('/quotes')
		else:
			return redirect('/quotes')


def user_gen(request,id):
	stuff = User.objects.get(id=id)
	context = {
	'user': stuff,
	'quote': Quote.objects.filter(user=stuff)
	}
	context['total_reviews']=Quote.objects.annotate(count=Count('quote')).filter(user__id=context['user'].id)
	return render(request, 'users.html', context)

def add_fav(request,id):
	user = User.objects.get(id=request.session['userid'])
	favquote = Quote.objects.get(id = id)
	print favquote.id
	Fav.objects.create(fav_user=user, fav_quote=favquote)
	return redirect('/quotes')


# def add_friend(request,id): 
# 	user = User.objects.get(id=request.session['userid'])#user is grabbing the current users id. 
# 	print user.id 
# 	newfriend = User.objects.get(id =id ) # grab the id of who you want to add as friend.
# 	print newfriend.id 
# 	Friend.objects.create(users=user, friends=newfriend)
# 	return redirect('/friends')


 # trip =Trip.objects.get(id=id) # trip is holding the id of the trip that you clicked.
 #    print trip.id
 #    user = User.objects.get(id = request.session['userid']) # is holding the id of the current user.
 #    trip.join.add(user) # using the forgein key to take the trip id and add your user id to it. 
 #    return redirect('/travels')

def delete(request, id):
    Fav.objects.get(id=id).delete()
    return redirect('/quotes')


def logout(request):
    del request.session['theuser']
    del request.session['alias']
    del request.session['userid']
    return redirect('/')


