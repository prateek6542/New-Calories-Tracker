from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('log_meal/', views.log_meal, name='log_meal'),
    path('add_food_item/', views.add_food_item, name='add_food_item'),
    path('daily-log/', views.daily_log, name='daily_log'),
    path('delete-log/<int:log_id>/', views.delete_log, name='delete_log'),

]
