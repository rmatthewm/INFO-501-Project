# Project for INFO-H 501 at IUI
*Raúl Mosley, Chirag Karachiwala, Danielle Dixon*

## Abstract
Write abstract

## Data
### RentCast Listing Data
To get current rental listings to recommend to the user, we are using the
RentCast API. This provides current rental listings in a given city. The
data is returned in json format which we have kept. This data does not
need cleaning. In order to access the API, the app will also need
a .env file to provide the access key `LISTINGS_API_KEY` and url `LISTINGS_API_URL`. 

For development, we use a mock API that can be started by running the file
`fake-api/fake-api.py`. To use the fake API for development, run `python3 fake-api.py`
in a different console in the `fake-api` directory. Then the main Streamlit
app can access it.

### Yelp Review Data
To provide a score for the area around each listing, we are using review data
from Yelp of local businesses. This is obviously not the most accurate way of
judging an area, but the data is free. And it gives an interesting analysis of
what the experience might be living there.

An interesting limitation of this data set is it does not seem to contain data
for several major cities such as NYC, LA, and Phoenix. Raul discovered this while
running some tests with the data. It has data for other areas within these states,
but it seems they have removed the data from the largest cities for some reason. It
has Indianapolis, though.

To set up the Yelp review data, first download the Yelp data found here: 
`https://business.yelp.com/data/resources/open-dataset/`. After extracting, 
the JSON files should be moved into a directory located at `data/yelp_temp`.
After this, the `yelp_data_cleaner.py` script should be run which will 
convert the data to csv and sort it. This data requires the most cleaning of
all the data. The original data is over 8gb across several files, but we do
not need all of the data for our uses. The cleaner script converts the data
to csv and sorts it by its geohash so it can be searched with binary search to
find businesses near certain coordinates. Commas in the address field or business
name are replaced with hyphens to preserve csv format. There are also some 
extraneous commas in the other fields in some rows, and these are simply removed.

### County-level Fair Market Rate Data
To analyze the price of each rental, we compare it against the fair market rent price
for the county. This data comes from the US Department of Housing and Urban Development. The data
was originally in Excel but was exported to csv without changes. The `rental_data.csv`
is the main part of the data, and `rental_data_headers.csv` is the provided explanation
for each column. To provide more concise display names for the columns, we created
`rental_data_columns.csv`, which also corrects some mismatched column names with the
actual dataset. These should be placed in the `data` directory. The original `rental_data_headers.csv`
provided will not work because of misnamed columns.

## Algorithms
talk about algorithms

## Tools Used
stuff

## Ethical Concerns
stuff