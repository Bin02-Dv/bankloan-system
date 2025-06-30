from django.shortcuts import render, redirect
import requests
import json
import logging
from django.http import JsonResponse
from .models import Loan
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def signout(request):
    auth.logout(request)
    return redirect('/signin')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return JsonResponse({'success': True, 'message': 'Signingin......'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid Signin Credentials!!'})
    return render(request, "signin.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "success": False, "message": "Username already exist!!"
            })
        elif confirm_password != password:
            return JsonResponse({
                "success": False, "message": "password and confirm password missed match!!"
            })
        else:
            User.objects.create_user(username=username, password=password)
            return JsonResponse({
                "success": True, "message": "Account has been created.."
            })
    return render(request, "signup.html")

def get_loan(request):
    if request.method == 'POST':
        
        current_user = request.user
        
        dependents = int(request.POST["dependents"])
        applicant_income = float(request.POST["applicant_income"])
        co_applicant_income = float(request.POST["co_applicant_income"])
        loan_amount = float(request.POST["loan_amount"])
        loan_amount_term = int(request.POST["loan_term"])
        credit_history = int(request.POST["credit_history"])
        gender = request.POST["gender"]
        marital = request.POST["marital"]
        education = request.POST["education"]
        employed = request.POST["employed"]
        area = request.POST["area"]
        name = request.POST["name"]

        # Convert categorical variables to numerical values
        gender_male = 1 if gender == 'Male' else 0
        gender_female = 1 if gender == 'Female' else 0

        marital_yes = 1 if marital == 'Yes' else 0
        marital_no = 1 if marital == 'No' else 0

        education_graduate = 1 if education == 'Graduate' else 0
        education_not_graduate = 1 if education == 'Not Graduate' else 0

        employed_yes = 1 if employed == 'Yes' else 0
        employed_no = 1 if employed == 'No' else 0

        area_rural = 1 if area == 'Rural' else 0
        area_semiurban = 1 if area == 'Semiurban' else 0
        area_urban = 1 if area == 'Urban' else 0


        url = 'https://9eb0-34-85-184-69.ngrok-free.app/predict'

        data = {
            "Dependants": dependents,
            "ApplicantIncome": applicant_income,
            "CoapplicantIncome": co_applicant_income,
            "LoanAmount": loan_amount,
            "Loan_Amount_Term": loan_amount_term,
            "Credit_History": credit_history,
            "Gender_Female": gender_female,
            "Gender_Male": gender_male,
            "Married_No": marital_no,
            "Married_Yes": marital_yes,
            "Education_Graduate": education_graduate,
            "Education_Not Graduate": education_not_graduate,
            "Self_Employed_No": employed_no,
            "Self_Employed_Yes": employed_yes,
            "Property_Area_Rural": area_rural,
            "Property_Area_Semiurban": area_semiurban,
            "Property_Area_Urban": area_urban
        }

        response = requests.post(url, json=data)
        response_data = response.json()
        status = response_data.get("status")
        if status ==  True:
            new_loan = Loan.objects.create(
                name=name, loan_amount=loan_amount, loan_status='Approved', user=current_user
            )
            new_loan.save()
            model_response = 'Congratulations! Your Loan has been Approved..'
            return JsonResponse({'success': True, 'message': model_response})
        elif status == False:
            new_loan = Loan.objects.create(
                name=name, loan_amount=loan_amount, loan_status='Rejected!!'
            )
            new_loan.save()
            model_response = 'Sorry! Your Loan has been Rejected!!'
            return JsonResponse({'success': False, 'message': model_response})
    return render(request, 'index.html')

@login_required(login_url='/signin')
def dashboard(request):
    applications = Loan.objects.all().order_by('-id')
    approved = Loan.objects.filter(loan_status='Approved').count()
    rejected = Loan.objects.filter(loan_status='Rejected!!').count()
    apps = applications.count()
    current_user = request.user
    user_applications = Loan.objects.filter(user=current_user)
    context = {
        "apps": applications,
        "all": apps,
        "approved": approved,
        "rejected": rejected,
        "current_user": current_user,
        "user_applications": user_applications,
    }
    return render(request, "dashboard.html", context)
