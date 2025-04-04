import os
import time
from datetime import datetime
import pandas as pd
import requests
from dotenv import load_dotenv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

class AmforiScraper:
    def __init__(self):
        self.base_url = "https://platform.amfori.org"
        self.sso_url = "https://sso.amfori.org"
        self.target_url = "https://platform.amfori.org/ui/monitoring/monitoring-partner-planning/ongoing"
        self.excel_file = "amfori_data.xlsx"
        self.setup_driver()
        
    def setup_driver(self):
        print("Setting up Chrome driver...")
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')  # Comment out headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # ChromeDriver path from Homebrew
        chromedriver_path = '/opt/homebrew/bin/chromedriver'
        
        # Verify ChromeDriver exists
        if not os.path.exists(chromedriver_path):
            raise Exception(f"ChromeDriver not found at {chromedriver_path}. Please install it using: brew install chromedriver")
        
        try:
            print(f"Using ChromeDriver at: {chromedriver_path}")
            service = Service(executable_path=chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
            print("ChromeDriver initialized successfully")
        except Exception as e:
            print(f"Error setting up Chrome driver: {str(e)}")
            print("Please make sure ChromeDriver is installed and matches your Chrome version")
            print("You can check Chrome version with: /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --version")
            print("And install matching ChromeDriver with: brew install chromedriver")
            raise
            
        self.wait = WebDriverWait(self.driver, 30)
        print("WebDriverWait initialized with 30 second timeout")
        
    def login(self):
        print("Logging in...")
        try:
            # Load credentials from .env file
            load_dotenv()
            username = os.getenv("AMFORI_USERNAME")
            password = os.getenv("AMFORI_PASSWORD")
            
            if not username or not password:
                raise ValueError("Please set AMFORI_USERNAME and AMFORI_PASSWORD in .env file")
            
            # Navigate to SSO login page
            print("Navigating to SSO login page...")
            login_url = f"{self.sso_url}/auth/realms/amfori/protocol/openid-connect/auth"
            params = {
                'client_id': 'sustainability-platform',
                'response_type': 'code',
                'scope': 'openid',
                'redirect_uri': self.target_url,
                'state': 'a28d7a40-cd22-4662-9c76-03d7ec5a52dd',
                'nonce': 'dc68a6eb-8948-43d2-822c-2be129ae83e6'
            }
            self.driver.get(f"{login_url}?{requests.compat.urlencode(params)}")
            
            # Wait for login form and enter credentials
            print("Waiting for login form...")
            username_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-control[name='username']"))
            )
            password_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-control[name='password']"))
            )
            
            print("Entering credentials...")
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)
            
            # Click login button
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-primary.btn-lg.w-100[name='login']"))
            )
            login_button.click()
            
            # Wait for redirect to complete
            print("Waiting for redirect...")
            self.wait.until(lambda driver: driver.current_url.startswith(self.target_url))
            print("Login successful!")
            
        except Exception as e:
            print(f"Login failed: {str(e)}")
            self.driver.save_screenshot("login_error.png")
            raise
            
    def apply_filters(self):
        print("Applying filters...")
        try:
            # Wait for filter section to be visible
            filter_section = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".filter-section"))
            )
            
            # Click "More criteria" button if it exists
            try:
                more_criteria = self.driver.find_element(By.XPATH, "//button[contains(text(), 'More criteria')]")
                more_criteria.click()
                time.sleep(2)
            except:
                print("No 'More criteria' button found, continuing...")
            
            # Select country
            country_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//mat-form-field[contains(., 'Country')]"))
            )
            country_field.click()
            time.sleep(1)
            
            # Search and select China
            search_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search']")
            search_input.send_keys("China")
            time.sleep(1)
            
            china_option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//mat-option[contains(., 'China')]"))
            )
            china_option.click()
            
            # Select initiatives
            initiative_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//mat-form-field[contains(., 'Initiative')]"))
            )
            initiative_field.click()
            time.sleep(1)
            
            # Select BSCI
            bsci_option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//mat-option[contains(., 'BSCI')]"))
            )
            bsci_option.click()
            
            # Select QMI
            qmi_option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//mat-option[contains(., 'QMI')]"))
            )
            qmi_option.click()
            
            # Click Apply button
            apply_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Apply')]")
            apply_button.click()
            
            # Wait for results to load
            time.sleep(5)
            print("Filters applied successfully")
            
        except Exception as e:
            print(f"Error applying filters: {str(e)}")
            self.driver.save_screenshot("filter_error.png")
            raise
            
    def extract_table_data(self):
        print("Extracting table data...")
        data = []
        
        try:
            # Wait for table to be visible
            table = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
            )
            
            # Get all rows
            rows = table.find_elements(By.TAG_NAME, "tr")
            
            for row in rows[1:]:  # Skip header row
                try:
                    # Extract data from cells
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) < 2:  # Skip rows without enough cells
                        continue
                        
                    # Get site name and remove any icon elements
                    site_name = cells[1].text
                    site_name = site_name.split('\n')[0]  # Remove any additional text
                    
                    # Get link
                    link = cells[1].find_element(By.TAG_NAME, "a").get_attribute("href")
                    
                    # Get site ID from the link
                    site_id = link.split("/")[-1]
                    
                    row_data = {
                        'Site amfori ID': site_id,
                        'Site Name': site_name,
                        'Link': link,
                        'Created At': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'Updated At': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'Scraped At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    data.append(row_data)
                    print(f"Extracted data for site: {site_name}")
                    
                except Exception as e:
                    print(f"Error extracting row data: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error extracting table data: {str(e)}")
            self.driver.save_screenshot("table_error.png")
            raise
            
        return data
        
    def update_excel(self, new_data):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            existing_df = pd.read_excel(self.excel_file)
        except FileNotFoundError:
            existing_df = pd.DataFrame()
            
        # Convert new data to DataFrame
        new_df = pd.DataFrame(new_data)
        
        if existing_df.empty:
            # If no existing data, save new data
            new_df.to_excel(self.excel_file, index=False)
        else:
            # Update existing records and add new ones
            for idx, row in new_df.iterrows():
                mask = existing_df['Site amfori ID'] == row['Site amfori ID']
                if mask.any():
                    # Update existing record
                    for col in row.index:
                        if col not in ['Created At']:  # Don't update creation date
                            existing_df.loc[mask, col] = row[col]
                    existing_df.loc[mask, 'Updated At'] = current_time
                    existing_df.loc[mask, 'Scraped At'] = current_time
                else:
                    # Add new record
                    existing_df = pd.concat([existing_df, pd.DataFrame([row])], ignore_index=True)
            
            existing_df.to_excel(self.excel_file, index=False)
            
    def scrape(self):
        try:
            self.login()
            self.apply_filters()
            data = self.extract_table_data()
            self.update_excel(data)
            print("Scraping completed successfully!")
            
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            raise
        finally:
            self.driver.quit()

if __name__ == "__main__":
    scraper = AmforiScraper()
    scraper.scrape() 