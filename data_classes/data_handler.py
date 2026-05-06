import pandas as pd


# Do stuff with the data
class DataHandler():
    def __init__(self, csv_path, csv_header_path):
        """ Initialize the data handler with the data

        Args:
            csv_path (str): the path to the data as a csv file
        """
        self.__df = pd.read_csv(csv_path)

        # Get the column names to display from the csv header file
        # and add them to a dictionary so we can get them for each
        # column as needed. These names are nicer to display to the
        # user.
        self.__fancy_col_names = {}

        # Transpose the dataframe so that each column gives the corresponding fancy name
        header_df = pd.read_csv(csv_header_path, index_col=0, header=None).T
        real_names = header_df.columns
        for name in real_names:
            self.__fancy_col_names[str(name)] = header_df[name].iloc[0]

    def get_dataframe(self):
        """ Return a copy of the dataframe so the original cannot
        be modified from the outside

        Returns:
            pandas.DataFrame: a copy of the data
        """
        return self.__df.copy()

    # Create a read-only property to access the dataframe more easily
    data = property(fget=get_dataframe)

    def get_state_codes(self):
        """ Return the two letter state codes

        Returns:
            list: a list of state codes
        """
        return list(self.__df['stusps'].unique())

    def get_columns(self):
        """ Return the dataframe's column names

        Returns:
            pandas.Index: a list of column names
        """
        return self.__df.columns

    def get_col_fancy_name(self, col_name):
        """ Return the name to display for a column

        Args:
            col_name (str): the actual name of the column in the data

        Returns:
            str: the name to display
        """
        return self.__fancy_col_names[col_name]

    def get_county_fmr(self, county, state, bed_count=0):
        """ Return the fair market rent for a given county and bed count

        Args:
            county (str): the name of the county without the word county
            state (str): the two letter state code
            bed_count (int, optional): the number of bedrooms. Defaults to 0.

        Returns:
            int: the fmr for this county and bed combination
        """
        # Prepare the capitalization
        county = county[0].upper() + county[1:].lower() + ' County'
        state = state.upper()
        return list(self.__df[(self.__df['countyname'] == county) & (self.__df['stusps'] == state)][f'fmr_{bed_count}'])[0]


    def get_average_rate(self, state='any', bed_count=0):
        """ Returns the mean rate for either the entire US or a given state
        for a given bedroom count.

        Args:
            state (str, optional): state to average. Defaults to 'any'.
            bed_count (int, optional): number of bedrooms. Defaults to 0.

        Raises:
            ValueError: if bedroom count is not between [0, 4]

        Returns:
            int: the mean rate
        """
        # There are only between 0 and 4 bedrooms in the dataset
        if bed_count < 0 or bed_count > 4:
            raise ValueError('Number of bedrooms must be 0 <= bed_count <= 4.')

        # If no state specified, return the mean for the US
        if state == 'any':
            return self.__df[f'fmr_{bed_count}'].mean()

        # Otherwise return the mean for a specific state
        filter = self.__df['stusps'] == state
        return self.__df[filter][f'fmr_{bed_count}'].mean()
        
    def get_cheapest_counties(self, state='any', bed_count=0, n_results=5):
        """ Returns the n_results cheapest counties for number of bedrooms,
        can be filtered by state.

        Args:
            state (str, optional): two letter state code. Defaults to 'any'.
            bed_count (int, optional): number of bedrooms. Defaults to 0.
            n_results (int, optional): number of results to return. Defaults to 5.

        Returns:
            pandas.DataFrame: the data related to the top n results
        """

        # There are only between 0 and 4 bedrooms in the dataset
        if bed_count < 0 or bed_count > 4:
            raise ValueError('Number of bedrooms must be 0 <= bed_count <= 4.')
        
        # Filter the results as needed
        if state != 'any':
            filter = self.__df['stusps'] == state
            results = self.__df[filter]
        else:
            results = self.__df

        # Sort by the cost for a given number of bed rooms 
        results = results.sort_values(by=f'fmr_{bed_count}')

        # Return the results
        return results.head(n_results)
    
    
    def get_recommendations(self, income, bed_count=0, state='any', n_results=5):
        """Return top recommended counties based on affordability"""

        monthly_income = income / 12
        affordable_rent = monthly_income * 0.3

        # Filter by state
        if state != 'any':
            df = self.__df[self.__df['stusps'] == state].copy()
        else:
            df = self.__df.copy()

        rent_col = f'fmr_{bed_count}'

        # Affordability ratio
        df['affordability_ratio'] = df[rent_col] / affordable_rent

        # Score (higher = better)
        df['affordability_score'] = 100 - (df['affordability_ratio'] * 100)
        df['affordability_score'] = df['affordability_score'].clip(0, 100)

        # Labels
        def label(x):
            if x <= 1:
                return "Affordable"
            elif x <= 1.2:
                return "Moderately Affordable"
            else:
                return "Not Affordable"

        df['affordability_label'] = df['affordability_ratio'].apply(label)

        # Sort best options
        df = df.sort_values(by='affordability_score', ascending=False)

        return df.head(n_results)