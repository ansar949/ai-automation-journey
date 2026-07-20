"""DSCR Investment Property Analyzer.

A beginner-friendly real estate finance project for evaluating rental property
loan scenarios. This version uses only the Python standard library.
"""

from dataclasses import dataclass


@dataclass
class DealInputs:
    purchase_price: float
    loan_amount: float
    annual_interest_rate: float
    loan_term_years: int
    monthly_rent: float
    monthly_expenses: float
    annual_taxes: float
    annual_insurance: float


def annual_debt_service(loan_amount: float, annual_rate: float, years: int) -> float:
    """Return annual principal-and-interest debt service for an amortizing loan."""
    monthly_rate = annual_rate / 100 / 12
    payments = years * 12

    if monthly_rate == 0:
        monthly_payment = loan_amount / payments
    else:
        monthly_payment = loan_amount * (
            monthly_rate * (1 + monthly_rate) ** payments
        ) / ((1 + monthly_rate) ** payments - 1)

    return monthly_payment * 12


def analyze_deal(deal: DealInputs) -> dict[str, float]:
    gross_income = deal.monthly_rent * 12
    operating_expenses = (
        deal.monthly_expenses * 12 + deal.annual_taxes + deal.annual_insurance
    )
    noi = gross_income - operating_expenses
    debt_service = annual_debt_service(
        deal.loan_amount, deal.annual_interest_rate, deal.loan_term_years
    )

    dscr = noi / debt_service if debt_service else 0
    ltv = deal.loan_amount / deal.purchase_price if deal.purchase_price else 0
    cap_rate = noi / deal.purchase_price if deal.purchase_price else 0
    annual_cash_flow = noi - debt_service

    return {
        "gross_income": gross_income,
        "operating_expenses": operating_expenses,
        "noi": noi,
        "annual_debt_service": debt_service,
        "dscr": dscr,
        "ltv": ltv,
        "cap_rate": cap_rate,
        "annual_cash_flow": annual_cash_flow,
    }


def money(value: float) -> str:
    return f"${value:,.2f}"


def main() -> None:
    print("DSCR Investment Property Analyzer")
    print("-" * 36)

    deal = DealInputs(
        purchase_price=float(input("Purchase price: $")),
        loan_amount=float(input("Loan amount: $")),
        annual_interest_rate=float(input("Interest rate (%): ")),
        loan_term_years=int(input("Loan term (years): ")),
        monthly_rent=float(input("Monthly rent: $")),
        monthly_expenses=float(input("Other monthly operating expenses: $")),
        annual_taxes=float(input("Annual property taxes: $")),
        annual_insurance=float(input("Annual insurance: $")),
    )

    result = analyze_deal(deal)

    print("\nDeal Analysis")
    print("-" * 36)
    print(f"Gross annual income:      {money(result['gross_income'])}")
    print(f"Operating expenses:      {money(result['operating_expenses'])}")
    print(f"Net operating income:    {money(result['noi'])}")
    print(f"Annual debt service:     {money(result['annual_debt_service'])}")
    print(f"Annual cash flow:         {money(result['annual_cash_flow'])}")
    print(f"DSCR:                     {result['dscr']:.2f}x")
    print(f"LTV:                      {result['ltv']:.1%}")
    print(f"Cap rate:                 {result['cap_rate']:.2%}")


if __name__ == "__main__":
    main()
