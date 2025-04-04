# Amfori Scraper

这是一个用于抓取 Amfori 平台数据的爬虫程序。

## 系统要求

- Python 3.8 或更高版本
- Chrome 浏览器
- ChromeDriver（与 Chrome 浏览器版本匹配）

## 安装步骤

1. 安装 Chrome 浏览器
   - 访问 https://www.google.com/chrome/ 下载并安装 Chrome 浏览器

2. 安装 ChromeDriver
   - 在 macOS 上使用 Homebrew：
     ```bash
     brew install chromedriver
     ```
   - 在其他系统上，请从 https://sites.google.com/chromium.org/driver/ 下载与 Chrome 浏览器版本匹配的 ChromeDriver

3. 克隆或下载项目文件到本地

4. 创建并激活虚拟环境（推荐）：
   ```bash
   # 创建虚拟环境
   python -m venv venv

   # 在 macOS/Linux 上激活虚拟环境
   source venv/bin/activate

   # 在 Windows 上激活虚拟环境
   .\venv\Scripts\activate
   ```

5. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

6. 配置环境变量：
   - 创建 `.env` 文件
   - 添加以下内容：
     ```
     AMFORI_USERNAME=你的用户名
     AMFORI_PASSWORD=你的密码
     ```

## 使用方法

1. 确保已激活虚拟环境

2. 运行爬虫：
   ```bash
   python amfori_scraper.py
   ```

3. 运行 Web 界面：
   ```bash
   python app.py
   ```

4. 在浏览器中访问：
   ```
   http://localhost:5000
   ```

## 输出文件

- 爬取的数据将保存在 `amfori_data.xlsx` 文件中
- 状态信息将显示在控制台中

## 注意事项

- 确保 Chrome 浏览器和 ChromeDriver 版本匹配
- 保持网络连接稳定
- 首次运行时需要登录 Amfori 平台
- 建议定期运行以更新数据

## 常见问题

1. ChromeDriver 版本不匹配
   - 检查 Chrome 浏览器版本
   - 安装匹配的 ChromeDriver 版本

2. 登录失败
   - 检查 `.env` 文件中的用户名和密码是否正确
   - 确保网络连接正常

3. 数据抓取失败
   - 检查网络连接
   - 确认 Amfori 平台是否可访问
   - 查看错误日志获取详细信息 