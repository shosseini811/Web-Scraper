# Zillow Web Scraper

This project is a web scraper for Zillow's Cleveland, OH real estate listings. It uses the ScrapingBee API to fetch and parse property data.

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Create a `.env` file in the `Zillow` directory with the following content:
     ```
     SCRAPINGBEE_API_KEY=your_api_key_here
     ```
   - Replace `your_api_key_here` with your actual ScrapingBee API key.

4. **Run the scraper**
   ```bash
   python Zillow/cleveland.py
   ```

## Disclaimer

This project is intended for educational purposes only. Web scraping may violate the terms of service of the website being scraped. Ensure you have the right to scrape the data and comply with all legal requirements. The author is not responsible for any misuse of this tool.
