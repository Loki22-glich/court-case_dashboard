🏛 Court Case Dashboard
A Flask + Selenium based dashboard to fetch and display court case details from official High Court websites.
This project automates form submissions, retrieves case data, and shows it in a user-friendly format.

📌 Features
Automated Data Fetching using Selenium.

Dynamic Search by case type, number, and filing year.

Caching to store previously fetched results (reduces repeated requests).

Flask Web Interface for easy access in any browser.

📂 Project Structure
bash
Copy code
court-case_dashboard/
│
├── app.py               # Main Flask application
├── scraper.py           # Selenium automation script
├── cache.json           # Stores fetched case data
├── requirements.txt     # Python dependencies
├── templates/
│   ├── index.html        # Main input form UI
│   └── results.html      # Page to display results
└── README.md             # This file
⚙️ How It Works
User enters search details (case type, number, filing year) in the web form.

Flask sends the details to scraper.py.

Selenium opens the court website and fills in the form automatically.

Case details are extracted and stored in cache.json.

Next time the same case is searched, data is loaded directly from cache (faster & avoids website load).

📜 File-by-File Explanation
app.py
The heart of the project.

Runs the Flask server.

Handles routes:

/ → Shows the search form.

/results → Displays fetched case data.

Calls the scraper to get new results if the case isn’t in the cache.

scraper.py
Uses Selenium WebDriver to:

Open the High Court website.

Select case type from dropdown.

Enter case number & filing year.

Click submit and scrape the table data.

Returns the extracted case details back to Flask.

cache.json
Stores previously fetched case details in JSON format:

json
Copy code
{
  "CRLA-123-2023": {
    "case_type": "CRLA",
    "case_number": "123",
    "year": "2023",
    "status": "Pending",
    "next_hearing": "2025-09-15"
  }
}
💡 Why Cache?

If you search the same case again, the scraper won’t run — data is fetched instantly.

Reduces server load and prevents unnecessary requests to the court website.

templates/index.html
Contains the HTML form for user input.

Has dropdown for case type, text inputs for case number & year.

templates/results.html
Displays case details in a clean table format.

🚀 How to Run Locally
Clone the repo

bash
Copy code
git clone https://github.com/your-username/court-case_dashboard.git
cd court-case_dashboard
Install dependencies

bash
Copy code
pip install -r requirements.txt
Run the app

bash
Copy code
python app.py
Open in browser

cpp
Copy code
http://127.0.0.1:5000
🛠 Requirements
Python 3.8+

Flask

Selenium

ChromeDriver (matching your Chrome version)

📌 Future Improvements
Add pagination support.

Improve error handling if the court site is down.

Support for multiple states’ High Courts.
