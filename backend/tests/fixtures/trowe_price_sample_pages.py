"""Synthetic page text modeled on a T. Rowe Price Portfolio Summary layout.

All names, account numbers, and dollar amounts here are fabricated -- this
fixture exists purely to exercise the parser's regexes against realistic line
shapes, without embedding anyone's real financial data in the repo.
"""

PAGE_1 = """January - December 2024
Portfolio Summary
T Rowe Price Trust Co
Cust For The Rollover IRA Of
Jane Q Sample
123 Fake Street
Sampleville KS 66061-0000
"""

PAGE_3_PORTFOLIO_VALUE = """January - December 2024
Portfolio Summary
Investor Number 999999999 Page 1 of 7
Mutual Fund Portfolio Value
As of 12/31/24 your total mutual fund portfolio value is $200,000.00.
Money Market Funds $6,000.00 3.0% $7,000.00 3.0% $1,000.00
Taxable 6,000.00 3.0 7,000.00 3.0 1,000.00
Tax - Free -- -- -- -- --
Bond Funds $18,000.00 9.0% $22,000.00 11.0% $4,000.00
Domestic – Taxable 14,000.00 7.0 18,000.00 9.0 4,000.00
Domestic – Tax-Free -- -- -- -- --
International/Global 4,000.00 2.0 4,000.00 2.0 0.00
Stock Funds $176,000.00 88.0% $171,000.00 86.0% -5,000.00
Domestic 118,000.00 59.0 113,000.00 57.0 -5,000.00
International/Global 58,000.00 29.0 58,000.00 29.0 0.00
Total Portfolio $200,000.00 100.0% $200,000.00 100.0% $0.00
"""

PAGE_5_INVESTMENT_STYLE = """January - December 2024
Portfolio Summary
Investor Number 999999999 Page 3 of 7
Investment Style Analysis
Retirement 2045 3.0 7.0 2.0 2.0 38.0 19.0 29.0
Total Portfolio 3.0% 7.0% 2.0% 2.0% 38.0% 19.0% 29.0% 0.0%
Retirement Monthly Income Estimator
Based on your current balance of $200,000.00.
Your estimated monthly retirement income is $1,750
Contributing an additional $150/month $1,900
Contributing an additional $300/month $2,050
"""

PAGE_6_ACTIVITY_AND_BENEFICIARIES = """January - December 2024
Portfolio Summary
Investor Number 999999999 Page 4 of 7
Activity Summary by Fund Beneficiary Information
T. Rowe Price Retirement 2045
Account Number: 1234567890 - 1
T Rowe Price Trust Co
Cust For The Rollover IRA Of
Jane Q Sample
All Accounts
12/31/23
Value Additions Deductions Income
Market
Fluctuation
12/31/24
Value
Blended Funds
Retirement 2045 $180,000.00 $0.00 $0.00 $5,000.00 $15,000.00 $200,000.00
Total Portfolio $180,000.00 $0.00 $0.00 $5,000.00 $15,000.00 $200,000.00
Primary: John Q Sample 100%
Secondary: Alex R Sample 50% Casey T Sample 50%
"""


def get_sample_pages() -> list[str]:
    return [
        PAGE_1,
        PAGE_3_PORTFOLIO_VALUE,
        PAGE_5_INVESTMENT_STYLE,
        PAGE_6_ACTIVITY_AND_BENEFICIARIES,
    ]
