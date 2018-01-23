## import all necessary packages and functions.
import csv
from datetime import datetime
from pprint import pprint


def print_first_point(filename):
    """
    This function prints and returns the first data point (second row) from
    a csv file that includes a header row.
    """
    # print city name for reference
    city = filename.split('-')[0].split('/')[-1]
    print('\nCity: {}'.format(city))

    with open(filename,newline='') as f_in:
        ## TODO: Use the csv library to set up a DictReader object. ##
        ## see https://docs.python.org/3/library/csv.html           ##
        trip_reader = csv.DictReader(f_in)

        # for row in trip_reader:


        ## TODO: Use a function on the DictReader object to read the     ##
        ## first trip from the data file and store it in a variable.     ##
        ## see https://docs.python.org/3/library/csv.html#reader-objects ##
        first_trip = trip_reader.__next__()

        ## TODO: Use the pprint library to print the first trip. ##
        ## see https://docs.python.org/3/library/pprint.html     ##
        pprint(first_trip)

    # output city name and first trip for later testing
    return (city, first_trip)


# list of files for each city
data_files = ['NYC-CitiBike-2016.csv',
             'Chicago-Divvy-2016.csv',
              'Washington-CapitalBikeshare-2016.csv', ]

# print the first trip from each file, store in dictionary
example_trips = {}
for data_file in data_files:
    city, first_trip = print_first_point(data_file)
    example_trips[city] = first_trip

def duration_in_mins(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the trip duration in units of minutes.

    Remember that Washington is in terms of milliseconds while Chicago and NYC
    are in terms of seconds.

    HINT: The csv module reads in all of the data as strings, including numeric
    values. You will need a function to convert the strings into an appropriate
    numeric type when making your transformations.
    see https://docs.python.org/3/library/functions.html
    """

    # YOUR CODE HERE
    temp = 0
    if city == 'NYC' or city == 'Chicago':
        temp = int(datum['tripduration'])
    elif city == 'Washington':
        temp = int(datum['Duration (ms)'])
        temp = temp / (10**3)

    temp = temp / 60
    duration = temp
    return duration


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': 13.9833,
         'Chicago': 15.4333,
         'Washington': 7.1231}

for city in tests:
    assert abs(duration_in_mins(example_trips[city], city) - tests[city]) < .001


def time_of_trip(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the month, hour, and day of the week in
    which the trip was made.

    Remember that NYC includes seconds, while Washington and Chicago do not.

    HINT: You should use the datetime module to parse the original date
    strings into a format that is useful for extracting the desired information.
    see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    """

    # YOUR CODE HERE
    dt = ''
    if city == 'NYC':
        dt = datetime.strptime(datum['starttime'],"%m/%d/%Y %H:%M:%S")

    elif city == 'Chicago':
        dt = datetime.strptime(datum['starttime'], "%m/%d/%Y %H:%M")

    elif city == 'Washington':
        dt = datetime.strptime(datum['Start date'], "%m/%d/%Y %H:%M")

    month = int(datetime.strftime(dt, "%m"))
    hour = int(datetime.strftime(dt, "%H"))
    day_of_week = datetime.strftime(dt, "%A")
    return (month, hour, day_of_week)


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': (1, 0, 'Friday'),
         'Chicago': (3, 23, 'Thursday'),
         'Washington': (3, 22, 'Thursday')}

for city in tests:
    assert time_of_trip(example_trips[city], city) == tests[city]


def type_of_user(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the type of system user that made the
    trip.

    Remember that Washington has different category names compared to Chicago
    and NYC.
    """

    # YOUR CODE HERE
    user_type = ''
    if city == 'NYC' or city == 'Chicago':
        user_type = datum['usertype']

    elif city == 'Washington':
        user_type = datum['Member Type']

    return user_type


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': 'Customer',
         'Chicago': 'Subscriber',
         'Washington': 'Registered'}

for city in tests:
    assert type_of_user(example_trips[city], city) == tests[city]


def condense_data(in_file, out_file, city):
    """
    This function takes full data from the specified input file
    and writes the condensed data to a specified output file. The city
    argument determines how the input file will be parsed.

    HINT: See the cell below to see how the arguments are structured!
    """

    with open(out_file, 'w',newline='') as f_out, open(in_file, 'r') as f_in:
        # set up csv DictWriter object - writer requires column names for the
        # first row as the "fieldnames" argument
        out_colnames = ['duration', 'month', 'hour', 'day_of_week', 'user_type']
        trip_writer = csv.DictWriter(f_out, fieldnames=out_colnames)
        trip_writer.writeheader()

        ## TODO: set up csv DictReader object ##
        trip_reader = csv.DictReader(f_in)

        # collect data from and process each row
        for row in trip_reader:
            # set up a dictionary to hold the values for the cleaned and trimmed
            # data point
            new_point = {}

            ## TODO: use the helper functions to get the cleaned data from  ##
            ## the original data dictionaries.                              ##
            ## Note that the keys for the new_point dictionary should match ##
            ## the column names set in the DictWriter object above.         ##
            month, hour, day_of_week = time_of_trip(row,city)
            new_point['duration'] = duration_in_mins(row,city)
            new_point['month'] = month
            new_point['hour'] = hour
            new_point['day_of_week'] = day_of_week
            new_point['user_type'] = type_of_user(row,city)

            ## TODO: write the processed information to the output file.     ##
            ## see https://docs.python.org/3/library/csv.html#writer-objects ##
            writer = csv.DictWriter(f_out,fieldnames=out_colnames)
            writer.writerow(new_point)

# Run this cell to check your work
city_info = {'Washington': {'in_file': 'Washington-CapitalBikeshare-2016.csv',
                            'out_file': 'Washington-2016-Summary.csv'},
             'Chicago': {'in_file': 'Chicago-Divvy-2016.csv',
                         'out_file': 'Chicago-2016-Summary.csv'},
             'NYC': {'in_file': 'NYC-CitiBike-2016.csv',
                     'out_file': 'NYC-2016-Summary.csv'}}

for city, filenames in city_info.items():
    condense_data(filenames['in_file'], filenames['out_file'], city)
    print_first_point(filenames['out_file'])


def number_of_trips(filename):
    """
    This function reads in a file with trip data and reports the number of
    trips made by subscribers, customers, and total overall.
    """
    with open(filename, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)

        # initialize count variables
        n_subscribers = 0
        n_customers = 0

        # tally up ride types
        for row in reader:
            if filename != 'Washington-2016-Summary.csv':
                if row['user_type'] == 'Subscriber':
                    n_subscribers += 1
                else:
                    n_customers += 1
            else:
                if row['user_type'] == 'Registered':
                    n_subscribers += 1
                else:
                    n_customers += 1

        # compute total number of rides
        n_total = n_subscribers + n_customers

        # return tallies as a tuple
        return (n_subscribers, n_customers, n_total)


summary_files = ['Washington-2016-Summary.csv', 'Chicago-2016-Summary.csv', 'NYC-2016-Summary.csv']
for file in summary_files:
    n_subscribers, n_customers, n_total = number_of_trips(file)
    ratio_customer = n_customers / n_total
    ratio_subscriber = n_subscribers / n_total
    print(file)
    print('Total', n_total)
    print('Customer Proportion', ratio_customer)
    print('Subscriber Proportion', ratio_subscriber)
    print('\n')


## Use this and additional cells to answer Question 4b.                 ##
##                                                                      ##
## HINT: The csv module reads in all of the data as strings, including  ##
## numeric values. You will need a function to convert the strings      ##
## into an appropriate numeric type before you aggregate data.          ##
## TIP: For the Bay Area example, the average trip length is 14 minutes ##
## and 3.5% of trips are longer than 30 minutes.                        ##

def average_trip_length(filename):
    with open(filename, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)

        # initialize count variables
        total_time = 0
        count = 0
        count_greater_30 = 0

        for row in reader:

            total_time += float(row['duration'])
            count += 1

            if float(row['duration']) > 30.0:
                count_greater_30 += 1

        average_length = total_time / count
        proportion_greater_30 = count_greater_30 / count

        return [average_length, proportion_greater_30]


summary_files = ['Washington-2016-Summary.csv', 'Chicago-2016-Summary.csv', 'NYC-2016-Summary.csv']
for file in summary_files:
    average_proportion = average_trip_length(file)
    print(file)
    print('Average time:', round(average_proportion[0], 2))
    print('Proportion greater 30 minutes:', round(average_proportion[1] * 100, 2), '%')
    print('\n')


## Use this and additional cells to answer Question 4c. If you have    ##
## not done so yet, consider revising some of your previous code to    ##
## make use of functions for reusability.                              ##
##                                                                     ##
## TIP: For the Bay Area example data, you should find the average     ##
## Subscriber trip duration to be 9.5 minutes and the average Customer ##
## trip duration to be 54.6 minutes. Do the other cities have this     ##
## level of difference?                                                ##

def find_longer(filename):
    with open(filename, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)

        # initialize count variables
        total_time_customer = 0
        total_time_subscriber = 0

        for row in reader:
            if filename != 'Washington-2016-Summary.csv':
                if row['user_type'] == 'Subscriber':
                    total_time_subscriber += float(row['duration'])
                else:
                    total_time_customer += float(row['duration'])

            else:
                if row['user_type'] == 'Registered':
                    total_time_subscriber += float(row['duration'])

                else:
                    total_time_customer += float(row['duration'])

        count_subscriber, count_customer, count_total = number_of_trips(filename)

        average_length_customer = total_time_customer / count_customer
        average_length_subscriber = total_time_subscriber / count_subscriber

        return [average_length_customer, average_length_subscriber]


summary_files = ['Washington-2016-Summary.csv', 'Chicago-2016-Summary.csv', 'NYC-2016-Summary.csv',
                 'BayArea-Y3-Summary.csv']
for file in summary_files:
    average_time = find_longer(file)
    print(file)
    print('Average time Customer:', round(average_time[0], 2))
    print('Average time Subscriber:', round(average_time[1], 2))
    print('\n')

## Use this and additional cells to collect all of the trip times as a list ##
## and then use pyplot functions to generate a histogram of trip times.     ##
import matplotlib.pyplot as plt

# this is a 'magic word' that allows for plots to be displayed
# inline with the notebook. If you want to know more, see:
# http://ipython.readthedocs.io/en/stable/interactive/magics.html
%matplotlib inline 

trip_time = []
with open('Chicago-2016-Summary.csv', 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)
        for row in reader:
            trip_time.append(round(float(row['duration']),2))
                

plt.hist(trip_time)
plt.title('Distribution of Trip Durations')
plt.xlabel('Duration (m)')
plt.show()

## Use this and additional cells to answer Question 5. ##
## Use this and additional cells to collect all of the trip times as a list ##
## and then use pyplot functions to generate a histogram of trip times.     ##
import matplotlib.pyplot as plt

# this is a 'magic word' that allows for plots to be displayed
# inline with the notebook. If you want to know more, see:
# http://ipython.readthedocs.io/en/stable/interactive/magics.html
%matplotlib inline 

trip_time_sub = []
trip_time_cus = []
with open('Chicago-2016-Summary.csv', 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)
        for row in reader:
            if row['user_type'] == 'Subscriber' and float(row['duration']) < 75:
                trip_time_sub.append(round(float(row['duration']),2))
            elif row['user_type'] == 'Customer' and float(row['duration']) < 75:
                trip_time_cus.append(round(float(row['duration']),2))
                
plt.hist(trip_time_sub,bins = [x for x in range(0,80,5)])
plt.title('Distribution of Trip Durations (Subscriber)')
plt.xlabel('Duration (m)')
plt.show()

plt.hist(trip_time_cus,bins = [x for x in range(0,80,5)])
plt.title('Distribution of Trip Durations (Customer)')
plt.xlabel('Duration (m)')
plt.show()