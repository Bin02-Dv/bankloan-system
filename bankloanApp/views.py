from django.shortcuts import render
import requests
import json
import logging
from django.http import JsonResponse

# Create your views here.

def get_loan(request):
    if request.method == 'POST':
        
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


        url = 'http://192.168.0.163:8000/bankloanApi/api/send'

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
            model_response = 'Congratulations! Your Loan has been Approved..'
            return JsonResponse({'success': True, 'message': model_response})
        elif status == False:
            model_response = 'Sorry! Your Loan has been Rejected!!'
            return JsonResponse({'success': False, 'message': model_response})
    return render(request, 'index.html')
