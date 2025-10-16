import os

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Detection thresholds
    PORT_SCAN_THRESHOLD = int(os.environ.get('PORT_SCAN_THRESHOLD', 10))
    DDOS_PACKET_THRESHOLD = int(os.environ.get('DDOS_PACKET_THRESHOLD', 1000))
    BRUTE_FORCE_THRESHOLD = int(os.environ.get('BRUTE_FORCE_THRESHOLD', 5))
    
    # Time windows (in seconds)
    PORT_SCAN_TIME_WINDOW = int(os.environ.get('PORT_SCAN_TIME_WINDOW', 60))
    DDOS_TIME_WINDOW = int(os.environ.get('DDOS_TIME_WINDOW', 10))
    BRUTE_FORCE_TIME_WINDOW = int(os.environ.get('BRUTE_FORCE_TIME_WINDOW', 300))
    
    # Monitoring settings
    MONITOR_INTERVAL = int(os.environ.get('MONITOR_INTERVAL', 2))  # seconds
    MAX_STORED_THREATS = int(os.environ.get('MAX_STORED_THREATS', 100))
    MAX_CONNECTION_HISTORY = int(os.environ.get('MAX_CONNECTION_HISTORY', 1000))
    
    # ML Model settings
    ANOMALY_CONTAMINATION = float(os.environ.get('ANOMALY_CONTAMINATION', 0.1))
    MODEL_RETRAIN_INTERVAL = int(os.environ.get('MODEL_RETRAIN_INTERVAL', 3600))  # seconds
    
    # Alert settings
    ALERT_EMAIL = os.environ.get('ALERT_EMAIL', None)
    ALERT_WEBHOOK = os.environ.get('ALERT_WEBHOOK', None)
    ENABLE_EMAIL_ALERTS = os.environ.get('ENABLE_EMAIL_ALERTS', 'False').lower() == 'true'
    ENABLE_WEBHOOK_ALERTS = os.environ.get('ENABLE_WEBHOOK_ALERTS', 'False').lower() == 'true'
    
    # Suspicious ports to monitor
    SUSPICIOUS_PORTS = [
        21,    # FTP
        23,    # Telnet
        135,   # MS RPC
        139,   # NetBIOS
        445,   # SMB
        1433,  # MS SQL
        3389,  # RDP
        5900,  # VNC
        6667,  # IRC
        31337  # Back Orifice
    ]
    
    # Whitelisted IPs (won't trigger alerts)
    WHITELISTED_IPS = os.environ.get('WHITELISTED_IPS', '127.0.0.1,::1').split(',')
    
    # Blacklisted IPs (auto-block)
    BLACKLISTED_IPS = os.environ.get('BLACKLISTED_IPS', '').split(',') if os.environ.get('BLACKLISTED_IPS') else []
    
    # Rate limiting
    RATE_LIMIT_ENABLED = os.environ.get('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT_REQUESTS = int(os.environ.get('RATE_LIMIT_REQUESTS', 100))
    RATE_LIMIT_WINDOW = int(os.environ.get('RATE_LIMIT_WINDOW', 60))  # seconds
    
    # Database (optional - for persistent storage)
    DATABASE_URL = os.environ.get('DATABASE_URL', None)
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'threat_detector.log')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    PORT_SCAN_THRESHOLD = 5  # Lower threshold for testing
    MONITOR_INTERVAL = 5


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in production")


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    PORT_SCAN_THRESHOLD = 3
    MONITOR_INTERVAL = 1


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration based on environment"""
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])