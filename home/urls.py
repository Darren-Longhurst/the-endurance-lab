from django.urls import path
from . import views
from products.views import top_rated_products

urlpatterns = [
    path('', views.index, name='home'),
    path('top-rated/', top_rated_products, name='top_rated'),
    path('contact/', views.contact, name='contact'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),

    # Exception Message Templates Testing

    path(
        '403-test/',
        views.Force403View.as_view(),
        name='403-test'
    ),
    path(
        '404-test/',
        views.Force404View.as_view(),
        name='404-test'
    ),
    path(
        '405-test/',
        views.Force405View.as_view(),
        name='405-test'
    ),
    path(
        '500-test/',
        views.Force500View.as_view(),
        name='500-test'
    ),
]
