from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_loan, name="get-loan"),
    path('dashboard/', views.dashboard, name="dashboard"),
]
