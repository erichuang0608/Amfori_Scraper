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
import traceback
from database import Database

# 加载环境变量
load_dotenv()

class AmforiConfirmedScraper:
    def __init__(self):
        self.base_url = "https://platform.amfori.org"
        self.sso_url = "https://sso.amfori.org"
        #self.target_url = "https://platform.amfori.org/ui/monitoring/monitoring-partner-planning/ongoing"
        self.target_url = "https://platform.amfori.org/ui/monitoring/monitoring-partner-plannings/planned"
        self.api_url = f"{self.base_url}/v1/services/monitoring/monitoring-partner-plannings/planned/search"
        self.excel_file = "amfori_to_plan_data.xlsx"
        self.session = requests.Session()
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
            test_url = f"{self.base_url}/v1/services/monitoring/monitoring-partner-plannings/planned/search"
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
            
    def get_data(self, start=0, rows=25):
        print(f"Fetching data from offset {start}...")
        
        # 修改查询参数，使用更简单的格式
        params = {
            'childQuery': '',
            'parentQuery': ' +(monitoringInitiative.en_GB:BSCI) +(+monitoredSite.address.country.en_GB:China) +(currentState.state.en_GB:"Expired" currentState.state.en_GB:"Canceled")',
            #'parentQuery': '+(monitoringInitiative.en_GB:BSCI) +(currentState.state.en_GB:"Waiting for Unavailability Days" currentState.state.en_GB:"To Plan")',
            #'parentQuery': '+(monitoringInitiative.en_GB:BSCI) + (currentState.state.en_GB:"Expired" currentState.state.en_GB:"Canceled")',
            'rows': rows,
            'sort': '',
            'sortOrder': '',
            'start': start
        }
        
        try:
            response = self.session.get(self.api_url, params=params)
            
            print(f"Request URL: {response.url}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            print(f"Request URL: {response.url}")
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text[:500]}")  # 打印前500个字符
            raise
            
    def extract_data(self, response_data):
        print("Extracting data from response...")
        data = []
        
        if 'results' in response_data:
            for doc in response_data['results']:
                # Convert timestamp to datetime
                request_date = datetime.fromtimestamp(doc.get('requestDate', 0) / 1000).strftime("%Y-%m-%d %H:%M:%S")
                state_date = datetime.fromtimestamp(doc.get('currentState', {}).get('stateDate', 0) / 1000).strftime("%Y-%m-%d %H:%M:%S")
                
                # Get UUID from the document
                uuid = doc.get('uuid', '')
                
                # Get current status
                current_status = doc.get('currentState', {}).get('state', {}).get('en_GB', '')
                
                # Get address components
                address = doc.get('monitoredSite', {}).get('address', {})
                street = address.get('street', '')
                city = address.get('city', '')
                zip_code = address.get('zip', '')
                country = address.get('country', {}).get('en_GB', '')
                
                # Combine address components into a single string
                address_parts = [street, city, zip_code, country]
                address1 = ', '.join(part for part in address_parts if part)
                
                # Get site name and clean it
                site_name = doc.get('monitoredSite', {}).get('name', '')
                # Remove any trailing LTD/Ltd and clean up spaces
                site_name = site_name.replace(' LTD', '').replace(' Ltd', '').replace(' Ltd.', '').strip()
                
                row_data = {
                    'Site amfori ID': doc.get('monitoredSite', {}).get('siteAmforiId', ''),
                    'Site Name': site_name,
                    'Local Name': doc.get('monitoredSite', {}).get('localName', ''),
                    'Address': {
                        'Street': street,
                        'City': city,
                        'Zip': zip_code,
                        'Country': country
                    },
                    'Address1': address1,
                    'Legal Name': doc.get('monitoredSite', {}).get('monitoredPartyLegalName', ''),
                    'Initiative': doc.get('monitoringInitiative', {}).get('en_GB', ''),
                    'Status': current_status,
                    'Monitoring ID': doc.get('monitoringId', ''),
                    'Monitoring Type': doc.get('monitoringType', {}).get('en_GB', ''),
                    'Announcement Type': doc.get('announcementType', {}).get('en_GB', ''),
                    'Requestor': doc.get('requestorLegalName', ''),
                    'Request Date': request_date,
                    'State Date': state_date,
                    'To_Plan_Link': f"{self.base_url}/v1/services/monitoring/monitoring-partner-plannings/{uuid}",
                    'to_confirm_link': f"{self.base_url}/ui/monitoring/monitoring-partner-planning/ongoing/{uuid}",
                    'Created At': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'Updated At': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'Scraped At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                data.append(row_data)
                
        return data
        
    def scrape(self):
        try:
            # Ensure we have a valid token
            self.ensure_valid_token()
            
            start = 0
            rows = 25
            all_data = []
            
            while True:
                response_data = self.get_data(start, rows)
                data = self.extract_data(response_data)
                
                if not data:
                    break
                    
                all_data.extend(data)
                
                # Check if there are more results
                total = response_data.get('totalItems', 0)
                if start + rows >= total:
                    break
                    
                start += rows
                time.sleep(1)  # Add delay between requests
            
            # Save data to Excel
            if all_data:
                df = pd.DataFrame(all_data)
                sheet_name = 'Expired_Cancelled'
                
                # 检查Excel文件是否存在
                if os.path.exists(self.excel_file):
                    # 如果文件存在，使用ExcelWriter追加模式，并替换已存在的sheet
                    with pd.ExcelWriter(self.excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                else:
                    # 如果文件不存在，直接创建新文件
                    df.to_excel(self.excel_file, sheet_name=sheet_name, index=False)
                
                print(f"\nData saved to {self.excel_file} in sheet {sheet_name}")
                print(f"Total records scraped in {sheet_name}: {len(all_data)}")

            print("\nScraping completed successfully!")
            
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            print("Full stack trace:")
            traceback.print_exc()
            raise
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    scraper = AmforiConfirmedScraper()
    scraper.scrape() 