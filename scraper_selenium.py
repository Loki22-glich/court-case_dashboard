from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Setup Chrome driver ---
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")  # Change if different court site

try:
    wait = WebDriverWait(driver, 30)

    # 1️⃣ Wait for and click the "Case Type" tab button
    case_type_button = wait.until(
        EC.element_to_be_clickable((By.ID, "casetype-tabMenu"))
    )
    case_type_button.click()

    # 2️⃣ Wait for case type dropdown and select value
    case_type_dropdown = wait.until(
        EC.presence_of_element_located((By.ID, "case_type"))
    )
    Select(case_type_dropdown).select_by_visible_text("WP")  # Change "WP" as needed

    # 3️⃣ Fill in case number
    driver.find_element(By.ID, "case_no").send_keys("123")  # Change as needed

    # 4️⃣ Fill in filing year
    driver.find_element(By.ID, "case_year").send_keys("2024")  # Change as needed

    # 5️⃣ Click search
    driver.find_element(By.ID, "search_button").click()

    # 6️⃣ Wait for results to appear
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    print("\n✅ Search completed and results loaded.")

except Exception as e:
    print("❌ Error during automation:", e)

# Keep browser open until you press Enter
input("\nPress Enter to close browser...")
driver.quit()
