import requests
import datetime
import pandas as pd
import calendar


# Helper functions
def most_frequent(original_list):
    return max(set(original_list), key=original_list.count)


def remove_duplicates(original_list):
    new_list = []

    for element in original_list:
        if element not in new_list:
            new_list.append(element)

    return new_list


# Returns a customisable string for what we should prepare for
def preparation(min_temp, rain):
    temp_message = ''
    condition_message = 'have a nice day!'

    # Checks the temperature
    if min_temp <= 0:
        temp_message = 'Wear a jacket'
    elif 0 < min_temp <= 10:
        temp_message = 'Wear a light jacket'
    elif 10 < min_temp <= 20:
        temp_message = 'Wear something casual'
    elif 20 < min_temp <= 30:
        temp_message = 'It\'s hot, wear something light'
    elif min_temp > 30:
        temp_message = 'Go hide in the shade'

    # Checks the rain

    if rain > 5.0:
        condition_message = 'remember to bring and umbrella!'

    return temp_message + ' & ' + condition_message


def get_weather(cityname):
    # API key and base url required for this to work
    API_KEY = 'YOUR_API_KEY'
    base_url = 'https://api.openweathermap.org/data/2.5/forecast'

    # Make the request with the specified parameters
    payload = {'q': cityname, 'appid': API_KEY, 'units': 'metric'}
    request = requests.get(url=base_url, params=payload)
    data = request.json()

    date_list, time_list, temp_list, condition_list, rain_list = [], [], [], [], []

    # Finds what we need from the API
    for item in data['list']:
        timestamp = item['dt']
        weather_condition = item['weather'][0]['description']
        temperature = item['main']['temp']

        try:
            rain = item['rain']['3h']
        except Exception:
            rain = 0.0

        # Makes it so we can use the date and time later
        converted_timestamp = datetime.datetime.fromtimestamp(timestamp)
        time = converted_timestamp.time()
        current_date = converted_timestamp.date()

        # Adds all the elements we want to the proper list
        date_list.append(str(current_date))
        time_list.append(time)
        temp_list.append(temperature)
        condition_list.append(weather_condition)
        rain_list.append(rain)

    # Cleans our data for the DataFrame
    raw_data = {
        'date': date_list,
        'time': time_list,
        'temp': temp_list,
        'conditions': condition_list,
        'rain': rain_list
    }

    # Creates a DataFrame
    df = pd.DataFrame(raw_data)
    print(df)

    dates = remove_duplicates(date_list)
    for current_date in dates:
        new_df = df[df['date'].str.contains(current_date)]
        # print(new_df)
        print()
        min_temp, max_temp = min(new_df.temp), max(new_df.temp)
        total_rain = round(sum(new_df.rain), 2)
        average_weather = most_frequent(new_df.conditions.tolist())

        # Gets the day of the week from the calendar
        t_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
        day_of_week = calendar.day_name[t_date.weekday()]

        # Display all the data
        print(f'{t_date.day} {day_of_week}')
        print('-- Weather:', average_weather, f'(Rain: {total_rain}mm)')
        print(f'-- Min: {min_temp}°C -> Max: {max_temp}°C')
        print('--', preparation(min_temp, total_rain))

    # Returns a DataFrame
    return df


get_weather(cityname='Copenhagen')
