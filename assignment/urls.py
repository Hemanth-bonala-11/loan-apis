from django.urls import path, include
from assignment import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'customer', views.CustomerViewset)
router.register(r'loan', views.LoanViewset)

urlpatterns = [
    path('register', views.Register.as_view(), name="register "),
    path('check-eligibility', views.Register.as_view(), name="check-eligibility"),
    path('create-loan', views.CreateLoan.as_view(), name="create-loan"),
    path('view-loan/<int:loan_id>', views.ViewLoan.as_view(), name="view-loan"),
    path('view-loans/<int:customer_id>', views.ViewCustomer.as_view(), name="view-customer")


]
