import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please enter the city you are interested in (chicago, new york city, washington):')
    while city not in CITY_DATA:
        city = input('You misspelled something. Please enter the city you are interested in (chicago, new york city, washington):')
    # get user input for month (all, january, february, ... , june)
    month = input('PLease enter the month you are interested in or all (all, january, february, ... , june):')
    months = ['all','january','february','march','april','may','june']
    while month not in months:
        month = input('You misspelled something! PLease enter the month you are interested in or all (all, january, february, ... , june):')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    day = input('Please enter the day you are interested in (all, monday, tuesday, ... sunday):')
    while day not in days:
        day = input('You misspelled something. Please enter the day you are interested in (all, monday, tuesday, ... sunday):')
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days =['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        day = days.index(day) + 1
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month of travel is:', most_common_month)
    # display the most common day of week
    most_common_dow = df['day_of_week'].mode()[0]
    print('The most common day of the week to travel is:', most_common_dow)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common hour to travel is:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common Start Station is:', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most common End Station is:', most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_frequent = df.groupby(['Start Station','End Station']).size().idxmax()
    print('The most frequent combination of start station and end station trip:\n', most_frequent[0], ' and ', most_frequent[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_travel_time = df['Trip Duration'].sum()
    print('The total travel time is: ', tot_travel_time/3600, 'h' )

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is: ', mean_travel_time/60, 'min' )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The user types are:')
    print('Subscriber:',user_types[0])
    print('Customer:',user_types[1],'\n')

    if  city != 'washington':
        # Display counts of gender
        gender_types= df['Gender'].value_counts()
        print('The gender types are:')
        print('Male:',gender_types[0])
        print('Female:', gender_types[1],'\n')

        # Display earliest, most recent, and most common year of birth
        print('The earliest year of birth is:', df['Birth Year'].min())
        print('The most recent year of birth is:', df['Birth Year'].max())
        print('The most common year of birth is:', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        cont = input('Do you want to see the first five rows of raw data? Type: yes.\n')
        n = 0

        while cont == 'yes':
            df = pd.read_csv(CITY_DATA[city])
            print(df.loc[n:n+4,:])
            n += 5
            cont = input('Do you want to see five more rows of raw data? Type: yes.\n')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
