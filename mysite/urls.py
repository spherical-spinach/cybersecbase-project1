from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(template_name='polls/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='polls:index'), name='logout'),
]