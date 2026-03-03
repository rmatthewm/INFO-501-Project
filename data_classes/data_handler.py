import pandas as pd


# Do stuff with the data
class DataHandler():
    def __init__(self, csv_path):
        """ Initialize the data handler with the data

        Args:
            csv_path (str): the path to the data as a csv file
        """
        self.__df = pd.read_csv(csv_path)

    def get_state_codes(self):
        return list(self.__df['stusps'].unique())

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
