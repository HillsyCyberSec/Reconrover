import subprocess
import os
import requests
from ftplib import FTP

# ASCII Art Welcome Message
def print_welcome_message():
    welcome_message = """
______                    ______                    
| ___ \                   | ___ \                   
| |_/ /___  ___ ___  _ __ | |_/ /_____   _____ _ __ 
|    // _ \/ __/ _ \| '_ \|    // _ \ \ / / _ \ '__|
| |\ \  __/ (_| (_) | | | | |\ \ (_) \ V /  __/ |   
\_| \_\___|\___\___/|_| |_\_| \_\___/ \_/ \___|_|
                                              
                                              
    """
    print(welcome_message)

def create_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

def run_gobuster(target_domain, company_name):
    print(f"Running Gobuster scans on {target_domain} for {company_name}...")
    directory_wordlist = "/usr/share/wordlists/seclists/Discovery/Web-Content/common.txt"
    directory_output_file = f"{company_name}/{target_domain}/gobuster/directories_{target_domain}.txt"
    create_directory(f"{company_name}/{target_domain}/gobuster")
    gobuster_command = [
        "gobuster", "dir",
        "-u", target_domain,
        "-w", directory_wordlist,
        "-o", directory_output_file,
        "-q"
    ]
    subprocess.run(gobuster_command)

def run_subfinder(target_domain, company_name):
    print(f"Running Subfinder scans on {target_domain} for {company_name}...")
    subdomain_output_file = f"{company_name}/{target_domain}/subfinder/subdomains_{target_domain}.txt"
    create_directory(f"{company_name}/{target_domain}/subfinder")
    subfinder_command = [
        "subfinder",
        "-d", target_domain,
        "-o", subdomain_output_file
    ]
    subprocess.run(subfinder_command)

def run_nmap_scan(target_domain, company_name):
    print(f"Running Nmap service scan for {target_domain}...")
    create_directory(f"{company_name}/{target_domain}/nmap")

    nmap_output_file_xml = f"{company_name}/{target_domain}/nmap/nmap_output_{target_domain}.xml"
    nmap_output_file_txt = f"{company_name}/{target_domain}/nmap/nmap_output_{target_domain}.txt"

    nmap_command = ["nmap", "-sC", "-sV", "-oX", nmap_output_file_xml, "-oN", nmap_output_file_txt, target_domain]
    subprocess.run(nmap_command)

    return nmap_output_file_txt

def process_http_services(ip, company_name):
    print(f"Processing HTTP/HTTPS services for {ip}...")
    try:
        response = requests.get(f"http://{ip}")
        website_content = response.text

        create_directory(f"{company_name}/{ip}/http")
        with open(f"{company_name}/{ip}/http/http_content_{ip}.txt", "w") as file:
            file.write(website_content)

    except requests.exceptions.RequestException as e:
        print(f"Failed to capture HTTP content for {ip}: {e}")

def process_ftp_service(ip, company_name):
    print(f"Processing FTP service for {ip}...")
    try:
        ftp = FTP(ip)
        ftp.login()
        files = ftp.nlst()

        create_directory(f"{company_name}/{ip}/ftp")
        with open(f"{company_name}/{ip}/ftp/ftp_files_{ip}.txt", "w") as file:
            for file_name in files:
                file.write(f"{file_name}\n")

        ftp.quit()
    except Exception as e:
        print(f"FTP anonymous login failed: {e}")
        print(f"Failed to list FTP files for {ip}.")

def process_target(target, company_name):
    nmap_output_file = run_nmap_scan(target, company_name)

    http_services = False
    ftp_services = False
    
    with open(nmap_output_file, "r") as file:
        for line in file:
            if "80/tcp" in line or "443/tcp" in line:
                http_services = True
            if "21/tcp" in line:
                ftp_services = True

    if http_services:
        process_http_services(target, company_name)
        run_gobuster(target, company_name)
        run_subfinder(target, company_name)

    if ftp_services:
        process_ftp_service(target, company_name)

def main():
    print_welcome_message()

    company_name = input("Enter the company name: ")
    choice = input("Do you want to provide a file with multiple IPs/domains or a single IP/domain? (file/single): ").strip().lower()

    if choice == "file":
        input_file = input("Enter the path to the file containing IPs or domains: ")

        if not os.path.isfile(input_file):
            print(f"File {input_file} does not exist.")
            return

        with open(input_file, "r") as file:
            for line in file:
                target = line.strip()
                if target:
                    process_target(target, company_name)

    elif choice == "single":
        target_domain = input("Enter the target domain or IP address: ").strip()
        process_target(target_domain, company_name)

    else:
        print("Invalid choice. Please enter 'file' or 'single'.")
        return

    print("Script completed successfully!")

if __name__ == "__main__":
    main()

