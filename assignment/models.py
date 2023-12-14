from django.db import models
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message="Phone number must be entered in the format: '987654321'. Up to 15 digits allowed.",
)

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, unique=True
    )
    age = models.IntegerField()
    monthly_salary = models.IntegerField()
    approved_limit = models.BigIntegerField()
    current_debt = models.BigIntegerField(null=True, blank=True)

class Loan(models.Model):
    customer_id = models.IntegerField()
    loan_amount = models.BigIntegerField()
    tenure = models.IntegerField()
    interest_rate = models.FloatField()
    monthly_payment = models.IntegerField(verbose_name="monthly repayment (emi)")
    emis_paid_on_time = models.IntegerField(verbose_name="EMIs paid on time")
    start_date = models.DateField(verbose_name="Date of Approval")
    end_date = models.DateField()




# Create your models here.
