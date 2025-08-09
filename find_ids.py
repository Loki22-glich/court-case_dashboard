from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Reuse the working setup from your scraper_selenium.py
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")

try:
    # Wait for form to appear
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.TAG_NAME, "form"))
    )

    # Get visible inputs
    inputs = driver.find_elements(By.TAG_NAME, "input")
    selects = driver.find_elements(By.TAG_NAME, "select")

    print("\n--- VISIBLE INPUT FIELDS ---")
    for inp in inputs:
        if inp.is_displayed():
            print(f"ID: {inp.get_attribute('id')} | NAME: {inp.get_attribute('name')} | TYPE: {inp.get_attribute('type')}")

    print("\n--- VISIBLE SELECT FIELDS ---")
    for sel in selects:
        if sel.is_displayed():
            print(f"ID: {sel.get_attribute('id')} | NAME: {sel.get_attribute('name')}")

except Exception as e:
    print("Error: Form not loaded properly.", e)

input("\nPress Enter to close browser...")
driver.quit()
