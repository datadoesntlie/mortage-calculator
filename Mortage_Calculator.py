import streamlit as st
import pandas as pd

st.title("Manny's Mortgage Magic ✨")
st.write("Welcome to your friendly mortgage calculator! 🏡💰 Let's find the best way for you to finance your dream home!")

# User choice for calculation method
calculation_method = st.radio(
    "How would you like to calculate your mortgage?",
    ('By Monthly Payment', 'By Property Value')
)

if calculation_method == 'By Monthly Payment':
    # Inputs for calculating based on desired monthly payment
    desired_monthly_payment = st.number_input(
        "💵 Enter your desired monthly payment ($):",
        min_value=100, max_value=10000, value=1500, step=100,
        key="desired_monthly_payment"
    )
    interest_rate_mp = st.number_input(
        "💸 Enter the interest rate (%):",
        min_value=0.00, max_value=20.00, value=3.5, step=0.05,
        key="interest_rate_mp"
    )
    initial_deposit_mp = st.number_input(
        "💼 Enter your initial deposit ($):",
        min_value=0, value=60000, step=1000,
        key="initial_deposit_mp"
    )
    mortgage_length_mp = st.number_input(
        "⏳ Enter the length of the mortgage (years):",
        min_value=5, max_value=35, value=30, step=1,
        key="mortgage_length_mp"
    )
    # Monthly interest rate
    monthly_interest_rate = (interest_rate_mp / 100) / 12
    # Total number of payments
    total_payments = mortgage_length_mp * 12
    
    # Calculate maximum loan amount based on desired monthly payment
    if monthly_interest_rate > 0:
        max_loan_amount = desired_monthly_payment * ((1 - (1 + monthly_interest_rate) ** -total_payments) / monthly_interest_rate)
    else:
        max_loan_amount = desired_monthly_payment * total_payments
    
    # Calculate maximum property value
    property_value = max_loan_amount + initial_deposit_mp
    loan_value = property_value - initial_deposit_mp

    # Calculating monthly payment and total amount
    monthly_interest_rate = (interest_rate_mp / 100) / 12
    total_payments = mortgage_length_mp * 12

    # Ensure we don't divide by zero in case of 0% interest rate
    if monthly_interest_rate > 0:
        desired_monthly_payment = loan_value * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
    else:
        desired_monthly_payment = loan_value / total_payments

    total_amount_paid = desired_monthly_payment * total_payments
    
    st.write(f"🏠 With your inputs, the maximum property value you can afford is: ${property_value:,.2f}")
    st.write(f"🔍 The loan amount after the initial deposit is: ${loan_value:,.2f}")
    st.write(f"💰 Total amount paid over the life of the mortgage: ${total_amount_paid:,.2f}")

elif calculation_method == 'By Property Value':
    # Inputs for calculating based on property value
    property_value = st.slider(
        "🏠 Select the value of the property:",
        min_value=120000, max_value=1200000, value=500000, step=50000,
        key="property_value"
    )
    interest_rate_pv = st.number_input(
        "💸 Enter the interest rate (%):",
        min_value=0.00, max_value=20.00, value=3.5, step=0.05,
        key="interest_rate_pv"
    )
    initial_deposit_pv = st.number_input(
        "💼 Enter your initial deposit ($):",
        min_value=0, max_value=property_value, value=60000, step=1000,
        key="initial_deposit_pv"
    )
    mortgage_length_pv = st.number_input(
        "⏳ Enter the length of the mortgage (years):",
        min_value=5, max_value=40, value=30, step=1,
        key="mortgage_length_pv"
    )
    # Calculating the loan value
    loan_value = property_value - initial_deposit_pv
    # Display the calculated loan value
    st.write("🔍 The loan amount after the initial deposit is: ${:,.0f}".format(loan_value))
    # Calculating monthly payment and total amount
    monthly_interest_rate = (interest_rate_pv / 100) / 12
    total_payments = mortgage_length_pv * 12

    # Ensure we don't divide by zero in case of 0% interest rate
    if monthly_interest_rate > 0:
        monthly_payment = loan_value * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
    else:
        monthly_payment = loan_value / total_payments

    total_amount_paid = monthly_payment * total_payments

    # Display the monthly payment and total amount paid
    st.write(f"📅 Your estimated monthly payment: ${monthly_payment:,.2f}")
    st.write(f"💰 Total amount paid over the life of the mortgage: ${total_amount_paid:,.2f}")

    # Preparing data for the bar chart
    remaining_balance = loan_value
    monthly_interest_rate = (interest_rate_pv / 100) / 12
    total_payments = mortgage_length_pv * 12

    monthly_data = []

    for month in range(1, total_payments + 1):
        interest_for_month = remaining_balance * monthly_interest_rate
        principal_for_month = monthly_payment - interest_for_month
        remaining_balance -= principal_for_month
        
        monthly_data.append({
            "Month": month,
            "Principal": principal_for_month,
            "Interest": interest_for_month,
        })

    df_payments = pd.DataFrame(monthly_data).set_index("Month")

    # Displaying the stacked bar chart
    st.write("📊 Here's how your payments break down over time:")
    st.bar_chart(df_payments)