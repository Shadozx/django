from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home_page"),
    path('delete/<city_id>', views.delete_city, name="delete_city"),
    path('filter_cities', views.filter_cities, name="filter_cities"),
    path('choose/', views.choose, name="choose")
]