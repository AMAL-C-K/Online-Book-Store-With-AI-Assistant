from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register_view, name = 'register'),
    path('signin/', views.signin_view, name='signin'),
    path('logout/', views.logout_view, name='logout')
]
