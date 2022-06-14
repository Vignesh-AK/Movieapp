from django.contrib import admin

from movies.models import Movies, User

# Register your models here.
admin.site.register(Movies)
admin.site.register(User)
