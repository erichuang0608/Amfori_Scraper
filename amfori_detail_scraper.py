import os
import time
import traceback
from datetime import datetime
import pandas as pd
import requests
from dotenv import load_dotenv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from amfori_scraper import AmforiScraper
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from database import Database

# 加载环境变量
load_dotenv()

class AmforiDetailScraper:
    def __init__(self):
        self.base_url = "https://platform.amfori.org"
        self.sso_url = "https://sso.amfori.org"
        self.target_url = "https://platform.amfori.org/ui/monitoring/monitoring-partner-planning/ongoing"
        self.api_url = f"{self.base_url}/v1/services/monitoring/monitoring-partner-plannings"
        self.excel_file = "amfori_detail_data.xlsx"
        self.backup_file = "amfori_detail_data_backup.xlsx"
        self.source_excel = "amfori_data.xlsx"
        self.session = requests.Session()
        self.driver = None
        self.token_file = "amfori_token.json"
        self.db = Database()
        self.setup_driver()
        
    def setup_driver(self):
        print("Setting up Chrome driver in headless mode...")
        options = webdriver.ChromeOptions()
        
        # 启用无头模式
        options.add_argument('--headless=new')  # 使用新版无头模式
        
        # 基本配置
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # 性能优化
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        
        # 内存优化
        options.add_argument('--disable-dev-tools')
        options.add_argument('--disable-logging')
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        
        # 禁用自动化标识
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 设置用户代理
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
        
        # ChromeDriver path from Homebrew
        #chromedriver_path = 'D:\Program Files\chromedriver-win64\chromedriver.exe'

        # ChromeDriver path from Homebrew
        chromedriver_path = '/opt/homebrew/bin/chromedriver'
        
        # 验证 ChromeDriver 是否存在
        if not os.path.exists(chromedriver_path):
            raise Exception(f"ChromeDriver not found at {chromedriver_path}. Please install it using: brew install chromedriver")
        
        try:
            print(f"Using ChromeDriver at: {chromedriver_path}")
            service = Service(executable_path=chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # 设置页面加载超时
            self.driver.set_page_load_timeout(30)
            # 设置脚本执行超时
            self.driver.set_script_timeout(30)
            
            print("ChromeDriver initialized successfully in headless mode")
        except Exception as e:
            print(f"Error setting up Chrome driver: {str(e)}")
            print("Please make sure ChromeDriver is installed and matches your Chrome version")
            print("You can check Chrome version with: /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --version")
            print("And install matching ChromeDriver with: brew install chromedriver")
            raise
            
        self.wait = WebDriverWait(self.driver, 30)
        print("WebDriverWait initialized with 30 second timeout")
        
    def login_and_get_token(self):
        """Login and get token, save it to file"""
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
            
            # Wait a bit for the page to fully load
            time.sleep(5)
            
            # Get all cookies
            print("Getting cookies...")
            cookies = self.driver.get_cookies()
            print(f"Found {len(cookies)} cookies")
            
            # Try to find the JWT security token in cookies
            jwt_token = None
            for cookie in cookies:
                print(f"Cookie name: {cookie['name']}")
                if cookie['name'] == 'JWT_SECURITY_TOKEN':
                    jwt_token = cookie['value']
                    print("Found JWT_SECURITY_TOKEN in cookies!")
                    break
            
            if jwt_token:
                # Save token to file
                token_data = {
                    'token': jwt_token,
                    'timestamp': datetime.now().isoformat()
                }
                with open(self.token_file, 'w') as f:
                    json.dump(token_data, f)
                print("Token saved to file")
                
                # Set up session headers
                self.session.headers.update({
                    'Authorization': f"Bearer {jwt_token}",
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                })
                print("Session headers updated successfully")
            else:
                print("No JWT token found in cookies")
                print("Current URL:", self.driver.current_url)
                print("Page source preview:", self.driver.page_source[:500])
                raise Exception("Failed to obtain JWT token")
            
            print("Login successful!")
            return True
            
        except Exception as e:
            print(f"Login failed: {str(e)}")
            self.driver.save_screenshot("login_error.png")
            raise
            
    def validate_token(self):
        """Check if token exists and is valid"""
        try:
            if not os.path.exists(self.token_file):
                print("No token file found")
                return False
                
            with open(self.token_file, 'r') as f:
                token_data = json.load(f)
                
            # Check if token exists
            if 'token' not in token_data:
                print("No token found in token file")
                return False
                
            # Set up session headers with token
            self.session.headers.update({
                'Authorization': f"Bearer {token_data['token']}",
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            })
            
            # Try to make a test request
            test_url = f"{self.base_url}/v1/services/monitoring/monitoring-partner-plannings/to-confirm/search"
            response = self.session.get(test_url, params={'rows': 1})
            
            if response.status_code == 401:
                print("Token is invalid or expired")
                return False
                
            print("Token is valid")
            return True
            
        except Exception as e:
            print(f"Error validating token: {str(e)}")
            return False
            
    def ensure_valid_token(self):
        """Ensure we have a valid token, login if necessary"""
        if not self.validate_token():
            print("Token invalid or missing, logging in...")
            self.login_and_get_token()
        else:
            print("Using existing valid token")
            
    def get_site_details(self, site_id):
        print(f"Fetching details for site {site_id}...")
        
        try:
            # 从数据库获取该站点的 To_Plan_Link
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT To_Plan_Link FROM sites WHERE Site_amfori_ID = ?", (site_id,))
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                print(f"No To_Plan_Link found for site {site_id}")
                return None
                
            url = result[0]
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching site details: {str(e)}")
            raise
            
    def extract_data(self, response_data):
        print("Extracting data from response...")
        data = []
        
        if response_data and isinstance(response_data, dict):
            try:
                # Get monitored site data
                monitored_site = response_data.get('monitoredSite', {})
                contact_details = monitored_site.get('contactDetails', {})
                
                # Get address components
                address = monitored_site.get('address', {})
                address_str = f"{address.get('street', '')}, {address.get('city', '')}, {address.get('zip', '')}, {address.get('country', '')}"
                
                # Get requestor data
                requestor = response_data.get('requestor', {})
                requestor_contact = requestor.get('contactDetails', {})
                
                # Get confirmed time window
                confirmed_time_window = response_data.get('confirmedTimeWindow', {})
                
                # Get unavailability days
                unavailability_days = response_data.get('unavailabilityDays', [])
                unavailability_days_str = ', '.join(str(day) for day in unavailability_days) if unavailability_days else ''
                
                # Get current time
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                row_data = {
                    'Scraped At': current_time,
                    'Status': 'New',  # 新记录状态为 New
                    'Request Date': response_data.get('requestDate', ''),
                    'Site amfori ID': monitored_site.get('siteAmforiId', ''),
                    'Monitoring ID': response_data.get('monitoringId', ''),
                    'Company Name(LegalName)': monitored_site.get('monitoredPartyLegalName', ''),
                    'Site Name(Sitename)': monitored_site.get('name', ''),
                    'Local Name(Localname)': monitored_site.get('localName', ''),
                    'Contact Email': contact_details.get('emailAddress', ''),
                    'Contact Phonenumber': contact_details.get('phoneNumber', ''),
                    'address': address_str,
                    'Audit Start window(confirmedTimeWindow-from)': confirmed_time_window.get('from', ''),
                    'Audit To window(confirmedTimeWindow-to)': confirmed_time_window.get('to', ''),
                    'Status1': '',
                    'Audit Start date': '',
                    'Audit End date': '',
                    'Unavailability Days': unavailability_days_str,
                    'Schedule#': '',
                    'Job#': '',
                    'BSCI MEMBER': requestor.get('legalName', ''),
                    'BSCI Member phonenumber': requestor_contact.get('phoneNumber', ''),
                    'BSCI Member emailAddress': requestor_contact.get('emailAddress', ''),
                    'Audit Announcement': response_data.get('announcementType', ''),
                    'Audit Methodology': response_data.get('monitoringActivityName', ''),
                    'Audit type': response_data.get('monitoringType', ''),
                    'CS': '',
                    'Remark（平台来单or CS来单）': '',
                    'Related Sales': '',
                    'Created At': current_time,
                    'Updated At': current_time
                }
                data.append(row_data)
                print(f"Successfully extracted data for site: {row_data['Site Name(Sitename)']}")
            except Exception as e:
                print(f"Error processing response data: {str(e)}")
                print("Response data:", response_data)
                raise
        else:
            print("Invalid response data format")
            print("Response data:", response_data)
            
        return data
        
    def update_site_status(self, site_id, status):
        """更新sites表中指定站点的状态为Extracted"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute("""
                UPDATE sites 
                SET Status_comparation = 'Extracted', 
                    Updated_At = ?, 
                    Scraped_At = ? 
                WHERE Site_amfori_ID = ?
            """, (current_time, current_time, site_id))
            
            conn.commit()
            print(f"Updated sites table status to 'Extracted' for site {site_id}")
        except Exception as e:
            print(f"Error updating site status: {str(e)}")
        finally:
            conn.close()

    def scrape(self):
        """入口1：抓取所有已确认的站点详情"""
        try:
            # 获取所有已确认的站点ID和URL
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Site_amfori_ID, To_Plan_Link FROM sites WHERE Status_comparation = 'Confirmed'")
            sites = cursor.fetchall()
            conn.close()
            
            if not sites:
                print("No confirmed sites to scrape")
                return
            
            print(f"Found {len(sites)} confirmed sites to scrape")
            
            all_data = []
            processed_sites = []
            
            # Process each site
            for site_id, url in sites:
                try:
                    print(f"\nProcessing site {site_id}...")
                    # 使用URL直接获取数据
                    response = self.session.get(url)
                    response.raise_for_status()
                    site_data = response.json()
                    
                    if site_data:
                        # 提取数据
                        extracted_data = self.extract_data(site_data)
                        if extracted_data:
                            all_data.extend(extracted_data)
                            processed_sites.append(site_id)
                            print(f"Successfully processed site {site_id}")
                        else:
                            print(f"No data extracted for site {site_id}")
                    else:
                        print(f"No data found for site {site_id}")
                except Exception as e:
                    print(f"Error processing site {site_id}:")
                    print(f"Error type: {type(e).__name__}")
                    print(f"Error message: {str(e)}")
                    print("Full stack trace:")
                    traceback.print_exc()
                    continue
            
            if all_data:
                print(f"\nUpdating database with {len(all_data)} records...")
                self.db.update_site_details(all_data)
                print("Database update completed")
                
                # 备份被更新的记录
                print("\nBacking up updated records...")
                self.db.backup_site_details(processed_sites)
                
                # Update sites table status to Extracted
                for site_id in processed_sites:
                    self.update_site_status(site_id, 'Extracted')
            else:
                print("\nNo data to update in database")
            
            # Print scraping results
            print("\nScraping Results Summary:")
            print(f"Total records processed in this run: {len(processed_sites)}")
            if processed_sites:
                print("\nProcessed Site IDs:")
                for site_id in processed_sites:
                    print(f"- {site_id}")
            
            # Get total records count
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            try:
                cursor.execute("SELECT COUNT(*) FROM site_details")
                total_records = cursor.fetchone()[0]
                print(f"\nTotal records in site_details table: {total_records}")
                
                # Get status counts for this run's records
                if processed_sites:
                    placeholders = ','.join(['?' for _ in processed_sites])
                    cursor.execute(f"""
                        SELECT Status, COUNT(*) as count, GROUP_CONCAT(Site_amfori_ID) as site_ids 
                        FROM site_details 
                        WHERE Site_amfori_ID IN ({placeholders})
                        GROUP BY Status
                    """, processed_sites)
                    
                    print("\nStatus Summary for this run:")
                    for status, count, site_ids in cursor.fetchall():
                        print(f"{status}: {count} records")
                        print(f"  Site IDs: {site_ids}")
                
                # Print detailed status summary
                print("\nDetailed Status Summary:")
                for site_id in processed_sites:
                    cursor.execute("SELECT Status, Site_Name_Sitename FROM site_details WHERE Site_amfori_ID = ?", (site_id,))
                    result = cursor.fetchone()
                    if result:
                        status, site_name = result
                        print(f"Site ID: {site_id}")
                        print(f"  Status: {status}")
                        print(f"  Site Name: {site_name}")
                
                conn.close()
                
            except Exception as e:
                print(f"\nError while counting statuses:")
                print(f"Error type: {type(e).__name__}")
                print(f"Error message: {str(e)}")
                print("Full stack trace:")
                traceback.print_exc()
                conn.close()
            
            print("\nScraping completed successfully!")
            
        except Exception as e:
            print(f"\nCritical error during scraping:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print("Full stack trace:")
            traceback.print_exc()

    def get_token(self):
        """Get token from token file"""
        try:
            if not os.path.exists(self.token_file):
                print("No token file found")
                return None
                
            with open(self.token_file, 'r') as f:
                token_data = json.load(f)
                
            # Check if token exists
            if 'token' not in token_data:
                print("No token found in token file")
                return None
                
            return token_data['token']
            
        except Exception as e:
            print(f"Error getting token: {str(e)}")
            return None

    def scrape_by_site_ids(self, site_ids):
        """Scrape details for specific site IDs"""
        try:
            # Ensure we have a valid token
            self.ensure_valid_token()
            
            if not site_ids:
                print("No site IDs provided")
                return []
                
            print(f"Processing {len(site_ids)} specified site IDs")
            
            all_data = []
            not_found_ids = []
            processed_sites = []
            
            # Initialize status counters
            status_data = {
                'New': {'count': 0, 'sites': []},
                'Update': {'count': 0, 'sites': []}
            }
            
            for site_id in site_ids:
                try:
                    print(f"\nProcessing site ID: {site_id}")
                    response_data = self.get_site_details(site_id)
                    if response_data:
                        print(f"Successfully fetched data for site {site_id}")
                        data = self.extract_data(response_data)
                        
                        if data:
                            print(f"Successfully extracted data for site {site_id}")
                            all_data.extend(data)
                            processed_sites.append(site_id)
                        else:
                            print(f"No data extracted for site {site_id}")
                    else:
                        print(f"No response data received for site {site_id}")
                        not_found_ids.append(site_id)
                        
                    time.sleep(1)  # Add delay between requests
                    
                except Exception as e:
                    print(f"\nError processing site {site_id}:")
                    print(f"Error type: {type(e).__name__}")
                    print(f"Error message: {str(e)}")
                    print("Full stack trace:")
                    traceback.print_exc()
                    not_found_ids.append(site_id)
                    continue
            
            if all_data:
                print(f"\nUpdating database with {len(all_data)} records...")
                self.db.update_site_details(all_data)
                print("Database update completed")
                
                # 备份被更新的记录
                print("\nBacking up updated records...")
                self.db.backup_site_details(processed_sites)
                
                # Update status for successfully processed sites to Extracted
                for site_id in processed_sites:
                    self.update_site_status(site_id, 'Extracted')
            else:
                print("\nNo data to update in database")
            
            # Print scraping results
            print("\nScraping Results Summary:")
            print(f"Total records processed in this run: {len(processed_sites)}")
            if processed_sites:
                print("\nProcessed Site IDs:")
                for site_id in processed_sites:
                    print(f"- {site_id}")
            
            # Get total records count
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            try:
                cursor.execute("SELECT COUNT(*) FROM site_details")
                total_records = cursor.fetchone()[0]
                print(f"\nTotal records in site_details table: {total_records}")
                
                # Get status counts for this run's records
                if processed_sites:
                    placeholders = ','.join(['?' for _ in processed_sites])
                    cursor.execute(f"""
                        SELECT Status, COUNT(*) as count, GROUP_CONCAT(Site_amfori_ID) as site_ids 
                        FROM site_details 
                        WHERE Site_amfori_ID IN ({placeholders})
                        GROUP BY Status
                    """, processed_sites)
                    
                    print("\nStatus Summary for this run:")
                    for status, count, site_ids in cursor.fetchall():
                        print(f"{status}: {count} records")
                        print(f"  Site IDs: {site_ids}")
                
                # Print detailed status summary
                print("\nDetailed Status Summary:")
                for site_id in processed_sites:
                    cursor.execute("SELECT Status, Site_Name_Sitename FROM site_details WHERE Site_amfori_ID = ?", (site_id,))
                    result = cursor.fetchone()
                    if result:
                        status, site_name = result
                        print(f"Site ID: {site_id}")
                        print(f"  Status: {status}")
                        print(f"  Site Name: {site_name}")
                
                conn.close()
                
            except Exception as e:
                print(f"\nError while counting statuses:")
                print(f"Error type: {type(e).__name__}")
                print(f"Error message: {str(e)}")
                print("Full stack trace:")
                traceback.print_exc()
                conn.close()
            
            return not_found_ids
            
        except Exception as e:
            print(f"\nCritical error during scraping:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print("Full stack trace:")
            traceback.print_exc()
            raise
        finally:
            if self.driver:
                self.driver.quit()

def main():
    scraper = AmforiDetailScraper()
    
    # Ask user for input
    print("\nPlease choose the scraping mode:")
    print("1. Normal mode (process all confirmed records)")
    print("2. Custom mode (process specific site IDs)")
    
    while True:
        try:
            mode = input("\nEnter mode (1 or 2): ").strip()
            if mode in ['1', '2']:
                break
            print("Invalid input. Please enter 1 or 2.")
        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
            return
    
    if mode == '1':
        # Normal mode - process all confirmed records
        scraper.scrape()
    else:
        # Custom mode - process specific site IDs
        while True:
            try:
                site_ids_input = input("\nEnter site IDs (separated by ':'): ").strip()
                if not site_ids_input:
                    print("No input provided. Please try again.")
                    continue
                    
                # Split and clean site IDs
                site_ids = [id.strip() for id in site_ids_input.split(':') if id.strip()]
                if not site_ids:
                    print("No valid site IDs provided. Please try again.")
                    continue
                    
                break
            except KeyboardInterrupt:
                print("\nProgram terminated by user.")
                return
        
        # Process the specified site IDs
        not_found_ids = scraper.scrape_by_site_ids(site_ids)
        
        # Report results
        if not_found_ids:
            print(f"\nNote: The following site IDs were not found in the source Excel file:")
            for site_id in not_found_ids:
                print(f"- {site_id}")

if __name__ == "__main__":
    main() 