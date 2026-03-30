import subprocess
import platform
import re
import csv
import datetime

def log_arp_activity(count):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("scanner_log.txt", "a") as f:
        f.write(f"[{timestamp}] ARP SCAN - Found {count} entries.\n")

def run_arp_scan():
    print("=== ARP Table Scanner ===")
    os_type = platform.system().lower()
    cmd = ['arp', '-a']
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        raw_data = result.stdout
        
        # Regex for IP and MAC
        ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        mac_pattern = r'([0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2})'
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'IP Address':<20} {'MAC Address':<20}")
        print("-" * 40)
        
        entries = []
        lines = raw_data.splitlines()
        for line in lines:
            ip = re.search(ip_pattern, line)
            mac = re.search(mac_pattern, line)
            if ip and mac:
                print(f"{ip.group(1):<20} {mac.group(1):<20}")
                entries.append([timestamp, ip.group(1), mac.group(1)])
        
        # Save to CSV (Bonus)
        if entries:
            with open('arp_results.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(entries)
            print("-" * 40)
            print(f"Total entries: {len(entries)}")
            print("Results exported to arp_results.csv")
            log_arp_activity(len(entries))
        else:
            print("No ARP entries found.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_arp_scan()