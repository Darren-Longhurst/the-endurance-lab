from django.urls import path
from . import views
from products.views import top_rated_products

urlpatterns = [
    path('', views.index, name='home'),
    path('top-rated/', top_rated_products, name='top_rated'),
    path('contact/', views.contact, name='contact'),
]
