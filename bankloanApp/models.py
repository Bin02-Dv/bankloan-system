from django.db import models
from django.contrib.auth.models import User

# Create your models here.

user = User()

class Loan(models.Model):
    name = models.CharField(max_length=225)
    loan_amount = models.CharField(max_length=225)
    loan_status = models.CharField(max_length=225)
    user = models.ForeignKey(user, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
