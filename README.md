# Network-repository
Network Scanning Toolkit (Python-Based Implementation)

This project presents a structured implementation of a lightweight network reconnaissance toolkit developed using Python. It is designed to automate fundamental network scanning operations by interfacing with native system utilities and processing their outputs programmatically.

The primary objective of this project is to demonstrate practical understanding of network discovery techniques, subprocess management in Python, and basic data parsing methodologies. The toolkit encapsulates three core functionalities: host reachability analysis, local network device enumeration, and port/service inspection using Nmap.

Project Components

ping_scanner.py
This module performs host availability checks by executing ICMP echo requests. It determines whether a given host is reachable and extracts response latency metrics where applicable.

arp_scanner.py
This script retrieves and interprets the system’s ARP table to identify devices present within the local network. It maps IP addresses to corresponding MAC addresses and presents the information in a structured format.

nmap_scanner.py
This component integrates with Nmap to perform more advanced scanning operations. It supports multiple scan configurations, including host discovery, port scanning, service version detection, and operating system identification.

Nmap Installation

Nmap is a prerequisite for executing the Nmap scanner module.

Windows
Download the installer from: https://nmap.org/download.html and follow the installation instructions.

Linux
Install via terminal using:
sudo apt install nmap

Mac
If Homebrew is installed, execute:
brew install nmap

To verify successful installation, run:
nmap --version

Execution Instructions

Ensure that Python 3 is installed on your system.

Navigate to the project directory in the terminal and execute the following commands:

python ping_scanner.py
python arp_scanner.py
python nmap_scanner.py

If necessary, replace "python" with "python3" depending on your system configuration.

Usage Overview

Ping Scanner
Upon execution, the user is prompted to specify a target host or a network range. The script evaluates host availability and reports response time metrics.

Example:
Input: google.com
Output: Host is reachable with corresponding latency

ARP Scanner
This script automatically extracts entries from the ARP table and displays detected devices along with their IP and MAC address mappings.

Example:
192.168.1.1 AA:BB:CC:DD:EE

Nmap Scanner
The user is prompted to input a target system or network range and select a desired scan type. The script then executes the appropriate Nmap command and displays the results.

Example:
Target: 192.168.1.1
Scan Type: Port Scan
