# Generate fake listings in the format of the real RentCast rental listings
# API so that we can test the app without using up our free API calls

# We can use faker to create more realistic data
from faker import Faker
from random import randint, randrange

# The options for property type according to the docs
PROPERTY_TYPES = ['Single Family', 'Condo', 'Townhouse', 'Manufactured', 
    'Multi-Family', 'Apartment']


def gen_fake_listing():
    """ Generates a fake listing JSON result based on the example above."""
    fkr = Faker('en_US')
    address_line1 = f'{fkr.building_number()} {fkr.street_name()},'

    # Only give a second line to some addresses
    address_line2 = fkr.secondary_address() if randint(0, 1) == 1 else None

    city = fkr.city()
    state = fkr.state_abbr()
    zip = fkr.zipcode_in_state(state)

    # Make a single line address
    full_address = address_line1
    if address_line2 is not None:
        full_address +=  f' {address_line2},'
    full_address += f' {city}, {state} {zip}'

    # Select one of the property types from the docs
    i = randrange(len(PROPERTY_TYPES))
    property_type = PROPERTY_TYPES[i]

    # price

    # date

    listing = {
        "id": full_address.replace(' ', '-'),
        "formattedAddress": full_address,
        "addressLine1": address_line1,
        "addressLine2": address_line2,
        "city": city,
        "state": state,
        "stateFips": fkr.numerify('##'),
        "zipCode": zip,
        # There is no county option, so I chose colors instead because I
        # thought it was funny and would be good enough.
        "county": fkr.color_name(),
        "countyFips": fkr.numerify('###'),
        "latitude": fkr.latitude(),
        "longitude": fkr.longitude(),
        "propertyType": property_type,
        "bedrooms": randint(1, 4),
        "bathrooms": randint(1, 4),
        "squareFootage": randint(500, 2000),
        "lotSize": randint(500, 2000),
        "yearBuilt": randint(1900, 2026),
        "hoa": {
            "fee": randint(500)
        },
        "status": "Active",
        "price": 2200,
        "listingType": "Standard",
        "listedDate": "2024-09-18T00:00:00.000Z",
        "removedDate": None,
        "createdDate": "2024-09-19T00:00:00.000Z",
        "lastSeenDate": "2024-09-30T03:49:20.620Z",
        "daysOnMarket": randint(1, 500),
        "mlsName": fkr.company(),
        "mlsNumber": fkr.numerify('######'),
        "listingAgent": {
            "name": fkr.full_name(),
            "phone": fkr.phone_number(),
            "email": fkr.email(),
            "website": fkr.url()
        },
        "listingOffice": {
            "name": fkr.company(),
            "phone": fkr.phone_number(),
            "email": fkr.email(),
            "website": fkr.url()
        },
        "history": "realistically, I don't think we need any of this."
    }

    # Create the nested dictionaries
    return listing



if __name__ == '__main__':
    print(gen_fake_listing())