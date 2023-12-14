def calculate_credit_score(loan_data):
    credit_score = 0
    no_of_loan = loan_data["no_of_loans"]
    emis_paid_on_time = loan_data["emis_paid_on_time"]
    total_months = loan_data["total_months"]
    approved_limit = loan_data["approved_limit"]
    average_limit = loan_data["average_limit"]
    current_loans_sum = loan_data["current_loans_sum"]
    current_year_activity = loan_data["current_year_activity"]
    total_monthly_emi = loan_data["toal_monthly_emi"]
    salary = loan_data["salary"]



    if no_of_loan > 1:
        credit_score += 20
    credit_score += (emis_paid_on_time//total_months)*20
    if not current_year_activity :
        credit_score += 20
    if current_loans_sum > approved_limit:
        credit_score = 0
    if total_monthly_emi > salary//2 :
        credit_score = 0

    return credit_score



