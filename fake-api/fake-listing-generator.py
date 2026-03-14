# Generate fake listings in the format of the real RentCast rental listings
# API so that we can test the app without using up our free API calls

# We can use faker to create more realistic data
from faker import Faker
from random import randrange

"""
Per the RentCase docs, a listing result should look something like this

{
    "id": "2005-Arborside-Dr,-Austin,-TX-78754",
    "formattedAddress": "2005 Arborside Dr, Austin, TX 78754",
    "addressLine1": "2005 Arborside Dr",
    "addressLine2": null,
    "city": "Austin",
    "state": "TX",
    "stateFips": "48",
    "zipCode": "78754",
    "county": "Travis",
    "countyFips": "453",
    "latitude": 30.35837,
    "longitude": -97.66508,
    "propertyType": "Single Family",
    "bedrooms": 3,
    "bathrooms": 2.5,
    "squareFootage": 1681,
    "lotSize": 4360,
    "yearBuilt": 2019,
    "hoa": {
      "fee": 45
    },
    "status": "Active",
    "price": 2200,
    "listingType": "Standard",
    "listedDate": "2024-09-18T00:00:00.000Z",
    "removedDate": null,
    "createdDate": "2024-09-19T00:00:00.000Z",
    "lastSeenDate": "2024-09-30T03:49:20.620Z",
    "daysOnMarket": 13,
    "mlsName": "CentralTexas",
    "mlsNumber": "556965",
    "listingAgent": {
      "name": "Zachary Barton",
      "phone": "5129948203",
      "email": "zak-barton@realtytexas.com",
      "website": "https://zak-barton.realtytexas.homes"
    },
    "listingOffice": {
      "name": "Realty Texas",
      "phone": "5124765348",
      "email": "sales@realtytexas.com",
      "website": "https://www.realtytexas.com"
    },
    "history": {
      "2024-09-18": {
        "event": "Rental Listing",
        "price": 2200,
        "listingType": "Standard",
        "listedDate": "2024-09-18T00:00:00.000Z",
        "removedDate": null,
        "daysOnMarket": 13
      }
    }
  },
"""

def gen_fake_listing():
    """ Generatese a fake listing JSON result based on the example above."""
    fkr = Faker()
    address = fkr.address()
    listing = {
        "id": address.replace(' ', '-'),
        "formattedAddress": address,
        "addressLine1": address.split('\n')[0],
        "addressLine2": None,
        "city": address.split('\n')[1].split(',')[0],
        "state": "TX",
        "stateFips": "48",
        "zipCode": "78754",
        "county": "Travis",
        "countyFips": "453",
        "latitude": 30.35837,
        "longitude": -97.66508,
        "propertyType": "Single Family",
        "bedrooms": 3,
        "bathrooms": 2.5,
        "squareFootage": 1681,
        "lotSize": 4360,
        "yearBuilt": 2019,
        "status": "Active",
        "price": 2200,
        "listingType": "Standard",
        "listedDate": "2024-09-18T00:00:00.000Z",
        "removedDate": None,
        "createdDate": "2024-09-19T00:00:00.000Z",
        "lastSeenDate": "2024-09-30T03:49:20.620Z",
        "daysOnMarket": randrange(1, 500),
        "mlsName": "CentralTexas",
        "mlsNumber": "556965",
    }

    # Create the nested dictionaries



if __name__ == '__main__':
    #gen_fake_listing()
    f = Faker()
    print(f.address())