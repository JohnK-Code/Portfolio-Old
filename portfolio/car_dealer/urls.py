from django.urls import path
from .views import *

app_name = 'car_dealer'
urlpatterns = [
    path('', index, name='index'),
    path('make', formMakeModel, name="make_model"),
    path('showroom', showroom, name="showroom"),
    path('showroom-search', showroom_search, name="show_search"),
    path('car/<int:id>', car, name="car")
]
