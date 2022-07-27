from django.shortcuts import  get_object_or_404, render, redirect
from .forms import AddMovies, NewUserForm, UpdateUser
from .models import Movies
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate #add this
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.db.models import Count


User = get_user_model()
def check_admin(user):
   
    return user.is_superuser


@user_passes_test(check_admin)
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            movies = form.cleaned_data['movies']
            user.movies.set(movies)
        
            messages.success(request, "Registration successful." )
           
            return redirect("/")
        messages.error(request, "Form is not valid")
        messages.error(request, form.errors)

    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("login")


@login_required(login_url="login")
def dashboard(request):
    if request.user.is_superuser:
        movies = Movies.objects.all()
    else:
        current_user = request.user
        movies = current_user.movies.all()
       
    return render(request=request, template_name="dashboard.html", context={"movies":movies})


@user_passes_test(check_admin)
def users_list(request):
    users = User.objects.annotate(q_count=Count('movies')).order_by('q_count')[:7]
    
    return render(request=request, template_name="user_list.html", context={"users":users})


@user_passes_test(check_admin)
def update_user(request,username):
    instance = get_object_or_404(User, username=username)
    if request.method == "POST":
        form = UpdateUser(request.POST, instance=instance)
        if form.is_valid():
            user = form.save()
            movies = form.cleaned_data['movies']
            user.movies.set(movies)
            messages.success(request, "Updation successful." )
            return redirect("/")
        messages.error(request, "Form is not valid")
    form = UpdateUser()
    return render (request=request, template_name="update.html", context={"update_user":form})

@user_passes_test(check_admin)
def add_movies(request):
    if request.method == 'POST':
        form = AddMovies(request.POST, request.FILES)

        if form.is_valid():
                movie = form.save()
                return redirect('dashboard')
    else:
        form = AddMovies()
    return render(request,'add_movies.html',context={'form': form})

  