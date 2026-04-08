# Project for INFO-H 501 at IUI
*Raúl Mosley, Chirag Karachiwala, Danielle Dixon*

## Project Structure
Pages for the Streamlit app are in the `views` folder. The app.py file will
handle the navigation and session-level information only. Anything else
should be on a specific page.

## Data
### RentCast Listing Data
For development, we use a mock API that can be started by running the file
`fake-api/fake-api.py`. In order to access the API, the app will also need
the .env file to provide the access key.

### Yelp Review Data
To set up the Yelp review data, first download the Yelp data found here: 
`https://business.yelp.com/data/resources/open-dataset/`. After extracting, 
the JSON files should be moved into a directory located at `data/yelp_temp`.
After this, the `yelp_data_cleaner.py` script should be run which will 
convert the data to csv and sort it.

### County-level Fair Market Rate Data
This data comes from the US Department of Housing and Urban Development. The data
was originally in Excel but was exported to csv without changes. The `rental_data.csv`
is the main part of the data, and `rental_data_headers.csv` is the provided explanation
for each column. To provide more concise display names for the columns, we created
`rental_data_columns.csv`, which also corrects some mismatched column names with the
actual dataset. These should be placed in the `data` directory.

## Example Page
I kept the example page for now, but I moved it into the views folder. It
can now be accessed as part of the main app at the route `/example`.

## Running the Fake API
To use the fake API for development, run `python3 fake-api.py` in a different console in the `fake-api` directory. Then the main Streamlit app can access it.