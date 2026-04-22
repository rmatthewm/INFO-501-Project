# Generate fake listings in the format of the real RentCast rental listings
# API so that we can test the app without using up our free API calls

# We can use faker to create more realistic data
from faker import Faker
from random import randint, randrange, uniform

# The options for property type according to the docs
PROPERTY_TYPES = ['Single Family', 'Condo', 'Townhouse', 'Manufactured', 
    'Multi-Family', 'Apartment']


def gen_fake_listing(city=None, state=None, latlong=None, radius=50):
    """ Generates a fake listing JSON result based on the example above."""
    fkr = Faker('en_US')
    address_line1 = f'{fkr.building_number()} {fkr.street_name()},'

    # Only give a second line to some addresses
    address_line2 = fkr.secondary_address() if randint(0, 1) == 1 else None

    # If no city or state is given, we will generate a  
    # random city and state
    if city is None or state is None:
        city = fkr.city()
        state = 'IN'

    zip = fkr.zipcode_in_state(state)

    # Make a single line address
    full_address = address_line1
    if address_line2 is not None:
        full_address +=  f' {address_line2},'
    full_address += f' {city}, {state} {zip}'

    # Select one of the property types from the docs
    i = randrange(len(PROPERTY_TYPES))
    property_type = PROPERTY_TYPES[i]

    # If coords are not given, we will center it at IUPUI
    if latlong is None:
        latlong = (39.774235, -86.175278)

    # The random area covered is actually more of a "box" with the radius
    # as the side lengths, but its close enough
    # Latitude lines are roughly 69 miles apart
    dist = radius / 69 
    lat = uniform(latlong[0] - dist, latlong[0] + dist)

    # Longitude lines are roughly 50 miles apart in the US
    # (this is like saying pi = 4, but it's fine)
    dist = radius / 50
    long = uniform(latlong[1] - dist, latlong[1] + dist)

    # Pick a county near Indy so we have a valid county
    counties = ['Marion', 'Johnson', 'Hamilton', 'Hancock', 'Hendricks']

    listing = {
        "id": full_address.replace(' ', '-'),
        "formattedAddress": full_address,
        "addressLine1": address_line1,
        "addressLine2": address_line2,
        "city": city,
        "state": state,
        "stateFips": fkr.numerify('##'),
        "zipCode": zip,
        "county": counties[randrange(len(counties))],
        "countyFips": fkr.numerify('###'),
        # The json converter doesn't like it if these are floats
        "latitude": str(lat),
        "longitude": str(long),
        "propertyType": property_type,
        "bedrooms": randint(1, 4),
        "bathrooms": randint(1, 4),
        "squareFootage": randint(500, 2000),
        "lotSize": randint(500, 2000),
        "yearBuilt": randint(1900, 2026),
        "hoa": {
            "fee": randint(0, 500)
        },
        "status": "Active",
        "price": randint(300,3000),
        "listingType": "Standard",
        "listedDate": "2024-09-18T00:00:00.000Z",
        "removedDate": None,
        "createdDate": "2024-09-19T00:00:00.000Z",
        "lastSeenDate": "2024-09-30T03:49:20.620Z",
        "daysOnMarket": randint(1, 500),
        "mlsName": fkr.company(),
        "mlsNumber": fkr.numerify('######'),
        "listingAgent": {
            "name": fkr.name(),
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