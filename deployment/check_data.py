from database import Database

def check_data():
    db = Database()
    
    # 检查 sites 表
    print("\nChecking sites table:")
    data, total = db.get_sites(1, 10)
    print(f"Total records: {total}")
    for record in data:
        print(f"Site ID: {record['Site_amfori_ID']}, Name: {record['Site_Name']}")
    
    # 检查 site_details 表
    print("\nChecking site_details table:")
    data, total = db.get_site_details(1, 10)
    print(f"Total records: {total}")
    for record in data:
        print(f"Site ID: {record['Site_amfori_ID']}, Company: {record['Company_Name_LegalName']}")
    
    # 检查 backup 表
    print("\nChecking backup table:")
    data, total = db.get_backup_data(1, 10)
    print(f"Total records: {total}")
    for record in data:
        print(f"Backup ID: {record['backup_id']}, Site ID: {record['Site_amfori_ID']}")

if __name__ == "__main__":
    check_data() 