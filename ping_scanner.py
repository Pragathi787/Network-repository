import subprocess
import platform
import re
import csv
from datetime import datetime


# simple function to save logs (just for tracking what happened)
def save_log(text):
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("ping_activity.log", "a") as log:
        log.write(f"[{time_stamp}] {text}\n")


def run_ping(target_ip):
    """
    Sends one ping request and checks if the host responds.
    Also tries to get response time if available.
    """

    system_os = platform.system().lower()

    # different flag for windows vs linux/mac
    count_flag = "-n" if system_os == "windows" else "-c"

    try:
        process = subprocess.run(
            ["ping", count_flag, "1", target_ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )

        output = process.stdout

        if process.returncode == 0:
            # extracting time (format may vary slightly across systems)
            match = re.search(r"time[=<]?([\d.]+)", output)

            if match:
                ping_time = match.group(1) + "ms"
            else:
                ping_time = "Unknown"

            save_log(f"{target_ip} responded ({ping_time})")
            return True, ping_time

        else:
            save_log(f"{target_ip} did not respond")
            return False, "N/A"

    except Exception as error:
        save_log(f"Error scanning {target_ip}: {error}")
        return False, "Error"


def single_scan():
    target = input("Enter IP or domain: ").strip()

    success, response = run_ping(target)

    print("\nResult:")
    print(f"Target: {target}")
    print(f"Status: {'Reachable' if success else 'Unreachable'}")
    print(f"Response Time: {response}")

    return [{"Host": target, "Status": "Reachable" if success else "Unreachable", "Time": response}]


def range_scan():
    base = input("Enter network prefix (example: 192.168.1): ").strip()
    collected = []

    print(f"\nChecking {base}.1 to {base}.10...\n")

    for num in range(1, 11):
        ip = f"{base}.{num}"

        success, response = run_ping(ip)

        if success:
            print(f"{ip} is active ({response})")

            collected.append({
                "Host": ip,
                "Status": "Reachable",
                "Time": response
            })

    return collected


def export_to_csv(data):
    # saving results for later use
    with open("ping_output.csv", "w", newline="") as file:
        field_names = ["Host", "Status", "Time"]

        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data)

    print("\nResults saved in ping_output.csv")


def main():
    print("=== Ping Utility ===")

    user_input = input("Scan single host? (y/n): ").strip().lower()

    if user_input == "y":
        results = single_scan()
    else:
        results = range_scan()

    if results:
        export_to_csv(results)


if __name__ == "__main__":
    main()
