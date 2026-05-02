# Deployment Guide

## Grant Management System - Python Version

### Development Deployment

#### Local Development
1. Clone the repository
2. Navigate to the python-app directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Access at `http://localhost:5173`

### Production Deployment

#### Option 1: Using Gunicorn (Recommended)

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Create a Gunicorn configuration file (`gunicorn.conf.py`):
   ```python
   bind = "0.0.0.0:8000"
   workers = 4
   worker_class = "sync"
   worker_connections = 1000
   max_requests = 1000
   max_requests_jitter = 100
   timeout = 30
   keepalive = 2
   preload_app = True
   ```

3. Run with Gunicorn:
   ```bash
   gunicorn --config gunicorn.conf.py app:app
   ```

#### Option 2: Using Docker

1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 5173
   
   CMD ["gunicorn", "--bind", "0.0.0.0:5173", "app:app"]
   ```

2. Create a `docker-compose.yml`:
   ```yaml
   version: '3.8'
   
   services:
     grant-management:
       build: .
       ports:
         - "5173:5173"
       volumes:
         - ./data:/app/data
       environment:
         - FLASK_ENV=production
   ```

3. Build and run:
   ```bash
   docker-compose up --build
   ```

#### Option 3: Using systemd (Linux)

1. Create a systemd service file (`/etc/systemd/system/grant-management.service`):
   ```ini
   [Unit]
   Description=Grant Management System
   After=network.target
   
   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/python-app
   ExecStart=/usr/bin/gunicorn --workers 3 --bind unix:grant-management.sock -m 007 app:app
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

2. Enable and start the service:
   ```bash
   sudo systemctl enable grant-management
   sudo systemctl start grant-management
   ```

### Nginx Configuration

Create an Nginx configuration (`/etc/nginx/sites-available/grant-management`):

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://unix:/path/to/python-app/grant-management.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static {
        alias /path/to/python-app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/grant-management /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL Configuration

#### Using Let's Encrypt
1. Install Certbot:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. Obtain certificate:
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

3. Auto-renewal:
   ```bash
   sudo crontab -e
   # Add: 0 12 * * * /usr/bin/certbot renew --quiet
   ```

### Environment Variables

Create a `.env` file for production:

```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DEBUG=False
PORT=5173
HOST=0.0.0.0
```

Load in your application:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Database Migration (Optional)

If you want to move from JSON files to a database:

1. Install database dependencies:
   ```bash
   pip install sqlalchemy psycopg2-binary
   ```

2. Create database models
3. Create migration scripts
4. Update the application to use database instead of JSON files

### Backup Strategy

#### Automated Backup Script
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/path/to/backups"
DATA_DIR="/path/to/python-app/data"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup data files
tar -czf "$BACKUP_DIR/grant_management_$DATE.tar.gz" -C "$DATA_DIR" .

# Keep only last 30 days of backups
find $BACKUP_DIR -name "grant_management_*.tar.gz" -mtime +30 -delete

echo "Backup completed: grant_management_$DATE.tar.gz"
```

Add to crontab for daily backups:
```bash
0 2 * * * /path/to/backup.sh
```

### Monitoring

#### Health Check Endpoint
Add to `app.py`:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
```

#### Log Monitoring
Configure logging in `app.py`:
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/grant-management.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
```

### Security Considerations

1. **Environment Variables**: Never hardcode sensitive information
2. **HTTPS**: Always use SSL in production
3. **Input Validation**: Validate all user inputs
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **Regular Updates**: Keep dependencies updated
6. **Firewall**: Configure firewall rules appropriately

### Performance Optimization

1. **Caching**: Implement Redis or Memcached for caching
2. **Database Indexing**: Add indexes for frequently queried fields
3. **Static Files**: Use CDN for static assets
4. **Compression**: Enable gzip compression
5. **Load Balancing**: Use multiple worker processes

### Troubleshooting

#### Common Issues

1. **Port Already in Use**:
   ```bash
   sudo lsof -i :5173
   sudo kill -9 PID
   ```

2. **Permission Issues**:
   ```bash
   sudo chown -R www-data:www-data /path/to/python-app
   ```

3. **Memory Issues**:
   - Increase worker timeout
   - Optimize database queries
   - Implement pagination

#### Log Analysis
```bash
# View application logs
tail -f logs/grant-management.log

# View Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```
