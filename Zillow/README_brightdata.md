# Brightdata API Integration for Zillow Scraping

This documentation explains how to use the Brightdata API integration (`brightdata_api.py`) for scraping Zillow data.

## Overview

The script `brightdata_api.py` automates the process of fetching data from Zillow using Brightdata's web scraping service. It handles:
- Making API requests to Brightdata
- Waiting for data processing
- Saving results to JSON files

## Prerequisites

1. Python 3.x
2. Required packages (install via `pip`):
   ```
   requests
   python-dotenv
   ```
3. Brightdata API token (stored in `.env` file)

## How It Works

### 1. Environment Setup
The script uses a `.env` file to store your Brightdata API token:
```
BRIGHTDATA_API_TOKEN=your_token_here
```

### 2. Main Script Flow (`brightdata_api.py`)

#### a. Initial API Call
- Makes a POST request to Brightdata's trigger endpoint
- Sends the target Zillow URL
- Receives a `snapshot_id` for tracking the scraping job

#### b. Data Retrieval
- Uses the `snapshot_id` to check job status
- Implements retry logic (12 attempts, 10 seconds apart)
- Handles different response types (list vs status updates)

#### c. Data Storage
- Creates a `data` directory if it doesn't exist
- Saves results in JSON format with timestamp
- Example filename: `zillow_data_20240315_143022.json`

### 3. Response Handling

The script handles two types of responses:

1. List Response (Success):
   - Contains actual scraped data
   - Saves complete dataset
   - Shows sample of first item
   - Reports total items received

2. Status Response:
   - `running`: Job still processing
   - `success/completed`: Job finished
   - Other statuses: Handled as unexpected

## Usage

1. Ensure your `.env` file is set up with your API token
2. Run the script:
   ```bash
   python brightdata_api.py
   ```

### Example Output
```
Got snapshot ID: s_xxxxx
Attempt 1/12 to get data...
Data still processing, waiting 10 seconds...

Success! Final Response:
First item in response (sample):
{
    // Sample data here
}

Total items received: X
Data saved to: data/zillow_data_20240315_143022.json
```

## Data Storage

- All scraped data is saved in the `data/` directory
- Files are named with pattern: `zillow_data_YYYYMMDD_HHMMSS.json`
- Data is stored in JSON format with proper indentation
- Each file contains the complete response from Brightdata

## Error Handling

The script includes robust error handling:
- API connection issues
- Empty responses
- Processing timeouts
- Unexpected response formats

## Limitations

- Maximum retry attempts: 12 (approximately 2 minutes)
- One URL per request
- Responses capped by Brightdata's limits

## Troubleshooting

1. If script fails immediately:
   - Check your API token
   - Verify internet connection
   - Ensure `.env` file is properly formatted

2. If script times out:
   - Site might be blocking scraping
   - Brightdata might be experiencing delays
   - Try increasing `max_retries` if needed
