from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_loan, name="get-loan")
]
