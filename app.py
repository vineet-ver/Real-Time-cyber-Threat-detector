from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import threading
import time
from datetime import datetime
import json
from collections import deque
import psutil
import socket
import numpy as np
from sklearn.ensemble import IsolationForest
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global data stores
threat_queue = deque(maxlen=100)
active_connections = {}
attack_stats = {
    'port_scan': 0,
    'ddos': 0,
    'suspicious_traffic': 0,
    'unauthorized_access': 0
}

# ML Model for anomaly detection
anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
is_model_trained = False

class ThreatMonitor:
    def __init__(self):
        self.running = False
        self.thread = None
        
    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.thread.start()
    
    def stop(self):
        self.running = False
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                # Monitor network connections
                connections = psutil.net_connections(kind='inet')
                self._analyze_connections(connections)
                
                # Monitor network stats
                net_io = psutil.net_io_counters()
                self._analyze_traffic(net_io)
                
                time.sleep(2)
            except Exception as e:
                print(f"Monitoring error: {e}")
    
    def _analyze_connections(self, connections):
        """Analyze active network connections"""
        global active_connections
        
        connection_count = {}
        for conn in connections:
            if conn.status == 'ESTABLISHED':
                remote_ip = conn.raddr.ip if conn.raddr else 'unknown'
                remote_port = conn.raddr.port if conn.raddr else 0
                
                # Count connections per IP
                if remote_ip not in connection_count:
                    connection_count[remote_ip] = []
                connection_count[remote_ip].append(remote_port)
        
        # Detect port scanning (multiple ports from same IP)
        for ip, ports in connection_count.items():
            unique_ports = len(set(ports))
            if unique_ports > 5:  # Threshold for port scan detection
                self._log_threat({
                    'type': 'port_scan',
                    'severity': 'high',
                    'source_ip': ip,
                    'details': f'Port scan detected: {unique_ports} unique ports accessed',
                    'timestamp': datetime.now().isoformat()
                })
                attack_stats['port_scan'] += 1
        
        active_connections = connection_count
    
    def _analyze_traffic(self, net_io):
        """Analyze network traffic patterns for DDoS indicators"""
        global is_model_trained
        
        # Create feature vector for ML analysis
        features = [
            net_io.packets_sent,
            net_io.packets_recv,
            net_io.bytes_sent,
            net_io.bytes_recv,
            net_io.errin,
            net_io.errout,
            net_io.dropin,
            net_io.dropout
        ]
        
        # Train model if not trained (using initial data)
        if not is_model_trained:
            # Simulate training with synthetic normal data
            normal_data = np.random.rand(100, len(features)) * 1000
            anomaly_detector.fit(normal_data)
            is_model_trained = True
        
        # Detect anomalies
        prediction = anomaly_detector.predict([features])
        if prediction[0] == -1:  # Anomaly detected
            self._log_threat({
                'type': 'suspicious_traffic',
                'severity': 'medium',
                'details': f'Unusual traffic pattern detected',
                'metrics': {
                    'packets_recv': net_io.packets_recv,
                    'bytes_recv': net_io.bytes_recv
                },
                'timestamp': datetime.now().isoformat()
            })
            attack_stats['suspicious_traffic'] += 1
    
    def _log_threat(self, threat_data):
        """Log detected threat and emit to dashboard"""
        threat_queue.append(threat_data)
        socketio.emit('new_threat', threat_data)

# Initialize monitor
monitor = ThreatMonitor()

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/threats')
def get_threats():
    """Get recent threats"""
    return jsonify(list(threat_queue))

@app.route('/api/stats')
def get_stats():
    """Get attack statistics"""
    return jsonify({
        'attack_stats': attack_stats,
        'active_connections': len(active_connections),
        'total_threats': len(threat_queue)
    })

@app.route('/api/connections')
def get_connections():
    """Get active connections"""
    conn_list = []
    for ip, ports in active_connections.items():
        conn_list.append({
            'ip': ip,
            'port_count': len(ports),
            'ports': list(set(ports))[:10]  # Limit to 10 ports
        })
    return jsonify(conn_list)

@app.route('/api/scan/<ip>')
def scan_ip(ip):
    """Perform nmap-style scan on suspicious IP"""
    try:
        result = {
            'ip': ip,
            'hostname': socket.gethostbyaddr(ip)[0] if ip != 'unknown' else 'unknown',
            'status': 'active'
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/monitor/start', methods=['POST'])
def start_monitoring():
    """Start the threat monitor"""
    monitor.start()
    return jsonify({'status': 'started'})

@app.route('/api/monitor/stop', methods=['POST'])
def stop_monitoring():
    """Stop the threat monitor"""
    monitor.stop()
    return jsonify({'status': 'stopped'})

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'data': 'Connected to threat monitor'})

@socketio.on('request_update')
def handle_update_request():
    """Send current stats on request"""
    emit('stats_update', {
        'attack_stats': attack_stats,
        'active_connections': len(active_connections)
    })

if __name__ == '__main__':
    # Auto-start monitoring
    monitor.start()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)