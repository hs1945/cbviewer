import requests
from pycrunchbase.resource import (
    Acquisition,
    FundingRound,
    FundRaise,
    IPO,
    Organization,
    Page,
    Person,
    Product,
)

final_url = 'https://api.crunchbase.com/v/2/organization/facebook?user_key=844895ab00a3e40cf2c92dd3c2b8409d'
response = requests.get(final_url)
response.raise_for_status()
data = response.json().get('data')
print(response.json().get('data'))
print type(Organization(data).funding_rounds)
