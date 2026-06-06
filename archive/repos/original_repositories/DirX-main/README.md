![Python](https://img.shields.io/badge/Python-3.x-blue)
![Version](https://img.shields.io/badge/Version-1.0-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)
![GitHub stars](https://img.shields.io/github/stars/Krish-Patwa01/dirx?style=social)
![GitHub forks](https://img.shields.io/github/forks/Krish-Patwa01/dirx?style=social)

# ⚡ DirX

```
██████╗ ██╗██████╗ ██╗  ██╗
██╔══██╗██║██╔══██╗╚██╗██╔╝
██║  ██║██║██████╔╝ ╚███╔╝ 
██║  ██║██║██╔══██╗ ██╔██╗ 
██████╔╝██║██║  ██║██╔╝ ██╗
╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
```

 Fastest Directory Bruteforce Tool


##  What is DirX?

**DirX** is a high-performance directory brute-forcing tool designed for **penetration testers, bug bounty hunters, and security researchers**.

It helps uncover hidden directories, endpoints, and sensitive files on web servers with speed and precision.

---

##  Features

*  **Blazing Fast Async Engine**
*  **Status Code Filtering** (`--status`)
*  **Exclude Unwanted Responses** (`--exclude`)
*  **Proxy Support** (Burp Suite / ZAP)
*  **Live Progress Bar + ETA**
*  **Colorized Output (Hacker Style)**
*  **Accessible URLs Highlighted**
*  **Clean & Noise-Free Output**



##  Installation

```bash
git clone https://github.com/yourusername/dirx.git
cd dirx
pip install -r requirements.txt
```



##  Usage

```bash
python3 dirx.py -u <target> -w <wordlist>
```



##  Examples

```bash
# Basic Scan
python3 dirx.py -u https://example.com -w wordlist.txt

# High Speed
python3 dirx.py -u https://target.com -w list.txt -t 30

# Filter Status Codes
python3 dirx.py -u https://target.com -w list.txt --status 200,403

# Exclude Responses
python3 dirx.py -u https://target.com -w list.txt --exclude 404,500

# Proxy (Burp Suite)
python3 dirx.py -u https://target.com -w list.txt --proxy http://127.0.0.1:8080
```



## 🖥️ Output Preview
```
/admin          200   5321B      -> https://target.com/admin
/login          403   721B
/test           406   226B

[████████████░░░░░░░] 65% (3000/4613) | ETA: 00:20
```



##  Disclaimer

This tool is strictly for **educational purposes and authorized security testing only**.
Unauthorized usage is illegal.



##  Support

If you like DirX, give it a ⭐ and share it with the community.



##  Tagline

> Connecting Hackers With Purpose
