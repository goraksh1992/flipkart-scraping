from django.urls import path
from .views import home, addCategory

urlpatterns = [
    path('', home, name="home"),
    path('add-category', addCategory, name="add-category"),
]