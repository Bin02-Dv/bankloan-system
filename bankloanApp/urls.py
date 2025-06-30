from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_loan, name="get-loan"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('signout/', views.signout, name="signout"),
]
