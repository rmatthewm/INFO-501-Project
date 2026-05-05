# Project for INFO-H 501 at IUI
*Raúl Mosley, Chirag Karachiwala, Danielle Dixon*

## Abstract
This project is a data-driven Streamlit web application designed to help users find rental listings that best fit their financial situation and personal needs. Users can input information such as income, preferred number of bedrooms, and location, and the app will recommend rental listings based on a combination of affordability, proximity, and local business quality.

The system integrates multiple data sources, including real time rental listings from the RentCast API, county-level Fair Market Rent (FMR) data from HUD, and Yelp business review data. By combining these sources, the app provides a more comprehensive recommendation system than traditional rental search tools. The goal of this project is to create a user friendly tool that helps individuals make more informed housing decisions based on both cost and quality of life factors.

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
The core of this project is a recommendation model that assigns a score to each listing based on multiple factors. Each listing is evaluated using three main components:

- **Price Score (50%)**  
  The listing price is compared to the county’s Fair Market Rent. Listings priced below or near the expected rent receive higher scores.

- **Distance Score (25%)**  
  The distance between the user’s selected location (e.g., school or workplace) and the listing is calculated using the haversine formula. Closer listings receive higher scores.

- **Review Score (25%)**  
  Yelp data is used to evaluate nearby businesses. The average rating of nearby businesses contributes to a score representing the quality of the area.

Each of these scores is normalized to a scale from 0 to 100 and combined using a weighted average to produce a final recommendation score:

Final Score = (Distance Score × 25 + Review Score × 25 + Price Score × 50) / 100

Listings are then ranked by this score, and the top results are returned to the user.

We also added an **Income-Based Recommendation System** for users who want to make a decision based only on income and affordability. This part of the app takes the user’s annual income, preferred number of bedrooms, and state as inputs. It then estimates an affordable monthly rent using the 30% income rule and compares that amount to the Fair Market Rent values in the dataset.

The income-based model returns the top recommended counties with:
- County name
- HUD area
- Monthly rent
- Affordability score out of 100
- Affordability label

This provides a simpler alternative for users who want to explore housing options strictly based on what they can afford.

## Tools Used
- **Python** – Core programming language  
- **Streamlit** – Web app framework for building the UI  
- **Pandas** – Data manipulation and analysis  
- **Requests** – API communication (RentCast API)  
- **Haversine** – Distance calculations between coordinates  
- **Faker** – Generating mock data for testing  
- **pygeohash** – Efficient location-based searching for Yelp data  
- **GitHub / Codespaces** – Version control and collaboration  
- **dotenv** – Managing API keys and environment variables
- **Figma** - Mid-Hi Fidelity Prototyping prior to deployment
- **Color Picker** - Used for color identification
- **WCAG Color Contrast Checker** - Used to ensure visual contrast (AA minimum) 

## Ethical Concerns

There are several ethical considerations in this project:

- **Data Bias:** Yelp reviews may not accurately represent the true quality of an area. They are subjective and may reflect biases of users who leave reviews.

- **Incomplete Data:** Missing data for major cities could lead to unfair or misleading recommendations.

- **Affordability Assumptions:** The use of the 30% income rule may not apply to all users, especially those with different financial situations or cost-of-living factors.

- **Privacy Considerations:** While we do not collect personal data, location-based recommendations could raise concerns if expanded in the future.

- **Over-Reliance on Algorithmic Decisions:** Users may rely too heavily on the app’s recommendations without considering other important personal factors.

Overall, this tool is intended to assist users in decision-making, not replace their judgment.
