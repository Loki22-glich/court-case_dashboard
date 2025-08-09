# Court Case Dashboard

This project is a **Python + Selenium + Flask** based dashboard that fetches case details from an Indian High Court website (in this setup, tested with Telangana High Court) and displays them in a user-friendly format.

It also implements **local caching** to avoid repeatedly fetching the same data, improving speed and reducing website load.

---

## Features

- **Automated case search** using Selenium.
- **Web scraping** to extract case details.
- **Local cache system** to store previously fetched results.
- **Flask web interface** to view and filter results.
- **Error handling** for missing data or unexpected site behavior.

---

## Folder / File Structure

court-case_dashboard/
│
├── app.py # Flask web server
├── fetch_cases.py # Selenium scraping script
├── cache.json # Stores cached results to avoid re-fetching
├── templates/
│ └── dashboard.html # HTML template for displaying cases
├── static/ # (Optional) CSS, JS, images
└── README.md # Project documentation


---

## How Caching Works

The `cache.json` file is a **local data storage** that keeps a record of all the fetched case details in JSON format.  

- When you request a case:
  - First, the program **checks** if it exists in `cache.json`.
  - If **found**, it loads from cache (much faster).
  - If **not found**, it fetches from the court website, then saves the result in the cache for future use.

**Example cache.json:**
json
{
  "CRLA-1234-2023": {
    "petitioner": "John Doe",
    "respondent": "State of Telangana",
    "status": "Pending",
    "last_hearing": "2025-08-01"
  }
}
Code Overview
1. fetch_cases.py
Handles Selenium automation to visit the court website.

Fills in the case type, number, and year.

Extracts results from the table using BeautifulSoup.

Returns results to be displayed or saved in cache.

2. app.py
Runs a Flask web app.

Routes:

/ → Home page with form to enter case details.

/search → Processes the form, checks cache, fetches if needed.

Passes data to dashboard.html for display.

3. dashboard.html
Displays the case details in a table format.

Allows basic styling for readability.

📌 Why Use a Cache File?
Speeds up repeated queries

Reduces server load on the court website

Prevents unnecessary Selenium launches


Installation & Setup
1. Clone the repository
bash
Copy code
git clone https://github.com/<your-username>/court-case_dashboard.git
cd court-case_dashboard
2. Install dependencies
bash
Copy code
pip install -r requirements.txt
(Requirements file should include Flask, Selenium, BeautifulSoup, requests, etc.)

3. Run the Flask app
bash
Copy code
python app.py
4. Open in browser
Go to:

cpp
Copy code
http://127.0.0.1:5000
Example Use
Select a Case Type (e.g., CRLA).

Enter case number and year.

Click "Search".

Dashboard displays the case details.

Next time you search the same case, it will load instantly from cache.json.

Notes
Ensure ChromeDriver is installed and matches your Chrome browser version.

Clear cache.json if you want to fetch updated case data from the website.

Website structure changes may require small adjustments in fetch_cases.py.
