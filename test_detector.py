"""
Testing and demonstration script for the Cyber Threat Detector
This script simulates various attack patterns for testing
"""

import requests
import time
import socket
import threading
from datetime import datetime

BASE_URL = "http://localhost:5000"

class ThreatSimulator:
    """Simulate various cyber threats for testing"""
    
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        
    def simulate_port_scan(self, target_ip="127.0.0.1", num_ports=15):
        """
        Simulate a port scanning attack
        Creates multiple connections to different ports
        """
        print(f"\n🔍 Simulating Port Scan Attack on {target_ip}")
        print(f"   Scanning {num_ports} ports...")
        
        ports = [21, 22, 23, 25, 80, 110, 143, 443, 445, 3306, 3389, 5432, 5900, 8080, 8443]
        
        for port in ports[:num_ports]:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                sock.connect_ex((target_ip, port))
                sock.close()
                print(f"   ✓ Probed port {port}")
                time.sleep(0.1)
            except Exception as e:
                print(f"   ✗ Port {port} failed: {e}")
        
        print("   ✅ Port scan simulation complete")
        time.sleep(2)
        self.check_threats()
    
    def simulate_ddos(self, duration=5):
        """
        Simulate DDoS-like traffic pattern
        Generates high volume of requests
        """
        print(f"\n⚠️  Simulating DDoS Attack Pattern")
        print(f"   Duration: {duration} seconds")
        
        start_time = time.time()
        request_count = 0
        
        def send_requests():
            nonlocal request_count
            while time.time() - start_time < duration:
                try:
                    requests.get(f"{self.base_url}/api/stats", timeout=0.5)
                    request_count += 1
                except:
                    pass
        
        # Launch multiple threads
        threads = []
        for i in range(10):
            t = threading.Thread(target=send_requests)
            t.start()
            threads.append(t)
        
        # Wait for completion
        for t in threads:
            t.join()
        
        print(f"   ✅ Sent {request_count} requests in {duration}s")
        time.sleep(2)
        self.check_threats()
    
    def simulate_suspicious_connection(self):
        """
        Simulate connection to suspicious ports
        """
        print(f"\n🚩 Simulating Suspicious Port Access")
        
        suspicious_ports = [23, 445, 3389, 5900]  # Telnet, SMB, RDP, VNC
        
        for port in suspicious_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                sock.connect_ex(("127.0.0.1", port))
                sock.close()
                print(f"   ✓ Attempted connection to suspicious port {port}")
                time.sleep(0.5)
            except:
                pass
        
        print("   ✅ Suspicious connection simulation complete")
        time.sleep(2)
        self.check_threats()
    
    def check_threats(self):
        """Check and display detected threats"""
        try:
            response = requests.get(f"{self.base_url}/api/threats")
            threats = response.json()
            
            print(f"\n📊 Threats Detected: {len(threats)}")
            
            if threats:
                print("\n   Recent threats:")
                for threat in threats[-5:]:  # Show last 5
                    print(f"   - [{threat['type']}] {threat['details']}")
                    print(f"     Severity: {threat['severity']} | Time: {threat.get('timestamp', 'N/A')}")
            else:
                print("   No threats detected yet")
                
        except Exception as e:
            print(f"   ✗ Error fetching threats: {e}")
    
    def check_stats(self):
        """Display current statistics"""
        try:
            response = requests.get(f"{self.base_url}/api/stats")
            stats = response.json()
            
            print("\n📈 Current Statistics:")
            print(f"   Port Scans: {stats['attack_stats']['port_scan']}")
            print(f"   DDoS Patterns: {stats['attack_stats']['ddos']}")
            print(f"   Suspicious Traffic: {stats['attack_stats']['suspicious_traffic']}")
            print(f"   Active Connections: {stats['active_connections']}")
            print(f"   Total Threats: {stats['total_threats']}")
            
        except Exception as e:
            print(f"   ✗ Error fetching stats: {e}")
    
    def start_monitor(self):
        """Start the threat monitor"""
        try:
            response = requests.post(f"{self.base_url}/api/monitor/start")
            print(f"✅ Monitor started: {response.json()}")
        except Exception as e:
            print(f"✗ Error starting monitor: {e}")
    
    def stop_monitor(self):
        """Stop the threat monitor"""
        try:
            response = requests.post(f"{self.base_url}/api/monitor/stop")
            print(f"⏸️  Monitor stopped: {response.json()}")
        except Exception as e:
            print(f"✗ Error stopping monitor: {e}")
    
    def run_full_demo(self):
        """
        Run a complete demonstration of all threat types
        """
        print("="*60)
        print("🚨 CYBER THREAT DETECTOR - FULL DEMO")
        print("="*60)
        
        # Start monitor
        print("\n▶️  Starting threat monitor...")
        self.start_monitor()
        time.sleep(2)
        
        # Initial stats
        self.check_stats()
        time.sleep(2)
        
        # Simulate various attacks
        self.simulate_port_scan(num_ports=12)
        time.sleep(3)
        
        self.simulate_suspicious_connection()
        time.sleep(3)
        
        self.simulate_ddos(duration=3)
        time.sleep(3)
        
        # Final stats
        print("\n" + "="*60)
        print("📊 FINAL RESULTS")
        print("="*60)
        self.check_stats()
        self.check_threats()
        
        print("\n✅ Demo complete! Check the dashboard at http://localhost:5000")
        print("="*60)


def test_api_endpoints():
    """Test all API endpoints"""
    print("\n🧪 Testing API Endpoints\n")
    
    endpoints = [
        ("GET", "/api/stats", None),
        ("GET", "/api/threats", None),
        ("GET", "/api/connections", None),
        ("POST", "/api/monitor/start", None),
        ("GET", "/api/scan/127.0.0.1", None),
    ]
    
    for method, endpoint, data in endpoints:
        try:
            url = f"{BASE_URL}{endpoint}"
            if method == "GET":
                response = requests.get(url, timeout=5)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=5)
            
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {method} {endpoint} - Status: {response.status_code}")
            
        except Exception as e:
            print(f"❌ {method} {endpoint} - Error: {e}")
        
        time.sleep(0.5)


def stress_test(duration=10, threads=5):
    """
    Perform stress test on the application
    """
    print(f"\n⚡ Running Stress Test")
    print(f"   Duration: {duration}s | Threads: {threads}")
    
    start_time = time.time()
    request_count = [0]
    error_count = [0]
    
    def make_requests():
        while time.time() - start_time < duration:
            try:
                response = requests.get(f"{BASE_URL}/api/stats", timeout=1)
                if response.status_code == 200:
                    request_count[0] += 1
                else:
                    error_count[0] += 1
            except:
                error_count[0] += 1
            time.sleep(0.1)
    
    # Launch threads
    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=make_requests)
        t.start()
        thread_list.append(t)
    
    # Wait for completion
    for t in thread_list:
        t.join()
    
    elapsed = time.time() - start_time
    rps = request_count[0] / elapsed
    
    print(f"\n   Results:")
    print(f"   ✓ Successful requests: {request_count[0]}")
    print(f"   ✗ Failed requests: {error_count[0]}")
    print(f"   📊 Requests per second: {rps:.2f}")
    print(f"   ⏱️  Total time: {elapsed:.2f}s")


def interactive_menu():
    """Interactive testing menu"""
    simulator = ThreatSimulator()
    
    while True:
        print("\n" + "="*60)
        print("🚨 CYBER THREAT DETECTOR - TEST MENU")
        print("="*60)
        print("1. Run Full Demo")
        print("2. Simulate Port Scan")
        print("3. Simulate DDoS Attack")
        print("4. Simulate Suspicious Connection")
        print("5. Check Current Stats")
        print("6. Check Detected Threats")
        print("7. Test API Endpoints")
        print("8. Run Stress Test")
        print("9. Start Monitor")
        print("10. Stop Monitor")
        print("0. Exit")
        print("="*60)
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            simulator.run_full_demo()
        elif choice == "2":
            num_ports = input("Number of ports to scan (default 15): ").strip()
            num_ports = int(num_ports) if num_ports else 15
            simulator.simulate_port_scan(num_ports=num_ports)
        elif choice == "3":
            duration = input("Duration in seconds (default 5): ").strip()
            duration = int(duration) if duration else 5
            simulator.simulate_ddos(duration=duration)
        elif choice == "4":
            simulator.simulate_suspicious_connection()
        elif choice == "5":
            simulator.check_stats()
        elif choice == "6":
            simulator.check_threats()
        elif choice == "7":
            test_api_endpoints()
        elif choice == "8":
            duration = input("Duration in seconds (default 10): ").strip()
            threads = input("Number of threads (default 5): ").strip()
            duration = int(duration) if duration else 10
            threads = int(threads) if threads else 5
            stress_test(duration=duration, threads=threads)
        elif choice == "9":
            simulator.start_monitor()
        elif choice == "10":
            simulator.stop_monitor()
        elif choice == "0":
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    import sys
    
    print("🚨 Cyber Threat Detector - Testing Suite")
    print("Make sure the application is running on http://localhost:5000\n")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/api/stats", timeout=2)
        print("✅ Server is running!\n")
    except:
        print("❌ Error: Server is not responding!")
        print("   Please start the application first: python app.py\n")
        sys.exit(1)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo":
            simulator = ThreatSimulator()
            simulator.run_full_demo()
        elif sys.argv[1] == "--test":
            test_api_endpoints()
        elif sys.argv[1] == "--stress":
            duration = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            threads = int(sys.argv[3]) if len(sys.argv) > 3 else 5
            stress_test(duration, threads)
        elif sys.argv[1] == "--port-scan":
            simulator = ThreatSimulator()
            simulator.simulate_port_scan()
        elif sys.argv[1] == "--ddos":
            simulator = ThreatSimulator()
            simulator.simulate_ddos()
        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print("\nUsage:")
            print("  python test_detector.py              # Interactive menu")
            print("  python test_detector.py --demo       # Run full demo")
            print("  python test_detector.py --test       # Test API endpoints")
            print("  python test_detector.py --stress     # Run stress test")
            print("  python test_detector.py --port-scan  # Simulate port scan")
            print("  python test_detector.py --ddos       # Simulate DDoS")
    else:
        # Run interactive menu
        interactive_menu()