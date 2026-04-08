# Cleans the Yelp review data for faster, more memory efficient access
# The goal is to convert the data to a csv format and sort the data by
# certain criteria so that we can use a binary search to read the file
# without loading everything into memory.

# We will use merge sort because this will allow us to read and write
# sequentially without needing to load all the data into memory.
# We only need the business and potentially review files for this application.
# The cleaned business data will be stored in data/yelp_businesses.csv

from itertools import islice 
import json
import os
import time
import pygeohash as pgh

def compare_businesses(left, right):
    """ Return true if the item on the left is 'smaller'. The function
    sorts the yelp business objects based on their location.

    Args:
        left (str): a csv string containing the business information
        right (str): a csv string containing the business information

    Returns:
        bool: true if the left item is 'smaller' 
    """
    # Get the left lat and long
    left_split = left.split(',')
    left_lat = float(left_split[0])
    left_long = float(left_split[1])

    # Get the right lat and long
    right_split = right.split(',')
    right_lat = float(right_split[0])
    right_long = float(right_split[1])

    # Get the geohashes for both
    left_hash = pgh.encode(left_lat, left_long)
    right_hash = pgh.encode(right_lat, right_long)

    # Compare the hashes
    return left_hash < right_hash

def csvify_businesses(json_line):
    # Convert from JSON, calling it j to make the next line shorter
    j = json.loads(json_line)
    return (f"{j['latitude']},{j['longitude']},{j['business_id']},{j['name']}," +
            f"{j['address']},{j['city']},{j['state']},{j['postal_code']},{j['stars']},{j['review_count']},{j['is_open']}")

def get_file_length(file_path):
    length = 0
    with open(file_path, 'r') as file:
        # Count all of the items
        item = next(file, None)
        while item is not None:
            length += 1
            item = next(file, None)

    return length

def merge_merge(left_start, right_start, depth, result_file_path, compare_func):
    # Open the left and right files
    file_left = open(f'data/yelp_temp{depth+1}:{left_start}.csv', 'r')
    file_right = open(f'data/yelp_temp{depth+1}:{right_start}.csv', 'r')

    # Overwrite the result file, then open it for appending
    if depth != 0:
        result_file_path = f'data/yelp_temp{depth}:{left_start}.csv'
    file_merged = open(result_file_path, 'w')
    file_merged.write('')
    file_merged.close()
    file_merged = open(result_file_path, 'a')

    left_item = next(file_left, None)
    right_item = next(file_right, None)
    # Compare the two sides, adding the smaller to the result until we
    # consume all the items
    while left_item is not None and right_item is not None:
        if compare_func(left_item, right_item):
            file_merged.write(left_item.strip() + '\n')
            left_item = next(file_left, None)
        else:
            file_merged.write(right_item.strip() + '\n')
            right_item = next(file_right, None)
    
    # If there are any left over on either side, write them
    while left_item is not None:
        file_merged.write(left_item.strip() + '\n')
        left_item = next(file_left, None)

    while right_item is not None:
        file_merged.write(right_item.strip() + '\n')
        right_item = next(file_right, None)

    # Close the files
    file_merged.close()
    file_left.close()
    file_right.close()

    # Delete the left and right files because we no longer need them
    os.remove(f'data/yelp_temp{depth+1}:{left_start}.csv')
    os.remove(f'data/yelp_temp{depth+1}:{right_start}.csv')

    
def merge_sort(file_path, start, end, result_file_path, compare_func, csvify_func, depth=0):
    # Base case, only one item
    if end - start == 1:
        # Get the item from the file
        with open(file_path, 'r') as file:
            json_line = list(islice(file, start, end))[0]

        # Convert the item to a line of csv
        csv_line = csvify_func(json_line)

        # Write the item to csv file, the depth and start will provide unique file names
        with open(f'data/yelp_temp{depth}:{start}.csv', 'w') as file:
            file.write(csv_line)

    # Otherwise, recurse
    elif end - start > 1:
        mid = ((end - start) // 2) + start
        merge_sort(file_path, start, mid, result_file_path, compare_func, csvify_func, depth=depth+1)
        merge_sort(file_path, mid, end, result_file_path, compare_func, csvify_func, depth=depth+1)

        # Merge the results
        merge_merge(start, mid, depth, result_file_path, compare_func)

# test
def compare_test(left, right):
    return left < right

def csvify_test(json_line):
    j = json.loads(json_line)
    return f"{j['name']},{j['test']}"


def main():
    # Run the merge sort on the business data

    print('Getting length...')

    # Get the length of the business file
    start_time = time.perf_counter()
    length = get_file_length('data/yelp_temp/yelp_academic_dataset_business.json')
    end_time = time.perf_counter()

    total_time = end_time - start_time
    print(f'Read file length in {total_time}s.')

    # Run the sort on the business data
    start_time = time.perf_counter()
    merge_sort('data/yelp_temp/yelp_academic_dataset_business.json', 0, length, 'data/yelp_businesses.csv', compare_businesses, csvify_businesses)
    end_time = time.perf_counter()

    total_time = end_time - start_time
    print(f'Converted and sorted yelp business data in {total_time}s.')


if __name__ == '__main__':
    main()