import requests
import json
import time
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Your API token
API_TOKEN = os.getenv('BRIGHTDATA_API_TOKEN')

def save_to_file(data, prefix="zillow_data"):
    # Create 'data' directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/{prefix}_{timestamp}.json"
    
    # Save data to file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    return filename

def fetch_data():
    # First API call to trigger the dataset
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    # URL data
    data = [{
        "url": "https://www.zillow.com/cleveland-oh/"
    }]
    
    # Make the first API call
    first_response = requests.post(
        "https://api.brightdata.com/datasets/v3/trigger",
        params={
            "dataset_id": "gd_lfqkr8wm13ixtbd8f5",
            "include_errors": "true"
        },
        headers=headers,
        json=data
    )
    
    # Check if the first call was successful
    if first_response.status_code != 200:
        print(f"Error in first API call: {first_response.text}")
        return
    
    # Extract the snapshot ID
    snapshot_data = first_response.json()
    snapshot_id = snapshot_data.get('snapshot_id')
    print(f"Got snapshot ID: {snapshot_id}")
    
    # Try to get the data with retries
    max_retries = 12  # Will try for about 2 minutes (12 times * 10 seconds)
    for attempt in range(max_retries):
        print(f"\nAttempt {attempt + 1}/{max_retries} to get data...")
        
        try:
            # Second API call to get the data using the snapshot ID
            second_response = requests.get(
                f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}",
                params={"format": "json"},
                headers=headers
            )
            
            # Parse the response
            response_data = second_response.json()
            
            # If response_data is a list, check its content
            if isinstance(response_data, list):
                if not response_data:  # If list is empty
                    print("Data still processing (empty response), waiting 10 seconds...")
                    time.sleep(10)
                    continue
                else:
                    print("\nSuccess! Final Response:")
                    # Print first item as sample (you can modify this based on your needs)
                    print("First item in response (sample):")
                    print(json.dumps(response_data[0], indent=2))
                    print(f"\nTotal items received: {len(response_data)}")
                    
                    # Save the data to a file
                    saved_file = save_to_file(response_data)
                    print(f"\nData saved to: {saved_file}")
                    return
            
            # If it's not a list, check for status (old logic)
            status = response_data.get('status')
            if status == 'running':
                print("Data still processing, waiting 10 seconds...")
                time.sleep(10)
                continue
            elif status == 'success' or status == 'completed':
                print("\nSuccess! Final Response:")
                print(json.dumps(response_data, indent=2))
                
                # Save the data to a file
                saved_file = save_to_file(response_data)
                print(f"\nData saved to: {saved_file}")
                return
            else:
                print(f"\nUnexpected status: {status}")
                print("Response data:")
                print(json.dumps(response_data, indent=2))
                return
                
        except Exception as e:
            print(f"Error during attempt {attempt + 1}: {str(e)}")
            time.sleep(10)
            continue
    
    print("\nTimed out waiting for data to be ready after all attempts")

if __name__ == "__main__":
    fetch_data() 