import numpy as np

# Define tranches
tranches = {
    "A": {"balance": 500000, "interest_rate": 0.05, "priority": 1},
    "B": {"balance": 300000, "interest_rate": 0.07, "priority": 2},
    "C": {"balance": 200000, "interest_rate": 0.10, "priority": 3}  
}

# Monthly incoming cash flow
cash_inflow = 50000

def calculate_interest(tranches):
    """Calculates interest due for each tranche."""
    return {k: v["balance"] * v["interest_rate"] / 12 for k, v in tranches.items()}

def apply_cash_flow(cash, tranches):
    """Distributes cash flow in a waterfall structure."""
    remaining_cash = cash
    payments = {k: 0 for k in tranches.keys()}
    
    # Sort tranches by priority
    sorted_tranches = sorted(tranches.items(), key=lambda x: x[1]["priority"])
    
    # Step 1: Pay interest
    interest_due = calculate_interest(tranches)
    for tranche, details in sorted_tranches:
        if remaining_cash >= interest_due[tranche]:
            payments[tranche] += interest_due[tranche]
            remaining_cash -= interest_due[tranche]
        else:
            payments[tranche] += remaining_cash
            remaining_cash = 0
            break  # No more cash left
    
    # Step 2: Pay down principal (if cash remains)
    for tranche, details in sorted_tranches:
        if remaining_cash > 0 and tranches[tranche]["balance"] > 0:
            pay_amount = min(tranches[tranche]["balance"], remaining_cash)
            payments[tranche] += pay_amount
            tranches[tranche]["balance"] -= pay_amount
            remaining_cash -= pay_amount
    
    return payments, remaining_cash

# Run waterfall calculation
payments, remaining_cash = apply_cash_flow(cash_inflow, tranches)

# Print results
print("Cash Flow Waterfall Distribution:")
for tranche, amount in payments.items():
    print(f"Tranche {tranche}: ${amount:,.2f}")
print(f"Remaining cash after payments: ${remaining_cash:,.2f}")
