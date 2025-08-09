# scraper_debug.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

def fetch_case_data(case_type, case_number, filing_year, debug_write=True):
    base = "https://services.ecourts.gov.in/ecourtindia_v6/"
    post_url = urljoin(base, "cases/case_no.php")  # your current endpoint

    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Referer": base
    }
    session.headers.update(headers)

    # Do an initial GET to establish session/cookies (helps some servers)
    try:
        session.get(base, timeout=15)
    except Exception:
        pass

    payload = {
        "state_cd": "HR",
        "dist_cd": "2",
        "court_complex_code": "1",
        "case_type": (case_type or "").upper(),
        "case_number": case_number or "",
        "case_year": filing_year or ""
    }

    try:
        resp = session.post(post_url, data=payload, timeout=20)
    except Exception as e:
        raise Exception(f"HTTP POST failed: {e}")

    html = resp.text
    if debug_write:
        with open("debug_response.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Saved full response to debug_response.html")

    # quick checks
    low = html.lower()
    if "captcha" in low or "access denied" in low or "forbidden" in low:
        raise Exception("Blocked by site (captcha / access denied). Try Selenium.")
    if "no record" in low or "no records" in low or "not found" in low:
        raise ValueError("No case found for the provided inputs (site returned no record).")

    soup = BeautifulSoup(html, "html.parser")

    # Flexible parsing: search tables for label-like cells
    data = {}
    found_parties = False

    # scan all tables/rows and normalize label text
    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            cols = row.find_all(["td", "th"])
            if len(cols) >= 2:
                label = cols[0].get_text(" ", strip=True).lower()
                value = cols[1].get_text(" ", strip=True)
                if any(k in label for k in ["petitioner", "petitioner/respondent", "petitioner vs", "parties"]):
                    data["parties"] = value
                    found_parties = True
                if any(k in label for k in ["filing", "date of filing", "filing date", "filed on"]):
                    data["filing_date"] = value
                if any(k in label for k in ["next hearing", "next date", "next hearing date"]):
                    data["next_hearing"] = value

    # fallback regex for parties "X v Y"
    if not found_parties:
        m = re.search(r'([A-Z][\w\s\.\-&]{2,}?)\s+v(?:s|ersus|s\.)\.?\s+([A-Z][\w\s\.\-&]{2,}?)', html, re.I)
        if m:
            data["parties"] = m.group(0).strip()

    # find a PDF link if present
    pdf_link = None
    a_view = soup.find("a", string=re.compile(r'view|download', re.I))
    if a_view and a_view.get("href"):
        pdf_link = urljoin(resp.url, a_view["href"])
    else:
        a_pdf = soup.find("a", href=re.compile(r'\.pdf', re.I))
        if a_pdf and a_pdf.get("href"):
            pdf_link = urljoin(resp.url, a_pdf["href"])

    # last resort: find last meaningful anchor in tables
    if not pdf_link:
        for t in soup.find_all("table")[::-1]:
            a = t.find("a", href=True)
            if a:
                href = a["href"]
                if ".pdf" in href.lower() or "view" in a.get_text("").lower():
                    pdf_link = urljoin(resp.url, href)
                    break

    if not data and not pdf_link:
        raise Exception("Unexpected response format or missing data. Open debug_response.html and inspect.")

    result = {
        "Parties": data.get("parties", ""),
        "Filing Date": data.get("filing_date", ""),
        "Next Hearing": data.get("next_hearing", ""),
        "PDF": pdf_link or ""
    }
    return result, html


# quick CLI test
if __name__ == "__main__":
    try:
        d, html = fetch_case_data("CIS", "1", "2023", debug_write=True)
        print("Parsed:", d)
    except Exception as e:
        print("ERROR:", e)
