from flask import Flask, render_template, jsonify, request, send_file
from flask_socketio import SocketIO
import sys
import io
import threading
import logging
from amfori_scraper import AmforiScraper
from amfori_detail_scraper import AmforiDetailScraper
from database import Database
import os
from dotenv import load_dotenv
import subprocess
import json
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OutputRedirector:
    def __init__(self, socketio):
        self.socketio = socketio
        self.buffer = io.StringIO()

    def write(self, text):
        if text.strip():  # Only send non-empty messages
            logger.info(f"Emitting output: {text.strip()}")
            self.socketio.emit('output', {'data': text})
            self.buffer.write(text)

    def flush(self):
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query')
def query():
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    site_id = request.args.get('site_id', '')
    active_tab = request.args.get('tab', 'sites')  # 默认显示 sites 标签页
    
    logger.info(f"Query request - page: {page}, per_page: {per_page}, site_id: '{site_id}', active_tab: {active_tab}")
    
    # 初始化数据库连接
    db = Database()
    
    # 初始化模板数据
    template_data = {
        'sites_data': [],
        'site_details_data': [],
        'backup_data': [],
        'total_records': 0
    }
    
    try:
        # 根据当前标签页获取相应的数据
        if active_tab == 'sites':
            data, total = db.get_sites(page, per_page, site_id)
            template_data['sites_data'] = data
            template_data['total_records'] = total
        elif active_tab == 'site_details':
            data, total = db.get_site_details(page, per_page, site_id)
            template_data['site_details_data'] = data
            template_data['total_records'] = total
        else:  # backup
            data, total = db.get_backup_data(page, per_page, site_id)
            template_data['backup_data'] = data
            template_data['total_records'] = total
        
        logger.info(f"Data retrieved for {active_tab}: {len(data)} records, total: {total}")
        if data:
            logger.info(f"Sample record: {data[0]}")
        
        total_pages = (total + per_page - 1) // per_page
        
        return render_template('query.html',
                             active_tab=active_tab,
                             current_page=page,
                             total_pages=total_pages,
                             **template_data)
    
    except Exception as e:
        logger.error(f"Error in query route: {str(e)}", exc_info=True)
        return render_template('query.html',
                             active_tab=active_tab,
                             current_page=1,
                             total_pages=1,
                             error_message="An error occurred while retrieving data.",
                             **template_data)

@app.route('/run_scraper')
def run_scraper():
    try:
        # 运行 amfori_scraper.py
        result = subprocess.run(['python3', 'amfori_scraper.py'], 
                              capture_output=True, 
                              text=True)
        return jsonify({
            'success': True,
            'output': result.stdout
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/run_detail_scraper')
def run_detail_scraper():
    try:
        # 运行 amfori_detail_scraper.py
        result = subprocess.run(['python3', 'amfori_detail_scraper.py'], 
                              capture_output=True, 
                              text=True)
        return jsonify({
            'success': True,
            'output': result.stdout
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def run_scraper_internal(scraper_type, site_ids=None):
    logger.info(f"Starting {scraper_type} scraper")
    logger.info(f"Site IDs parameter: {site_ids}")
    
    # Redirect stdout to our custom output handler
    old_stdout = sys.stdout
    sys.stdout = OutputRedirector(socketio)
    
    try:
        if scraper_type == 'amfori':
            logger.info("Initializing AmforiScraper")
            scraper = AmforiScraper()
            scraper.scrape()
        else:
            logger.info("Initializing AmforiDetailScraper")
            scraper = AmforiDetailScraper()
            
            # Ensure we have a valid token before proceeding
            try:
                logger.info("Validating token...")
                scraper.ensure_valid_token()
                logger.info("Token validation successful")
            except Exception as e:
                error_msg = f"Token validation failed: {str(e)}"
                logger.error(error_msg)
                logger.error("Full stack trace:", exc_info=True)
                print(error_msg)
                socketio.emit('scraper_complete', {
                    'scraper': scraper_type,
                    'status': 'error',
                    'message': f'Error validating token: {str(e)}'
                })
                return

            if site_ids and isinstance(site_ids, str) and site_ids.strip():
                logger.info(f"Running detail scraper with site IDs: {site_ids}")
                # Split the site_ids string into a list
                site_ids_list = [id.strip() for id in site_ids.split(':') if id.strip()]
                logger.info(f"Processed site IDs list: {site_ids_list}")
                not_found_ids = scraper.scrape_by_site_ids(site_ids_list)
                if not_found_ids:
                    logger.warning(f"Some site IDs were not found: {not_found_ids}")
                    socketio.emit('scraper_complete', {
                        'scraper': scraper_type,
                        'status': 'warning',
                        'message': f'Detail scraper completed with warnings. Some site IDs were not found: {", ".join(not_found_ids)}'
                    })
                    return
            else:
                logger.info("No site IDs provided, running detail scraper for all confirmed records")
                try:
                    scraper.scrape()
                except Exception as e:
                    error_msg = f"Error in scrape method: {str(e)}"
                    logger.error(error_msg)
                    logger.error("Full stack trace:", exc_info=True)
                    raise
            
        # Send completion event
        logger.info(f"Scraper {scraper_type} completed successfully")
        socketio.emit('scraper_complete', {
            'scraper': scraper_type,
            'status': 'success',
            'message': f'{scraper_type.title()} scraper completed successfully!'
        })
        logger.info("Completion event sent")
    except Exception as e:
        error_msg = f"Error running scraper: {str(e)}"
        logger.error(error_msg)
        logger.error("Full stack trace:", exc_info=True)
        print(error_msg)
        # Send error event
        socketio.emit('scraper_complete', {
            'scraper': scraper_type,
            'status': 'error',
            'message': f'Error running {scraper_type} scraper: {str(e)}'
        })
        logger.info("Error event sent")
    finally:
        sys.stdout = old_stdout
        logger.info(f"Finished running {scraper_type} scraper")

@app.route('/run/<scraper_type>', methods=['POST'])
def run(scraper_type):
    logger.info(f"Received request to run {scraper_type} scraper")
    
    if scraper_type not in ['amfori', 'detail']:
        logger.error(f"Invalid scraper type: {scraper_type}")
        return jsonify({'error': 'Invalid scraper type'})
    
    # Get site IDs from request if provided
    site_ids = None
    if scraper_type == 'detail':
        data = request.get_json()
        logger.info(f"Received request data: {data}")
        if data and 'site_ids' in data and data['site_ids'] and data['site_ids'].strip():
            site_ids = data['site_ids']
            logger.info(f"Processing site IDs: {site_ids}")
    
    # Start scraper in a separate thread
    thread = threading.Thread(target=run_scraper_internal, args=(scraper_type, site_ids))
    thread.start()
    
    return jsonify({'status': 'started', 'scraper': scraper_type})

@app.route('/export')
def export():
    site_id = request.args.get('site_id', '')
    active_tab = request.args.get('tab', 'sites')
    
    # 初始化数据库连接
    db = Database()
    
    # 根据当前标签页获取所有数据（不分页）
    if active_tab == 'sites':
        data, _ = db.get_sites(page=1, per_page=None, site_id=site_id)  # per_page=None 表示获取所有数据
        filename = 'sites_export.xlsx'
    elif active_tab == 'site_details':
        data, _ = db.get_site_details(page=1, per_page=None, site_id=site_id)
        filename = 'site_details_export.xlsx'
    else:  # backup
        data, _ = db.get_backup_data(page=1, per_page=None, site_id=site_id)
        filename = 'backup_data_export.xlsx'
    
    # 创建 DataFrame
    df = pd.DataFrame(data)
    
    # 创建一个内存中的 Excel 文件
    output = io.BytesIO()
    
    # 使用 ExcelWriter 来设置一些格式
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
        # 获取 workbook 和 worksheet 对象
        workbook = writer.book
        worksheet = writer.sheets['Data']
        
        # 设置列宽
        for i, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).apply(len).max(), len(col)) + 2
            worksheet.set_column(i, i, max_length)
    
    output.seek(0)
    
    # 在文件名中添加时间戳
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{active_tab}_export_{timestamp}.xlsx"
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )

if __name__ == '__main__':
    logger.info("Starting Flask application")
    socketio.run(app, debug=True, port=5001) 