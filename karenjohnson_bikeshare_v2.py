import time
import pandas as pd
import calendar


debug = 0
debug2 = 0

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june']
DAY_DATA = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
ROWINCREMENT = 1000

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    while True:
        # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input("Please select from the following Cities by entering city name:\nChicago \nNew York \nWashington DC\n\nWhich city would you like to explore?  "+
                     "(just ENTER to explore all 3 cities):  ")
        
        city = city.lower()
        if city == "":
            city = 'all'
            break
        elif city == 'chicago':
            break
        elif city == 'new york city' or city == 'new york' or city == 'ny': 
            city = 'new york city'
            break
        elif city == 'washington dc' or city == 'washington':  
            city = 'washington'
            break
        else: 
            print ("Not a valid input: Please try again\n")
               
    
    while True:
        # TO DO: get user input for month (all, january, february, ... , june)
        print ("\n\nSelect which month to explore Bikeshare Data: \nJanuary\nFebruary\nMarch\nApril\nMay\nJune\n")
        month = input("Enter the desired month (or just ENTER for bikeshare data for all months) :  ")
        
        month = month.lower()
        if month == "":
            month = 'all'
            break
        elif month in MONTH_DATA:
            break
        else:
            print ("Not a valid input: Please try again\n")

    while True:
        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("Would you like the data filtered by day?\nEnter monday, tuesday, wednesday, thursday, friday, (or just ENTER to include all days)  ")
        
        day = day.lower()
        if day == "":
            day = 'all'
            break
        elif day in DAY_DATA:
            break
        else:
            print ("Not a valid input: Please try again\n")

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    print('\nPlease wait loading the data from csv file(s)...\n')

    # load data file into a dataframe
    #if debug:  print ('The city:  {} and the associated file: {}'.format(city, CITY_DATA[city]))
    df = pd.DataFrame({})
    if city == 'all':
        for file in CITY_DATA.keys():
            df1 = pd.read_csv(CITY_DATA[file])
            if debug:  print("Shape: {}\n {}\n".format(df1.head(), df1.keys()))
            df = df.append(df1, sort=True)
            if debug: print(df.shape)
    else:
        df = pd.read_csv(CITY_DATA[city])
        if debug2: print(df.shape)

    if debug:   print ("the DataFrame: {}".format(df.shape))


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['monthb'] = df['month'].apply(lambda x: calendar.month_name[x].lower())
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if debug2:  print(df.head())
          
    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe        
        df = df[df.monthb ==  month]
        
        # filter by month and return only the Start Time column
        #df = df.loc[df.month == month, 'Start Time']
        if debug: print ("MONTH: the new dataframe: \n{}".format(df.shape))


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df.day_of_week ==  day.title()]
    if debug: print ("DAY:  the new dataframe: \n{}".format(df.shape))
    if debug2:  print (df.day_of_week,"\n",df.head())
    
    print('\n {} BIKESHARE DATA {} \n'.format(('-'*10),('-'*10)))
    print('FILTERED BY:')
    print('{} CITY: {}'.format((' '*5),city.title()))
    print('{} MONTH: {}'.format((' '*5),month.title()))
    print('{} DAY: {}\n'.format((' '*5),day.title()))

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nMost Frequent Times of Travel...\n')
    start_time = time.time()
    
    # TO DO: display the most common month
    common_month = df['monthb'].value_counts().idxmax()
    print ("{} Most Frequent Month: {}".format((' '*5),common_month.title()))

    # TO DO: display the most common day of week
    common_week = df['day_of_week'].value_counts().idxmax()
    print ("{} Most Frequent Day of the Week: {}".format((' '*5), common_week))


    # TO DO: display the most common start hour
    common_starthour = df['hour'].value_counts().idxmax()
    print ("{} Most Frequent Start Hour: {}".format((' '*5), common_starthour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    #print (df.head(15))
    print('\nMost Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_startstation = df['Start Station'].value_counts().idxmax()
    print ("{} Popular Start Station: {}".format((' '*5),common_startstation))


    # TO DO: display most commonly used end station
    #print (df['End Station'].value_counts().head(15))
    common_endstation = df['End Station'].value_counts().idxmax()
    print ("{} Popular End Station: {}".format((' '*5), common_endstation))


    # TO DO: display most frequent combination of start station and end station trip
    
    common_startend = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print ("{} Popular Start & End Station: {} and {}".format((' '*5), common_startend[0], common_startend[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nTrip Duration...\n')
    start_time = time.time()
  
    #df1 = df.loc[:, ['Trip Duration', 'User Type']]
    #print (df1.head(15))
    #print (df.shape)
    # TO DO: display total travel time
    trip_duration = df['Trip Duration'].count()
    print("{} Total Trip Duration: {} secs".format((' '*5), trip_duration))

    # TO DO: display mean travel time
    print("{} Average Trip Duration: {} secs".format((' '*5), df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nUser Stats...\n')
    isGender = 'Gender' in df.keys()
    isDOB = 'Birth Year' in df.keys()
    if debug: print ('Checking if all columns exist: Gender: {}, DOB: {}'.format(isGender, isDOB))
    if isGender and isDOB:
        start_time = time.time()
        if debug:  print(df['Birth Year'].value_counts())
        oyear = int(df['Birth Year'].min())
        yyear = int(df['Birth Year'].max())
        if debug: print(oyear)
        if debug: print(yyear)

        # TO DO: Display counts of user types
        print( "Bikeshare Riders by User Type: \n{}\n\n".format(df['User Type'].value_counts()))
    
        # TO DO: Display counts of gender
        print("Bikeshare Riders by Gender: \n{}".format(df['Gender'].value_counts()))
    
        # TO DO: Display earliest, most recent, and most common year of birth
        print("\nOldest Bikeshare rider: {} (born: {})".format(2019-oyear,oyear))
        print("Youngest Bikeshare rider: {} (born: {})".format(2019-yyear, yyear))
    
        # print ("Average Age of Bikeshare rider: {}")
        print("Average age of Bikeshare riders: {}\n".format(2019-int(df['Birth Year'].mean())))
    
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        print (" NO USER DATA AVAILABLE ")



def display_raw(df):
        """Displays raw data per users request."""
        # TO DO: get user input for seeing the raw data
        response = input("Would you like to see raw data? Please enter yes, no or just ENTER to see raw data")
        numRows = df.shape[0]
        print ("TOTAL number of rows: {}".format(numRows))
        startrow = 0
        endrow = startrow + ROWINCREMENT
        while response == True or response == 'yes' or response == "":
            print( "Displaying Raw Data: rows {} through {}\n{}".format(startrow, endrow,df.iloc[startrow:endrow]))
            response = input("Like more data? Please enter yes, no or just ENTER to see raw data  ")
            temprow = endrow
            startrow = endrow
            if endrow > numRows:
                endrow = numRows
                break
            else:
                endrow =temprow + ROWINCREMENT
        

def main():
    while True:
        city, month, day = get_filters()
#        city = "chicago"
#        month = "june"
#        day = "thursday"
        df = load_data(city, month, day)
        display_raw(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
