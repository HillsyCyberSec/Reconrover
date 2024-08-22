Welcome to Reconrover.py, I've created this script mainly for CTF's / Bug bounties but may come in handy for some smaller project work.

Prerequisite:
- You must have Seclists installed
- This currently works on Linux, i have not tested on MAC / Windows.

What does the script do;

When you initially run the script you will be faced with the screen below:
![image](https://github.com/user-attachments/assets/6a9304c0-8b1b-407c-891a-9a3237e01662)

I've left this as "Company" but you can enter anything here, the CTF you're playing, project you're working on etc. Next the script will ask if you're scanning a file or single ip/domain you can use either
- File
- Single

Depending on your response the script will either ask for a IP or the directory/file you want to use.

Once you've begun your project and entered the required information the script will intiialise with an nmap scan, this will be a service/script scan.

![image](https://github.com/user-attachments/assets/ce381d45-0efc-4f13-95e9-a6f1f283dde2)

Depending on what the scan detects being open the script will carry out further recon, currently supported is HTTP/HTTPS & FTP.

If FTP anonymous access is allowed the script will then login anonymously and record which files you have access to.
If HTTP / HTTP(S) is detected the script will then; 
Run both Gobuster & Subfinder against some standard Seclists, The script will also navigate to the website and record a text output.

![image](https://github.com/user-attachments/assets/40fecc07-99e2-41d9-b690-a8ebdf80be66)

Once the script has completed you will find the outputs recorded in the directory in which the script was run.

In this instance we have the folder "ScriptTest"
![image](https://github.com/user-attachments/assets/082a01d4-eb92-4546-87bf-d7b6f878826e)

Depending on your options (single scan or file) you will find a folder(s) inside the folder amended with the IP address or domain of each asset, in this case i've renamed mine to [IP1] and [IP2]

![image](https://github.com/user-attachments/assets/73f31f9c-5dcc-465f-9fad-e48836bdd1ff)

Within these folders you will find more folders with their respective results, if the nmap scan did not detect certain services they will not have any folders as we can see below.

![image](https://github.com/user-attachments/assets/1c2f528b-f596-4a5a-ab3b-dc697cfd76b6)

![image](https://github.com/user-attachments/assets/467873f1-1ad6-43d6-b8de-25d2f7deb8ab)

- I ran this script against Metasploitable2 and MrRobot from TryHackMe.
