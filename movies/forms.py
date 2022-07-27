from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Movies


# Create your views here.

User = get_user_model()

class NewUserForm(UserCreationForm):
    
    movies = forms.ModelMultipleChoiceField(queryset=Movies.objects.all(),widget=forms.CheckboxSelectMultiple)


    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "movies")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class UpdateUser(forms.ModelForm):
    movies = forms.ModelMultipleChoiceField(queryset=Movies.objects.all(),widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = User
        fields = ("movies",)

    def save(self, commit=True):
        user = super(UpdateUser, self).save(commit=False)
        if commit:
            user.save()
        return user

class AddMovies(forms.ModelForm):
   
    class Meta:
        model = Movies
        fields = '__all__'

