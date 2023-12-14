from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from datetime import datetime, timedelta
from .utils import *
from dateutil.relativedelta import relativedelta

class CustomerViewset(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
class LoanViewset(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class Register(CustomerViewset):

    def post(self, request):
        data = request.data
        if data:
            try:
                first_name = data["first_name"]
                last_name = data["last_name"]
                age = data["age"]
                monthly_income = data["monthly_income"]
                phone_number = data["phone_number"]
                approved_limit = 36 * monthly_income

                customer = Customer(first_name=first_name, last_name=last_name, monthly_salary=monthly_income,
                         phone_number=phone_number,
                         approved_limit=approved_limit)
                customer.save()

                return Response({
                    "customer_id": customer.id,
                    "name": customer.first_name+customer.last_name,
                    "age": age,
                    "monthly_income": customer.monthly_salary,
                    "approved_limit": customer.approved_limit,
                    "phone_number": customer.phone_number
                },
                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST)


        else:
            return Response({
                "message": "No Data"
            },
            status=status.HTTP_400_BAD_REQUEST)

class CheckEligibility(generics.ListAPIView):

    def post(self,request):
        data = request.data
        if data:
            try:
                customer_id = data["customer_id"]
                loan_amount = data["loan_amount"]
                interest_rate = data["interest_rate"]
                tenure = data["tenure"]
                customer = Customer.objects.get(pk=customer_id)
                loans = Loan.objects.filter(customer_id=customer_id)
                current_loans_sum = 0
                emis_paid_on_time = 0
                total_months = 0
                no_of_loans = 0
                current_year_activity = 0
                total_emi = 0
                for loan in loans.iterator():
                    no_of_loans += 1
                    current_loans_sum += loan.loan_amount
                    emis_paid_on_time += loan.emis_paid_on_time
                    temp_months = (loan.end_date.year - loan.start_date.year)*12 + (loan.end_date.month - loan.start_date.month)
                    total_months += temp_months
                    total_emi += loan.monthly_payment

                    if loan.start_date.year == datetime.now().year:
                        current_year_activity = 1

                data["current_loans_sum"] = current_loans_sum
                data["emis_paid_on_time"] = emis_paid_on_time
                data["total_months"] = total_months
                data["approved_limit"] = customer.approved_limit
                data["no_of_loans"] = no_of_loans
                data["toal_monthly_emi"] = total_emi
                data["salary"] = customer.monthly_salary
                credit_score = calculate_credit_score(data)
                approval = False
                corrected_interest_rate = False

                if credit_score > 50:
                    approval = True
                elif credit_score >30:
                    approval = True
                    corrected_interest_rate = 12
                elif credit_score > 10:
                    approval = True
                    corrected_interest_rate = 16
                else:
                    approval = False

                if corrected_interest_rate :
                    monthly_installment = (loan_amount * corrected_interest_rate * (1+corrected_interest_rate)**tenure)// (1+corrected_interest_rate)**(tenure-1)
                    return Response({
                        "customer_id": customer_id,
                        "approval": approval,
                        "interest_rate": interest_rate,
                        "corrected_interest_rate": corrected_interest_rate,
                        "tenure": tenure,
                        "monthly_installment": monthly_installment
                    },
                        status=status.HTTP_200_OK)
                monthly_installment = (loan_amount * interest_rate * (
                            1 + interest_rate) ** tenure) // (1 + interest_rate) ** (tenure - 1)
                return Response({
                    "customer_id": customer_id,
                    "approval": approval,
                    "interest_rate": interest_rate,
                    "tenure": tenure,
                    "monthly_installment": monthly_installment
                },
                    status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "No Data"
            },
                status=status.HTTP_400_BAD_REQUEST)


class CreateLoan(generics.ListAPIView):

    def post(self, request):
        data = request.data
        if data:
            try:
                customer_id = data["customer_id"]
                loan_amount = data["loan_amount"]
                interest_rate = data["interest_rate"]
                tenure = data["tenure"]
                customer = Customer.objects.get(pk=customer_id)
                loans = Loan.objects.filter(customer_id=customer_id)
                current_loans_sum = 0
                emis_paid_on_time = 0
                total_months = 0
                no_of_loans = 0
                current_year_activity = 0
                total_emi = 0
                for loan in loans.iterator():
                    no_of_loans += 1
                    current_loans_sum += loan.loan_amount
                    emis_paid_on_time += loan.emis_paid_on_time
                    temp_months = (loan.end_date.year - loan.start_date.year) * 12 + (
                                loan.end_date.month - loan.start_date.month)
                    total_months += temp_months
                    total_emi += loan.monthly_payment

                    if loan.start_date.year == datetime.now().year:
                        current_year_activity = 1

                data["current_loans_sum"] = current_loans_sum
                data["emis_paid_on_time"] = emis_paid_on_time
                data["total_months"] = total_months
                data["approved_limit"] = customer.approved_limit
                data["no_of_loans"] = no_of_loans
                data["toal_monthly_emi"] = total_emi
                data["salary"] = customer.monthly_salary
                credit_score = calculate_credit_score(data)
                approval = False
                corrected_interest_rate = False

                if credit_score > 50:
                    approval = True
                elif credit_score > 30:
                    approval = True
                    corrected_interest_rate = 12
                elif credit_score > 10:
                    approval = True
                    corrected_interest_rate = 16
                else:
                    approval = False

                if approval:
                    if corrected_interest_rate:

                        monthly_installment = (loan_amount * corrected_interest_rate * (
                                    1 + corrected_interest_rate) ** tenure) // (1 + corrected_interest_rate) ** (tenure - 1)
                        loan = Loan(customer_id=customer_id, loan_amount=loan_amount, tenure=tenure,
                             interest_rate=corrected_interest_rate,
                             monthly_payment=monthly_installment,
                             emis_paid_on_time=emis_paid_on_time,
                             start_date=datetime.now().strftime("%d-%m-%y"),
                             end_date=(datetime.now() + relativedelta(months=tenure)).strftime('%d-%m-%y')
                             )
                        loan.save()

                        return Response({
                            "loan_id": loan.id,
                            "customer_id": customer_id,
                            "loan_approved": approval,
                            "message": "your loan has been sanctioned",
                            "monthly_installment": monthly_installment
                        },
                            status=status.HTTP_200_OK)
                    monthly_installment = (loan_amount * interest_rate * (
                            1 + interest_rate) ** tenure) // (1 + interest_rate) ** (tenure - 1)
                    loan = Loan(customer_id=customer_id, loan_amount=loan_amount, tenure=tenure,
                                interest_rate=interest_rate,
                                monthly_payment=monthly_installment,
                                emis_paid_on_time=emis_paid_on_time,
                                start_date=datetime.now().strftime("%d-%m-%y"),
                                end_date=(datetime.now() + relativedelta(months=tenure)).strftime('%d-%m-%y')
                                )
                    loan.save()
                    return Response({
                        "customer_id": customer_id,
                        "loan_id": loan.id,
                        "loan_approved": approval,
                        "message": "your loan has been sanctioned",
                        "monthly_installment": monthly_installment
                    },
                        status=status.HTTP_200_OK)
                else:
                    return Response({
                        "customer_id": customer_id,
                        "loan_id": None,
                        "loan_approved": approval,
                        "message": "your loan has been rejected due to your low credit score",
                        "monthly_installment": None

                    },
                        status=status.HTTP_200_OK)


            except Exception as e:
                return Response({
                    "error": str(e)
                },
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {
                "message": "No Data"
            },
            status=status.HTTP_400_BAD_REQUEST)

class ViewLoan(generics.ListAPIView):
    def post(self,request,loan_id):
        response = {}
        loan = Loan.objects.get(pk=loan_id)
        customer_id = loan.customer_id
        customer = Customer.objects.get(pk=customer_id)
        customer_serializer = CustomerRequiredSerializer(customer)
        response["customer"] = customer_serializer.data
        response["loan_id"] = loan_id


        if loan:
            response["approval"] = True
            response["interest_rate"] = loan.interest_rate
            response["monthly_installment"] = loan.monthly_payment
            response["tenure"] = loan.tenure

            return  Response(response,
                             status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "no loan object is present with this loan id"
            },
            status=status.HTTP_404_NOT_FOUND)

class ViewCustomer(generics.ListAPIView):
    def post(self,request,customer_id):
        customer = Customer.objects.get(pk=customer_id)
        if customer:
            loans = Loan.objects.filter(customer_id=customer_id)

        else:
            return Response({
                "message": "no customer object is present with this customer id"
            },
            status=status.HTTP_404_NOT_FOUND)




