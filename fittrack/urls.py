from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('log_workout/',views.log_workout,name='log_workout'),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('register',views.register,name='register'),
    path('workout_history',views.workout_history,name='workout_history'),
    path('protein_calculator',views.protein_cal,name='protein_cal'),
    path('calaroies_count',views.cal_count, name='cal_count'),
]