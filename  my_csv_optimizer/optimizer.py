import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

def get_code_from_location(location_input):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv('Book3.csv')

    # Search for the location in the DataFrame
    matched_row = df[df['local'] == location_input]
    if not matched_row.empty:
        code = str(matched_row.iloc[0]['code'])  # Convert code to string
        return code
    else:
        return None

def main():
    # Ask the user to enter a location
    location_input = input("Enter location: ")

    # Get the code corresponding to the input location
    code = get_code_from_location(location_input)
    if code is not None:
        print(f"Code for {location_input}: {code}")
        # Construct the URL based on the code
        url = f'https://tenki.jp/forecast/3/16/4410/{code}/'
        print(f"URL: {url}")

        # Fetch weather data for the location
        weather_data = fetch_weather_data(url)
        if weather_data:
            # Print or save the weather data as needed
            print(json.dumps(weather_data, ensure_ascii=False, indent=4))
        else:
            print(f"Error fetching weather data for {location_input}: Weather data not found on the page")
    else:
        print(f"Error: Could not find code for {location_input}. Please try again with a different location.")

def fetch_weather_data(url):
    # Fetch weather data from the URL
    r_location = requests.get(url)
    location_soup = BeautifulSoup(r_location.text, 'html.parser')

    # Parse the weather data
    try:
        weather_data = parse_weather(location_soup)
        return weather_data
    except Exception as e:
        print(f"Error parsing weather data: {e}")
        return None

def parse_weather(soup):
    data = {}
    
    # Extract location name
    location = soup.title.text.split('の')[0]
    data['location'] = location + 'の天気'
    
    # Extract today and tomorrow's forecast if available
    today_soup = soup.select('.today-weather')
    tomorrow_soup = soup.select('.tomorrow-weather')
    
    if today_soup and tomorrow_soup:
        data['today'] = forecast2dict(today_soup[0])
        data['tomorrow'] = forecast2dict(tomorrow_soup[0])
    else:
        raise Exception("Weather data not found on the page")
    
    return data

def forecast2dict(soup):
    data = {}
    
    # Extract date
    date_text = soup.select('.left-style')[0].text
    date_pattern = r"(\d+)月(\d+)日\(([土日月火水木金])+\)"
    date_match = re.search(date_pattern, date_text)
    if date_match:
        month, day, day_of_week = date_match.groups()
        data['date'] = f"{month}-{day}({day_of_week})"
    
    # Extract weather details
    data['weather'] = soup.select('.weather-telop')[0].text.strip()
    data['high_temp'] = soup.select("[class='high-temp temp']")[0].text.strip()
    data['high_temp_diff'] = soup.select("[class='high-temp tempdiff']")[0].text.strip()
    data['low_temp'] = soup.select("[class='low-temp temp']")[0].text.strip()
    data['low_temp_diff'] = soup.select("[class='low-temp tempdiff']")[0].text.strip()
    
    rain_probabilities = soup.select('.rain-probability > td')
    data['rain_probability'] = {f"{i*6:02}-{(i+1)*6:02}": prob.text.strip() for i, prob in enumerate(rain_probabilities)}
    
    data['wind_wave'] = soup.select('.wind-wave > td')[0].text.strip()
    
    return data

if __name__ == '__main__':
    main()

