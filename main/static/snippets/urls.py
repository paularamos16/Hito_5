from django.urls import path
from main.views import index, about, contact, prices, ayuda, success, welcome, pruebas, suscriptions, registerfree, registerpremium, registerdiamond

urlpatterns = [
    path('', index),
    path('about/', about),
    path('contact/', contact),
    path('prices/', prices),
    path('ayuda/', ayuda),
    path('success/', success),    
    path('welcome/', welcome),    
    path('pruebas/', pruebas, name='pruebas' ),
    path('suscriptions/', suscriptions, name ='suscriptions'),
    path('registerfree/', registerfree, name ='registerfree'),
    path('registerpremium/', registerpremium, name ='registerpremium'),
    path('registerdiamond/', registerdiamond, name ='registerdiamond'),
] 