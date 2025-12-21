from django.urls import path
from . import views

urlpatterns = [
    path('my-affirmations/', views.my_affirmations, name='my_affirmations'),
    path('api/affirmation/', views.affirmation_api, name='affirmation_api'),
]
