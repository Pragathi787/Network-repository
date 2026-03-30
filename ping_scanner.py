import subprocess
import platform
import re
import csv
import datetime

# Bonus: Logging function with timestamps
def write_log(msg):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("scanner_log.txt", "a") as f:
        f.write(f"[{now}] {msg}\n")

def get_ping_stats(target):
    # Detect OS for correct flags
    os_type = platform.system().lower()
    flag = "-n" if os_type == "windows" else "-c"
    
    try:
        # Run command with a 2-second timeout per ping
        res = subprocess.run(['ping', flag, '1', target], capture_output=True, text=True, timeout=5)
        
        if res.returncode == 0:
            # Look for the time in the output (works for most systems)
            time_match = re.search(r'time=([\d.]+)', res.stdout)
            avg_time = time_match.group(1) if time_match else "N/A"
            write_log(f"Success: {target} responded in {avg_time}ms")
            return "Reachable", f"{avg_time}ms"
        else:
            write_log(f"Failed: {target} was unreachable")
            return "Unreachable", "N/A"
            
    except Exception as e:
        write_log(f"Error: Could not scan {target}. {e}")
        return "Error", "N/A"

if __name__ == "__main__":
    print("=== Ping Scanner ===")
    
    choice = input("Ping single host? (y/n): ").lower()
    results_list = []

    if choice == 'y':
        host = input("Enter hostname or IP: ")
        status, time = get_ping_stats(host)
        print(f"Host: {host}")
        print(f"Status: {status}")
        print(f"Average Time: {time}")
        results_list.append({"Host": host, "Status": status, "Time": time})
        
    else:
        # Bonus: Network Range Scanning
        network_prefix = input("Enter network prefix (e.g., 192.168.1): ")
        print(f"Scanning range {network_prefix}.1 to {network_prefix}.10...") 
        # Range limited to 10 for the demo screenshot so it's fast
        for i in range(1, 11):
            target_ip = f"{network_prefix}.{i}"
            status, time = get_ping_stats(target_ip)
            if status == "Reachable":
                print(f"[+] {target_ip}: {status} ({time})")
                results_list.append({"Host": target_ip, "Status": status, "Time": time})

    # Bonus: Export results to CSV
    if results_list:
        with open('ping_results.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Host", "Status", "Time"])
            writer.writeheader()
            writer.writerows(results_list)
        print("\n[!] Results exported to ping_results.csv")