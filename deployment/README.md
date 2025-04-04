# Amfori 数据采集系统部署指南

## 系统要求
- Docker
- Docker Compose
- 至少 2GB 可用内存
- 至少 10GB 可用磁盘空间

## 部署步骤

1. 准备环境文件
```bash
cp .env.example .env
# 编辑 .env 文件，填入实际的配置信息
```

2. 创建必要的目录
```bash
mkdir -p data logs
chmod 777 data logs
```

3. 构建并启动服务
```bash
docker-compose up -d --build
```

4. 验证服务状态
```bash
docker-compose ps
docker-compose logs -f
```

## 目录结构
- `data/`: 数据库文件存储目录
- `logs/`: 日志文件存储目录
- `.env`: 环境配置文件
- `Dockerfile`: Docker 镜像构建文件
- `docker-compose.yml`: Docker Compose 配置文件
- `requirements.txt`: Python 依赖列表

## 常见问题处理

1. 服务无法启动
- 检查 .env 文件配置
- 检查端口 5001 是否被占用
- 检查日志文件内容

2. 数据采集失败
- 验证 Amfori 账号密码是否正确
- 检查网络连接
- 查看详细错误日志

3. 内存使用过高
- 调整 Docker 容器内存限制
- 检查是否有内存泄漏

## 维护指南

1. 日志轮转
系统使用 logrotate 进行日志管理，配置文件在 /etc/logrotate.d/ 目录下

2. 数据备份
建议定期备份 data 目录下的数据库文件

3. 系统更新
```bash
# 拉取最新代码
git pull

# 重新构建并启动服务
docker-compose up -d --build
```

## 安全建议

1. 定期更新系统和依赖包
2. 使用强密码并定期更换
3. 限制服务器访问IP
4. 启用 HTTPS
5. 定期备份数据

## 监控建议

1. 设置系统资源监控
2. 配置错误告警
3. 监控数据采集任务状态
4. 定期检查日志文件

## 联系支持
如遇到问题，请联系技术支持团队：
- Email: support@example.com
- Tel: +86-xxx-xxxx-xxxx 