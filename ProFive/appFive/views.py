from django.shortcuts import render
from appFive.forms import UserProfileInfoForm, UserForm

#
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout



# Create your views here.
def index(request):
    return render(request, 'appFive/index.html')

@login_required
def special(request):
    return HttpResponse("You're logged in, Nice!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False

    if request.method =='POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            
            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)
            # Update with the Hashed password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pics' in request.FILES:
                profile.profile_pics = request.FILES['profile_pics']

            # Now save the model
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'appFive/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("<strong>ACCOUNT NOT ACTIVE</strong>")

        else: 
            print('<strong>Someone tried to login and failed!</strong>')
            print('Username: {} and password {}'.format(username, password))
            return HttpResponse("<strong> Invalid login details supplied!</strong>")

    else:
        return render(request, 'appFive/login.html', {})