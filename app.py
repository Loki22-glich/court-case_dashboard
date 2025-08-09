from flask import Flask, render_template, request
from scraper_debug import fetch_case_data

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    error = None

    if request.method == "POST":
        case_type = request.form.get("case_type")
        case_number = request.form.get("case_number")
        filing_year = request.form.get("filing_year")

        try:
            data, _ = fetch_case_data(case_type, case_number, filing_year)
        except Exception as e:
            error = str(e)

    return render_template("index.html", data=data, error=error)

if __name__ == "__main__":
    app.run(debug=True)

