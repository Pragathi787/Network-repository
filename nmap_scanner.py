import subprocess
import sys
import datetime
import csv
import re

def log_event(target, scan_type, status):
    # This creates a separate log file for all activity
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("scanner_log.txt", "a") as f:
        f.write(f"[{timestamp}] NMAP - Target: {target}, Scan: {scan_type}, Status: {status}\n")

def check_nmap():
    try:
        subprocess.run(['nmap', '--version'], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False

def format_and_export_nmap(raw_text, target):
    """Parses Nmap output for the terminal and saves data to CSV."""
    print("\nResults:")
    print("=" * 40)
    print(f"{'PORT':<15} {'STATE':<10} {'SERVICE':<15}")
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = raw_text.splitlines()
    found_table = False
    
    # Open CSV for appending results
    with open('nmap_results.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        for line in lines:
            # Look for the port data (e.g., 80/tcp  open  http)
            match = re.match(r'^(\d+/(tcp|udp))\s+(\w+)\s+(.+)$', line.strip())
            if match:
                port, _, state, service = match.groups()
                # 1. Print to Terminal for Screenshot
                print(f"{port:<15} {state:<10} {service:<15}")
                # 2. Export to CSV with Timestamp
                writer.writerow([timestamp, target, port, state, service])
                found_table = True
    
    if not found_table:
        print("No open ports found or host is down.")
    print("=" * 40)

def run_nmap():
    print("=== Nmap Scanner ===")
    if not check_nmap():
        print("Error: Nmap not installed.")
        return

    target = input("Enter target IP or network: ")
    print("\nSelect scan type:")
    print("1. Basic Host Discovery (-sn)")
    print("2. Port Scan (1-1000)")
    print("3. Service Version Detection (-sV)")
    print("4. OS Detection (-O) [Requires sudo/admin]")
    print("5. Custom Port Range (-p)")
    
    choice = input("\nEnter choice (1-5): ")
    
    # Map choices to flags
    flags = {'1':['-sn'], '2':['-p', '1-1000'], '3':['-sV'], '4':['-O'], '5':['-p']}
    cmd = ['nmap'] + flags.get(choice, ['-F'])
    
    if choice == '5':
        ports = input("Enter ports (e.g., 80,443 or 1-500): ")
        cmd.append(ports)
    
    cmd.append(target)
    
    print("\nScanning... (this may take a while)")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            log_event(target, cmd, "Success")
            format_and_export_nmap(result.stdout, target)
            print(f"Full results exported to nmap_results.csv")
        else:
            print(f"Scan failed: {result.stderr}")
            log_event(target, cmd, "Failed")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_nmap()