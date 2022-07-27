from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("accounts/login/", views.login_request, name="login"),
    path("accounts/register", views.register_request, name="register"),
    path("logout", views.logout_request, name= "logout"),
    path("users", views.users_list, name= "users_list"),
    path("add_movies", views.add_movies, name= "add_movies"),
    path("update_user/<str:username>", views.update_user, name="update")

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)