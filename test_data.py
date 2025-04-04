from database import Database
from datetime import datetime

def insert_test_data():
    db = Database()
    
    # 测试数据
    sites_data = [
        {
            'Site_amfori_ID': 'TEST001',
            'Site_Name': 'Test Site 1',
            'Local_Name': '测试站点1',
            'Address_Street': 'Test Street 1',
            'Address_City': 'Test City 1',
            'Address_Zip': '12345',
            'Address_Country': 'Test Country',
            'Address1': 'Test Address 1',
            'Legal_Name': 'Test Legal Name 1',
            'Initiative': 'BSCI',
            'Status': 'Active',
            'Monitoring_ID': 'MON001',
            'Monitoring_Type': 'Full Monitoring',
            'Announcement_Type': 'Semi Announced',
            'Requestor': 'Test Requestor 1',
            'Request_Date': '2024-01-01',
            'State_Date': '2024-01-01',
            'To_Plan_Link': 'http://test1.com',
            'to_confirm_link': 'http://test1.com/confirm',
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Updated_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Scraped_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Status_comparation': 'New'
        }
    ]
    
    site_details_data = [
        {
            'Scraped_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Status': 'New',
            'Request_Date': '2024-01-01',
            'Site_amfori_ID': 'TEST001',
            'Monitoring_ID': 'MON001',
            'Company_Name_LegalName': 'Test Company 1',
            'Site_Name_Sitename': 'Test Site 1',
            'Local_Name_Localname': '测试站点1',
            'Contact_Email': 'test1@example.com',
            'Contact_Phonenumber': '1234567890',
            'address': 'Test Address 1',
            'Audit_Start_window_from': '2024-01-01',
            'Audit_To_window_to': '2024-12-31',
            'Status1': 'Active',
            'Audit_Start_date': '2024-01-01',
            'Audit_End_date': '2024-12-31',
            'Unavailability_Days': '[]',
            'Schedule_Number': 'SCH001',
            'Job_Number': 'JOB001',
            'BSCI_MEMBER': 'Test Member 1',
            'BSCI_Member_phonenumber': '0987654321',
            'BSCI_Member_emailAddress': 'member1@example.com',
            'Audit_Announcement': 'Semi Announced',
            'Audit_Methodology': 'Full Monitoring',
            'Audit_type': 'Regular',
            'CS': 'Test CS',
            'Remark': 'Test Remark',
            'Related_Sales': 'Test Sales',
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Updated_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]
    
    # 插入数据
    db.update_sites(sites_data)
    db.update_site_details(site_details_data)
    
    # 备份数据
    db.backup_site_details(['TEST001'])
    
    print("Test data inserted successfully!")

if __name__ == "__main__":
    insert_test_data() 