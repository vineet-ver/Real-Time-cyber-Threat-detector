import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import socket
import struct

class AdvancedThreatDetector:
    """
    Advanced threat detection using multiple ML techniques
    """
    
    def __init__(self):
        # Anomaly detection model
        self.anomaly_model = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        
        # Feature scaler
        self.scaler = StandardScaler()
        
        # Attack signatures
        self.attack_signatures = {
            'port_scan': {
                'threshold_ports': 10,
                'threshold_time': 60  # seconds
            },
            'ddos': {
                'threshold_packets': 1000,
                'threshold_time': 10  # seconds
            },
            'brute_force': {
                'threshold_attempts': 5,
                'threshold_time': 300  # seconds
            }
        }
        
        # Historical data for pattern analysis
        self.connection_history = []
        self.traffic_history = []
        self.is_trained = False
    
    def train_baseline(self, normal_traffic_data):
        """
        Train the anomaly detector on normal traffic patterns
        
        Args:
            normal_traffic_data: List of feature vectors representing normal traffic
        """
        if len(normal_traffic_data) < 50:
            # Generate synthetic normal data if insufficient real data
            normal_traffic_data = self._generate_synthetic_normal_data()
        
        # Scale features
        scaled_data = self.scaler.fit_transform(normal_traffic_data)
        
        # Train anomaly detector
        self.anomaly_model.fit(scaled_data)
        self.is_trained = True
        
        return True
    
    def _generate_synthetic_normal_data(self, n_samples=200):
        """Generate synthetic normal traffic for baseline training"""
        # Simulate normal traffic patterns
        return np.random.rand(n_samples, 8) * np.array([
            100,   # packets_sent
            100,   # packets_recv
            10000, # bytes_sent
            10000, # bytes_recv
            1,     # errin
            1,     # errout
            1,     # dropin
            1      # dropout
        ])
    
    def detect_port_scan(self, connections, time_window=60):
        """
        Detect port scanning attempts
        
        Args:
            connections: List of connection dictionaries
            time_window: Time window in seconds to analyze
        
        Returns:
            List of detected port scan threats
        """
        threats = []
        now = datetime.now()
        
        # Group connections by source IP
        ip_ports = {}
        for conn in connections:
            if 'timestamp' not in conn:
                conn['timestamp'] = now
            
            # Only consider recent connections
            if (now - conn['timestamp']).seconds > time_window:
                continue
            
            source_ip = conn.get('source_ip', 'unknown')
            dest_port = conn.get('dest_port', 0)
            
            if source_ip not in ip_ports:
                ip_ports[source_ip] = set()
            ip_ports[source_ip].add(dest_port)
        
        # Detect scanning behavior
        for ip, ports in ip_ports.items():
            if len(ports) >= self.attack_signatures['port_scan']['threshold_ports']:
                threats.append({
                    'type': 'port_scan',
                    'severity': 'high',
                    'source_ip': ip,
                    'details': f'Port scan detected: {len(ports)} unique ports accessed in {time_window}s',
                    'ports': list(ports)[:20],  # Limit to first 20 ports
                    'timestamp': now.isoformat()
                })
        
        return threats
    
    def detect_ddos(self, traffic_metrics, time_window=10):
        """
        Detect DDoS attack patterns
        
        Args:
            traffic_metrics: Dictionary containing traffic statistics
            time_window: Time window in seconds
        
        Returns:
            Threat dictionary if DDoS detected, None otherwise
        """
        packets_per_second = traffic_metrics.get('packets_recv', 0) / time_window
        bytes_per_second = traffic_metrics.get('bytes_recv', 0) / time_window
        
        # Check for abnormal traffic volume
        if packets_per_second > self.attack_signatures['ddos']['threshold_packets']:
            return {
                'type': 'ddos',
                'severity': 'critical',
                'details': f'Potential DDoS attack: {int(packets_per_second)} packets/sec',
                'metrics': {
                    'packets_per_second': int(packets_per_second),
                    'bytes_per_second': int(bytes_per_second)
                },
                'timestamp': datetime.now().isoformat()
            }
        
        return None
    
    def detect_anomaly(self, traffic_features):
        """
        Use ML to detect traffic anomalies
        
        Args:
            traffic_features: Feature vector for current traffic
        
        Returns:
            Anomaly score and prediction
        """
        if not self.is_trained:
            # Train with current data as baseline
            self.train_baseline([traffic_features])
            return {'is_anomaly': False, 'score': 0}
        
        # Scale features
        scaled_features = self.scaler.transform([traffic_features])
        
        # Predict
        prediction = self.anomaly_model.predict(scaled_features)[0]
        score = self.anomaly_model.score_samples(scaled_features)[0]
        
        return {
            'is_anomaly': prediction == -1,
            'score': float(score),
            'confidence': abs(score) * 100
        }
    
    def analyze_connection_pattern(self, connection):
        """
        Analyze individual connection for suspicious patterns
        
        Args:
            connection: Dictionary containing connection details
        
        Returns:
            Threat dictionary if suspicious, None otherwise
        """
        threats = []
        
        # Check for suspicious ports
        suspicious_ports = [23, 135, 139, 445, 1433, 3389, 5900]  # Telnet, RPC, SMB, SQL, RDP, VNC
        dest_port = connection.get('dest_port', 0)
        
        if dest_port in suspicious_ports:
            threats.append({
                'type': 'suspicious_port',
                'severity': 'medium',
                'details': f'Connection to suspicious port {dest_port}',
                'source_ip': connection.get('source_ip', 'unknown'),
                'dest_port': dest_port,
                'timestamp': datetime.now().isoformat()
            })
        
        # Check for unusual packet sizes
        packet_size = connection.get('packet_size', 0)
        if packet_size > 65000:  # Unusually large packets
            threats.append({
                'type': 'large_packet',
                'severity': 'medium',
                'details': f'Unusually large packet detected: {packet_size} bytes',
                'source_ip': connection.get('source_ip', 'unknown'),
                'timestamp': datetime.now().isoformat()
            })
        
        return threats
    
    def detect_brute_force(self, failed_attempts, time_window=300):
        """
        Detect brute force authentication attempts
        
        Args:
            failed_attempts: List of failed login attempts
            time_window: Time window in seconds
        
        Returns:
            List of brute force threats
        """
        threats = []
        now = datetime.now()
        
        # Group by source IP
        ip_attempts = {}
        for attempt in failed_attempts:
            if (now - attempt['timestamp']).seconds > time_window:
                continue
            
            source_ip = attempt.get('source_ip', 'unknown')
            if source_ip not in ip_attempts:
                ip_attempts[source_ip] = []
            ip_attempts[source_ip].append(attempt)
        
        # Detect brute force patterns
        threshold = self.attack_signatures['brute_force']['threshold_attempts']
        for ip, attempts in ip_attempts.items():
            if len(attempts) >= threshold:
                threats.append({
                    'type': 'brute_force',
                    'severity': 'high',
                    'source_ip': ip,
                    'details': f'Brute force attack: {len(attempts)} failed attempts in {time_window}s',
                    'attempt_count': len(attempts),
                    'timestamp': now.isoformat()
                })
        
        return threats
    
    def get_threat_level(self, threats):
        """
        Calculate overall threat level based on detected threats
        
        Args:
            threats: List of threat dictionaries
        
        Returns:
            Overall threat level (low, medium, high, critical)
        """
        if not threats:
            return 'low'
        
        severity_scores = {
            'low': 1,
            'medium': 2,
            'high': 3,
            'critical': 4
        }
        
        total_score = sum(severity_scores.get(t.get('severity', 'low'), 1) for t in threats)
        avg_score = total_score / len(threats)
        
        if avg_score >= 3.5:
            return 'critical'
        elif avg_score >= 2.5:
            return 'high'
        elif avg_score >= 1.5:
            return 'medium'
        else:
            return 'low'
    
    def generate_threat_report(self, threats, time_period='1h'):
        """
        Generate a comprehensive threat report
        
        Args:
            threats: List of all detected threats
            time_period: Time period for the report
        
        Returns:
            Dictionary containing threat report
        """
        report = {
            'generated_at': datetime.now().isoformat(),
            'time_period': time_period,
            'total_threats': len(threats),
            'threat_breakdown': {},
            'top_threat_sources': {},
            'overall_threat_level': self.get_threat_level(threats)
        }
        
        # Count threats by type
        for threat in threats:
            threat_type = threat.get('type', 'unknown')
            if threat_type not in report['threat_breakdown']:
                report['threat_breakdown'][threat_type] = 0
            report['threat_breakdown'][threat_type] += 1
            
            # Track source IPs
            source_ip = threat.get('source_ip', 'unknown')
            if source_ip not in report['top_threat_sources']:
                report['top_threat_sources'][source_ip] = 0
            report['top_threat_sources'][source_ip] += 1
        
        # Sort top sources
        report['top_threat_sources'] = dict(
            sorted(report['top_threat_sources'].items(), 
                   key=lambda x: x[1], 
                   reverse=True)[:10]
        )
        
        return report


class NetworkScanner:
    """
    Network scanning utilities for investigating suspicious IPs
    """
    
    @staticmethod
    def scan_port(ip, port, timeout=1):
        """
        Scan a single port on target IP
        
        Args:
            ip: Target IP address
            port: Port number to scan
            timeout: Timeout in seconds
        
        Returns:
            True if port is open, False otherwise
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    @staticmethod
    def scan_common_ports(ip, timeout=1):
        """
        Scan common ports on target IP
        
        Args:
            ip: Target IP address
            timeout: Timeout in seconds
        
        Returns:
            Dictionary of open ports with service names
        """
        common_ports = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            445: 'SMB',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            5900: 'VNC',
            8080: 'HTTP-Alt'
        }
        
        open_ports = {}
        for port, service in common_ports.items():
            if NetworkScanner.scan_port(ip, port, timeout):
                open_ports[port] = service
        
        return open_ports
    
    @staticmethod
    def get_ip_info(ip):
        """
        Get information about an IP address
        
        Args:
            ip: IP address
        
        Returns:
            Dictionary containing IP information
        """
        info = {
            'ip': ip,
            'hostname': 'unknown',
            'is_private': False,
            'is_loopback': False
        }
        
        try:
            # Get hostname
            info['hostname'] = socket.gethostbyaddr(ip)[0]
        except:
            pass
        
        # Check if private IP
        octets = ip.split('.')
        if len(octets) == 4:
            first = int(octets[0])
            second = int(octets[1])
            
            if first == 10:
                info['is_private'] = True
            elif first == 172 and 16 <= second <= 31:
                info['is_private'] = True
            elif first == 192 and second == 168:
                info['is_private'] = True
            elif first == 127:
                info['is_loopback'] = True
        
        return info