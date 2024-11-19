import requests
import pandas as pd

# NASA API setup
api_key = "key"
url = "https://api.nasa.gov/neo/rest/v1/feed"

# Function to fetch asteroid data
def fetch_asteroid_data(start_date, end_date):
    # Parameters for the API request
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': api_key
    }

    # Send GET request
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()

        # Parse JSON data
        asteroid_data = data['near_earth_objects']
        asteroid_list = []
        for date, asteroids in asteroid_data.items():
            for asteroid in asteroids:
                asteroid_list.append({
                    'id': asteroid['id'],
                    'name': asteroid['name'],
                    'close_approach_date': date,
                    'estimated_diameter_m': asteroid['estimated_diameter']['meters']['estimated_diameter_max'],
                    'velocity_kph': asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'],
                    'miss_distance_km': asteroid['close_approach_data'][0]['miss_distance']['kilometers']
                })

        # Convert to DataFrame
        df = pd.DataFrame(asteroid_list)

        # Display summary statistics
        print("Summary Statistics:")
        print(df.describe())

        # Display DataFrame preview to confirm data
        print("DataFrame Preview:")
        print(df.head())

        # Save to CSV with absolute path
        df.to_csv(r'C:\Users\User\PycharmProjects\NASA API\asteroid_data.csv', index=False)
        print("Data saved to asteroid_data.csv")

        return df
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

# Example usage
if __name__ == "__main__":
    # Fetch asteroid data for a specific date range
    df = fetch_asteroid_data('2024-11-01', '2024-11-07')
