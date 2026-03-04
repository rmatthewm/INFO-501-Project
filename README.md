# Project for INFO-H 501 at IUI
*Raúl Mosley, Chirag Karachiwala, Danielle Dixon*

## Project Structure
Pages for the Streamlit app are in the `views` folder. The app.py file will
handle the navigation and session-level information only. Anything else
should be on a specific page.

## Data
The data comes from the US Department of Housing and Urban Development. The data
was originally in Excel but was exported to csv without changes. The `rental_data.csv`
is the main part of the data, and `rental_data_headers.csv` is the provided explanation
for each column. To provide more concise display names for the columns, we created
`rental_data_columns.csv`, which also corrects some mismatched column names with the
actual dataset.

## Example Page
I kept the example page for now, but I moved it into the views folder. It
can now be accessed as part of the main app at the route `/example`.
