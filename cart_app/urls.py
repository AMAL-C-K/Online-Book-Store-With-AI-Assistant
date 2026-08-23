from django.urls import path
from . import views
urlpatterns = [
    
    path('', views.cart, name='cart'),
    path('add/<int:book_id>/', views.add_to_cart, name='add'),
    path('plus/<int:cart_id>/', views.quantity_plus, name='plus'),
    path('minus/<int:cart_id>/', views.quantity_minus, name='minus'),
    path('remove/<int:cart_id>/', views.remove, name='remove')
]
