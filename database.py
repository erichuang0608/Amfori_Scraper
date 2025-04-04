import sqlite3
import pandas as pd
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.db_file = "amfori.db"
        self.init_database()

    def get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row  # 启用字典行工厂
        return conn

    def init_database(self):
        """初始化数据库表结构"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 创建主表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Site_amfori_ID TEXT,
            Site_Name TEXT,
            Local_Name TEXT,
            Address_Street TEXT,
            Address_City TEXT,
            Address_Zip TEXT,
            Address_Country TEXT,
            Address1 TEXT,
            Legal_Name TEXT,
            Initiative TEXT,
            Status TEXT,
            Monitoring_ID TEXT,
            Monitoring_Type TEXT,
            Announcement_Type TEXT,
            Requestor TEXT,
            Request_Date TEXT,
            State_Date TEXT,
            To_Plan_Link TEXT,
            to_confirm_link TEXT,
            Created_At TEXT,
            Updated_At TEXT,
            Scraped_At TEXT,
            Status_comparation TEXT
        )
        ''')

        # 创建详情表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS site_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Scraped_At TEXT,
            Status TEXT,
            Request_Date TEXT,
            Site_amfori_ID TEXT,
            Monitoring_ID TEXT,
            Company_Name_LegalName TEXT,
            Site_Name_Sitename TEXT,
            Local_Name_Localname TEXT,
            Contact_Email TEXT,
            Contact_Phonenumber TEXT,
            address TEXT,
            Audit_Start_window_from TEXT,
            Audit_To_window_to TEXT,
            Status1 TEXT,
            Audit_Start_date TEXT,
            Audit_End_date TEXT,
            Unavailability_Days TEXT,
            Schedule_Number TEXT,
            Job_Number TEXT,
            BSCI_MEMBER TEXT,
            BSCI_Member_phonenumber TEXT,
            BSCI_Member_emailAddress TEXT,
            Audit_Announcement TEXT,
            Audit_Methodology TEXT,
            Audit_type TEXT,
            CS TEXT,
            Remark TEXT,
            Related_Sales TEXT,
            Created_At TEXT,
            Updated_At TEXT
        )
        ''')

        # 创建备份表（如果不存在）
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS amfori_detail_data_backup (
            backup_id INTEGER PRIMARY KEY AUTOINCREMENT,
            site_detail_ID INTEGER,
            Scraped_At TEXT,
            Status TEXT,
            Request_Date TEXT,
            Site_amfori_ID TEXT,
            Monitoring_ID TEXT,
            Company_Name_LegalName TEXT,
            Site_Name_Sitename TEXT,
            Local_Name_Localname TEXT,
            Contact_Email TEXT,
            Contact_Phonenumber TEXT,
            address TEXT,
            Audit_Start_window_from TEXT,
            Audit_To_window_to TEXT,
            Status1 TEXT,
            Audit_Start_date TEXT,
            Audit_End_date TEXT,
            Unavailability_Days TEXT,
            Schedule_Number TEXT,
            Job_Number TEXT,
            BSCI_MEMBER TEXT,
            BSCI_Member_phonenumber TEXT,
            BSCI_Member_emailAddress TEXT,
            Audit_Announcement TEXT,
            Audit_Methodology TEXT,
            Audit_type TEXT,
            CS TEXT,
            Remark TEXT,
            Related_Sales TEXT,
            Created_At TEXT,
            Updated_At TEXT,
            Backup_Time TEXT
        )
        ''')

        conn.commit()
        conn.close()

    def create_backup_table(self):
        """创建备份表"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 创建备份表（如果不存在）
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS amfori_detail_data_backup (
            backup_id INTEGER PRIMARY KEY AUTOINCREMENT,
            site_detail_ID INTEGER,
            Scraped_At TEXT,
            Status TEXT,
            Request_Date TEXT,
            Site_amfori_ID TEXT,
            Monitoring_ID TEXT,
            Company_Name_LegalName TEXT,
            Site_Name_Sitename TEXT,
            Local_Name_Localname TEXT,
            Contact_Email TEXT,
            Contact_Phonenumber TEXT,
            address TEXT,
            Audit_Start_window_from TEXT,
            Audit_To_window_to TEXT,
            Status1 TEXT,
            Audit_Start_date TEXT,
            Audit_End_date TEXT,
            Unavailability_Days TEXT,
            Schedule_Number TEXT,
            Job_Number TEXT,
            BSCI_MEMBER TEXT,
            BSCI_Member_phonenumber TEXT,
            BSCI_Member_emailAddress TEXT,
            Audit_Announcement TEXT,
            Audit_Methodology TEXT,
            Audit_type TEXT,
            CS TEXT,
            Remark TEXT,
            Related_Sales TEXT,
            Created_At TEXT,
            Updated_At TEXT,
            Backup_Time TEXT
        )
        ''')

        conn.commit()
        conn.close()

    def update_sites(self, data):
        """更新主表数据"""
        conn = self.get_connection()
        cursor = conn.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # 获取现有的Site amfori ID列表
            cursor.execute("SELECT Site_amfori_ID FROM sites")
            existing_ids = {row[0] for row in cursor.fetchall()}

            # 字段名称映射
            field_mapping = {
                'Site amfori ID': 'Site_amfori_ID',
                'Site Name': 'Site_Name',
                'Local Name': 'Local_Name',
                'Legal Name': 'Legal_Name',
                'Monitoring ID': 'Monitoring_ID',
                'Monitoring Type': 'Monitoring_Type',
                'Announcement Type': 'Announcement_Type',
                'Request Date': 'Request_Date',
                'State Date': 'State_Date',
                'To_Plan_Link': 'To_Plan_Link',
                'to_confirm_link': 'to_confirm_link',
                'Updated At': 'Updated_At',
                'Scraped At': 'Scraped_At',
                'Initiative': 'Initiative',
                'Status': 'Status',
                'Requestor': 'Requestor'
            }

            for item in data:
                site_id = item.get('Site amfori ID', '')
                if not site_id:
                    continue

                # 准备数据，使用映射后的字段名
                site_data = {}
                for source_field, db_field in field_mapping.items():
                    if source_field == 'Address':
                        # 处理地址字段
                        address = item.get('Address', {})
                        site_data['Address_Street'] = address.get('Street', '')
                        site_data['Address_City'] = address.get('City', '')
                        site_data['Address_Zip'] = address.get('Zip', '')
                        site_data['Address_Country'] = address.get('Country', '')
                        site_data['Address1'] = item.get('Address1', '')
                    else:
                        site_data[db_field] = item.get(source_field, '')

                # 添加时间戳
                site_data['Updated_At'] = current_time
                site_data['Scraped_At'] = current_time

                if site_id in existing_ids:
                    # 更新现有记录
                    set_clause = ', '.join(f"{k} = ?" for k in site_data.keys())
                    cursor.execute(f"UPDATE sites SET {set_clause} WHERE Site_amfori_ID = ?",
                                 (*site_data.values(), site_id))
                    cursor.execute("UPDATE sites SET Status_comparation = 'Update' WHERE Site_amfori_ID = ?", (site_id,))
                else:
                    # 插入新记录
                    site_data['Created_At'] = current_time
                    site_data['Status_comparation'] = 'New'
                    columns = ', '.join(site_data.keys())
                    placeholders = ', '.join(['?' for _ in site_data])
                    cursor.execute(f"INSERT INTO sites ({columns}) VALUES ({placeholders})",
                                 list(site_data.values()))

            # 将不在新数据中的记录标记为Confirmed
            new_ids = {item.get('Site amfori ID', '') for item in data}
            cursor.execute("UPDATE sites SET Status_comparation = 'Confirmed', Updated_At = ?, Scraped_At = ? WHERE Site_amfori_ID NOT IN ({})".format(','.join(['?' for _ in new_ids])),
                         (current_time, current_time, *new_ids))

            conn.commit()
        finally:
            conn.close()

    def update_site_details(self, data):
        """更新详情表数据"""
        conn = self.get_connection()
        cursor = conn.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # 字段名称映射
            field_mapping = {
                'Site amfori ID': 'Site_amfori_ID',
                'Monitoring ID': 'Monitoring_ID',
                'Company Name(LegalName)': 'Company_Name_LegalName',
                'Site Name(Sitename)': 'Site_Name_Sitename',
                'Local Name(Localname)': 'Local_Name_Localname',
                'Contact Email': 'Contact_Email',
                'Contact Phonenumber': 'Contact_Phonenumber',
                'address': 'address',
                'Audit Start window(confirmedTimeWindow-from)': 'Audit_Start_window_from',
                'Audit To window(confirmedTimeWindow-to)': 'Audit_To_window_to',
                'Status1': 'Status1',
                'Audit Start date': 'Audit_Start_date',
                'Audit End date': 'Audit_End_date',
                'Unavailability Days': 'Unavailability_Days',
                'Schedule#': 'Schedule_Number',
                'Job#': 'Job_Number',
                'BSCI MEMBER': 'BSCI_MEMBER',
                'BSCI Member phonenumber': 'BSCI_Member_phonenumber',
                'BSCI Member emailAddress': 'BSCI_Member_emailAddress',
                'Audit Announcement': 'Audit_Announcement',
                'Audit Methodology': 'Audit_Methodology',
                'Audit type': 'Audit_type',
                'CS': 'CS',
                'Remark（平台来单or CS来单）': 'Remark',
                'Related Sales': 'Related_Sales',
                'Updated At': 'Updated_At',
                'Scraped At': 'Scraped_At',
                'Status': 'Status'
            }

            for item in data:
                site_id = str(item.get('Site amfori ID', ''))
                if not site_id:
                    continue

                # 准备数据，使用映射后的字段名
                detail_data = {}
                for source_field, db_field in field_mapping.items():
                    value = item.get(source_field, '')
                    # 确保值是字符串类型
                    detail_data[db_field] = str(value) if value is not None else ''

                # 检查记录是否存在
                cursor.execute("SELECT COUNT(*) FROM site_details WHERE Site_amfori_ID = ?", (site_id,))
                exists = cursor.fetchone()[0] > 0
                
                if exists:
                    # 更新现有记录
                    set_clause = ', '.join(f"{k} = ?" for k in detail_data.keys())
                    cursor.execute(f"UPDATE site_details SET {set_clause} WHERE Site_amfori_ID = ?",
                                 (*detail_data.values(), site_id))
                    # 更新状态为 Updated
                    cursor.execute("""
                        UPDATE site_details 
                        SET Status = 'Updated',
                            Updated_At = ?,
                            Scraped_At = ?
                        WHERE Site_amfori_ID = ?
                    """, (current_time, current_time, site_id))
                    print(f"Updated existing record for site {site_id} (Status: Updated)")
                else:
                    # 插入新记录
                    detail_data['Created_At'] = current_time
                    detail_data['Updated_At'] = current_time
                    detail_data['Scraped_At'] = current_time
                    detail_data['Status'] = 'New'  # 新记录状态为 New
                    columns = ', '.join(detail_data.keys())
                    placeholders = ', '.join(['?' for _ in detail_data])
                    cursor.execute(f"INSERT INTO site_details ({columns}) VALUES ({placeholders})",
                                 list(detail_data.values()))
                    print(f"Inserted new record for site {site_id} (Status: New)")

            conn.commit()
        finally:
            conn.close()

    def get_sites(self, page, per_page, site_id=''):
        logger.info(f"Getting sites data - page: {page}, per_page: {per_page}, site_id: {site_id}")
        offset = (page - 1) * per_page if per_page is not None else 0
        
        # 基础查询
        query = """
            SELECT 
                id,
                Site_amfori_ID as site_amfori_id,
                Site_Name as site_name,
                Local_Name as local_name,
                Address_Street as address_street,
                Address_City as address_city,
                Address_Zip as address_zip,
                Address_Country as address_country,
                Address1 as address1,
                Legal_Name as legal_name,
                Initiative as initiative,
                Status as status,
                Monitoring_ID as monitoring_id,
                Monitoring_Type as monitoring_type,
                Announcement_Type as announcement_type,
                Requestor as requestor,
                Request_Date as request_date,
                State_Date as state_date,
                To_Plan_Link as to_plan_link,
                to_confirm_link,
                Created_At as created_at,
                Updated_At as updated_at,
                Scraped_At as scraped_at,
                Status_comparation as status_comparation
            FROM sites
            WHERE 1=1
        """
        count_query = "SELECT COUNT(*) FROM sites WHERE 1=1"
        
        params = []
        if site_id:
            query += " AND Site_amfori_ID LIKE ?"
            count_query += " AND Site_amfori_ID LIKE ?"
            params.append(f"%{site_id}%")
        
        # 添加分页
        if per_page is not None:
            query += " LIMIT ? OFFSET ?"
            params.extend([per_page, offset])
        
        logger.info(f"Executing query: {query}")
        logger.info(f"Query parameters: {params}")
        
        try:
            # 执行查询
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # 获取总记录数
            cursor.execute(count_query, params[:-2] if per_page is not None and params else params)
            total = cursor.fetchone()[0]
            
            # 转换为字典列表
            result = [dict(row) for row in rows]
            
            logger.info(f"Query returned {len(result)} rows, total: {total}")
            
            return result, total
        finally:
            cursor.close()
            conn.close()

    def get_site_details(self, page, per_page, site_id=''):
        logger.info(f"Getting site details - page: {page}, per_page: {per_page}, site_id: {site_id}")
        offset = (page - 1) * per_page if per_page is not None else 0
        
        # 基础查询
        query = """
            SELECT 
                id,
                Scraped_At as scraped_at,
                Status as status,
                Request_Date as request_date,
                Site_amfori_ID as site_amfori_id,
                Monitoring_ID as monitoring_id,
                Company_Name_LegalName as company_name_legalname,
                Site_Name_Sitename as site_name_sitename,
                Local_Name_Localname as local_name_localname,
                Contact_Email as contact_email,
                Contact_Phonenumber as contact_phonenumber,
                address,
                Audit_Start_window_from as audit_start_window_from,
                Audit_To_window_to as audit_to_window_to,
                Status1 as status1,
                Audit_Start_date as audit_start_date,
                Audit_End_date as audit_end_date,
                Unavailability_Days as unavailability_days,
                Schedule_Number as schedule_number,
                Job_Number as job_number,
                BSCI_MEMBER as bsci_member,
                BSCI_Member_phonenumber as bsci_member_phonenumber,
                BSCI_Member_emailAddress as bsci_member_emailaddress,
                Audit_Announcement as audit_announcement,
                Audit_Methodology as audit_methodology,
                Audit_type as audit_type,
                CS as cs,
                Remark as remark,
                Related_Sales as related_sales,
                Created_At as created_at,
                Updated_At as updated_at
            FROM site_details
            WHERE 1=1
        """
        count_query = "SELECT COUNT(*) FROM site_details WHERE 1=1"
        
        params = []
        if site_id:
            query += " AND Site_amfori_ID LIKE ?"
            count_query += " AND Site_amfori_ID LIKE ?"
            params.append(f"%{site_id}%")
        
        # 添加分页
        if per_page is not None:
            query += " LIMIT ? OFFSET ?"
            params.extend([per_page, offset])
        
        try:
            # 执行查询
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # 获取总记录数
            cursor.execute(count_query, params[:-2] if per_page is not None and params else params)
            total = cursor.fetchone()[0]
            
            # 转换为字典列表
            result = [dict(row) for row in rows]
            
            logger.info(f"Query returned {len(result)} rows, total: {total}")
            
            return result, total
        finally:
            cursor.close()
            conn.close()

    def get_confirmed_sites(self, page=1, per_page=25, site_id=None):
        """获取已确认的站点数据，支持分页和搜索"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # 构建查询条件
            where_clause = "WHERE Status_comparation = 'Confirmed'"
            params = []
            if site_id:
                where_clause += " AND Site_amfori_ID LIKE ?"
                params.append(f"%{site_id}%")
            
            # 获取总记录数
            cursor.execute(f"SELECT COUNT(*) FROM sites {where_clause}", params)
            total_records = cursor.fetchone()[0]
            total_pages = (total_records + per_page - 1) // per_page
            
            # 获取分页数据
            offset = (page - 1) * per_page
            cursor.execute(f"SELECT * FROM sites {where_clause} LIMIT ? OFFSET ?", 
                         params + [per_page, offset])
            records = cursor.fetchall()
            
            # 获取列名
            columns = [description[0] for description in cursor.description]
            
            # 将结果转换为字典列表
            data = []
            for record in records:
                data.append(dict(zip(columns, record)))
            
            return {
                'data': data,
                'pages': total_pages,
                'total': total_records
            }
        finally:
            conn.close()

    def backup_site_details(self, site_ids=None):
        """备份site_details表中指定站点ID的数据到amfori_detail_data_backup表
        如果site_ids为None，则备份所有数据
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # 构建查询条件
            where_clause = "WHERE 1=1"
            params = []
            if site_ids:
                placeholders = ','.join(['?' for _ in site_ids])
                where_clause = f"WHERE Site_amfori_ID IN ({placeholders})"
                params = site_ids

            # 获取需要备份的数据
            cursor.execute(f"SELECT * FROM site_details {where_clause}", params)
            source_columns = [description[0] for description in cursor.description]
            data = cursor.fetchall()

            if data:
                # 准备要插入的列（排除原表的id列，因为我们使用它作为site_detail_ID）
                insert_columns = [col for col in source_columns if col != 'id']
                insert_columns.append('Backup_Time')
                
                # 构建插入语句
                columns_str = ','.join(['site_detail_ID'] + insert_columns)
                placeholders = ','.join(['?' for _ in range(len(insert_columns) + 1)])  # +1 for site_detail_ID
                
                # 准备插入数据
                insert_data = []
                for row in data:
                    # row[0] 是原表的id，用作site_detail_ID
                    # row[1:] 是其他所有列的数据
                    insert_data.append((row[0],) + row[1:] + (current_time,))
                
                # 插入数据到备份表
                cursor.executemany(
                    f"INSERT INTO amfori_detail_data_backup ({columns_str}) VALUES ({placeholders})",
                    insert_data
                )
                conn.commit()
                print(f"Successfully backed up {len(data)} records to amfori_detail_data_backup")
            else:
                print("No data to backup in site_details table")

        except Exception as e:
            print(f"Error during backup: {str(e)}")
            raise
        finally:
            conn.close()

    def get_backup_data(self, page, per_page, site_id=''):
        logger.info(f"Getting backup data - page: {page}, per_page: {per_page}, site_id: {site_id}")
        offset = (page - 1) * per_page if per_page is not None else 0
        
        # 基础查询
        query = """
            SELECT 
                backup_id,
                site_detail_ID as site_detail_id,
                Scraped_At as scraped_at,
                Status as status,
                Request_Date as request_date,
                Site_amfori_ID as site_amfori_id,
                Monitoring_ID as monitoring_id,
                Company_Name_LegalName as company_name_legalname,
                Site_Name_Sitename as site_name_sitename,
                Local_Name_Localname as local_name_localname,
                Contact_Email as contact_email,
                Contact_Phonenumber as contact_phonenumber,
                address,
                Audit_Start_window_from as audit_start_window_from,
                Audit_To_window_to as audit_to_window_to,
                Status1 as status1,
                Audit_Start_date as audit_start_date,
                Audit_End_date as audit_end_date,
                Unavailability_Days as unavailability_days,
                Schedule_Number as schedule_number,
                Job_Number as job_number,
                BSCI_MEMBER as bsci_member,
                BSCI_Member_phonenumber as bsci_member_phonenumber,
                BSCI_Member_emailAddress as bsci_member_emailaddress,
                Audit_Announcement as audit_announcement,
                Audit_Methodology as audit_methodology,
                Audit_type as audit_type,
                CS as cs,
                Remark as remark,
                Related_Sales as related_sales,
                Created_At as created_at,
                Updated_At as updated_at,
                Backup_Time as backup_time
            FROM amfori_detail_data_backup
            WHERE 1=1
        """
        count_query = "SELECT COUNT(*) FROM amfori_detail_data_backup WHERE 1=1"
        
        params = []
        if site_id:
            query += " AND Site_amfori_ID LIKE ?"
            count_query += " AND Site_amfori_ID LIKE ?"
            params.append(f"%{site_id}%")
        
        # 添加分页
        if per_page is not None:
            query += " LIMIT ? OFFSET ?"
            params.extend([per_page, offset])
        
        try:
            # 执行查询
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # 获取总记录数
            cursor.execute(count_query, params[:-2] if per_page is not None and params else params)
            total = cursor.fetchone()[0]
            
            # 转换为字典列表
            result = [dict(row) for row in rows]
            
            logger.info(f"Query returned {len(result)} rows, total: {total}")
            
            return result, total
        finally:
            cursor.close()
            conn.close() 