import requests
import json
import os
import time
import random
from colorama import init, Fore, Style

init(autoreset=True)

# === CONFIGURATION ===
API_BASE = "https://exploitsindia.site/anish/api.php?key=Imlasahu&num=number"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Termux) Gecko/117.0 Firefox/117.0",
    "Accept": "application/json, text/plain, */*",
    "Connection": "keep-alive"
}

# === Typing Animation ===
def type_effect(text, delay=0.002):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# === Swipe-style Text Animation ===
def swipe_effect(text, delay=0.01):
    for line in text.splitlines():
        for char in line:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

# === Banner ===
def show_banner():
    os.system("clear")
    ascii_banner = f"""{Fore.GREEN}

                _   _ _____  _____ _    _     ________   _______  _      ____ _____ _______ _____  
     /\   | \ | |_   _|/ ____| |  | |   |  ____\ \ / /  __ \| |    / __ \_   _|__   __/ ____| 
    /  \  |  \| | | | | (___ | |__| |   | |__   \ V /| |__) | |   | |  | || |    | | | (___   
   / /\ \ | . ` | | |  \___ \|  __  |   |  __|   > < |  ___/| |   | |  | || |    | |  \___ \  
  / ____ \| |\  |_| |_ ____) | |  | |   | |____ / . \| |    | |___| |__| || |_   | |  ____) | 
 /_/    \_\_| \_|_____|_____/|_|  |_|   |______/_/ \_\_|    |______\____/_____|  |_| |_____/  

                                                                   
"""
    credit = f"{Fore.RED}{Style.BRIGHT}➤ Mobile Number Lookup Tool | Credit: YASH X CHEATS\n"
    type_effect(ascii_banner, delay=0.0005)
    print(credit)

# === Print Colored ===
def print_colored(text, delay=0.005):
    colors = [Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.LIGHTBLUE_EX, Fore.LIGHTGREEN_EX]
    for line in text.splitlines():
        color = random.choice(colors)
        for char in line:
            print(color + char, end='', flush=True)
            time.sleep(delay)
        print()

# === Format as JS Object ===
def format_as_js(data):
    if isinstance(data, dict):
        js_lines = []
        for key, value in data.items():
            value_str = json.dumps(str(value), ensure_ascii=False) if not isinstance(value, (dict, list)) else json.dumps(value, ensure_ascii=False)
            js_lines.append(f"  {key}: {value_str}")
        return "{\n" + ",\n".join(js_lines) + "\n}"
    return str(data)

# === Normalize API Response ===
def normalize_response(data):
    """Handle different API response formats"""
    
    # Agar direct dict hai with data field
    if isinstance(data, dict):
        # Agar already fields hain
        if any(k in data for k in ['name', 'mobile', 'operator', 'circle', 'state', 'number']):
            return [data]
        # Agar 'data' key mein list hai
        if 'data' in data and data['data']:
            if isinstance(data['data'], list):
                return data['data']
            elif isinstance(data['data'], dict):
                return [data['data']]
        # Agar 'result' key mein hai
        if 'result' in data and data['result']:
            if isinstance(data['result'], list):
                return data['result']
            elif isinstance(data['result'], dict):
                return [data['result']]
    
    # Agar list hai directly
    if isinstance(data, list):
        return data
    
    # Agar string hai toh try to parse
    if isinstance(data, str):
        try:
            parsed = json.loads(data)
            return normalize_response(parsed)
        except:
            return [{"raw_response": data}]
    
    return []

# === Search Function ===
def search_number(number):
    url = f"{API_BASE}{number}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        raw_text = response.text.strip()
        
        print(f"{Fore.CYAN}[DEBUG] Raw Response: {raw_text[:200]}{Style.RESET_ALL}\n")
        
        # Try to parse JSON
        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError:
            # Agar pure text hai toh usko as is dikhao
            print(f"{Fore.YELLOW}⚠️ Response is not JSON. Showing raw text:{Style.RESET_ALL}")
            print_colored(raw_text)
            return
        
        records = normalize_response(data)
        
        if not records:
            print(f"{Fore.YELLOW}⚠️ No results found for {number}{Style.RESET_ALL}")
            return
        
        swipe_effect(Fore.CYAN + f"\n{'='*50}")
        swipe_effect(Fore.CYAN + f"📊 SEARCH RESULTS for +91-{number}")
        swipe_effect(Fore.CYAN + f"{'='*50}\n")
        
        for idx, record in enumerate(records, 1):
            if isinstance(record, dict) and record:
                title = f"─── [ RESULT {idx} ] ───"
                type_effect(Fore.LIGHTRED_EX + title)
                formatted = format_as_js(record)
                print_colored(formatted)
                print()
            elif record:
                print_colored(str(record))
        
        print(Fore.RED + f"\{'='*50}")
        print(Fore.RED + "⚡ Made by YASH X CHEATS")
        print(Fore.BLUE + "👉 Join: https://discord.gg/zh3SuFV7J")
        print(Fore.RED + f"{'='*50}\n")
        
    except requests.exceptions.Timeout:
        print(Fore.RED + "⚠️ Server Timeout. Try again later.")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"⚠️ Network error: {e}")
    except Exception as e:
        print(Fore.RED + f"⚠️ Error: {e}")

# === Main CLI ===
def main():
    show_banner()
    while True:
        try:
            type_effect(Fore.BLUE + "\n📞 Enter 10 Digit Mobile Number (or 'exit' to quit):")
            number = input(Fore.LIGHTGREEN_EX + "└─➤ ")
            
            if number.lower() == "exit":
                print(Fore.RED + "\n👋 Goodbye!")
                break
            
            if number.isdigit() and len(number) == 10:
                search_number(number)
            else:
                print(Fore.RED + "❌ Invalid! Please enter exactly 10 digits.")
                
        except KeyboardInterrupt:
            print(Fore.RED + "\n⛔ Exiting...")
            break

if __name__ == "__main__":
    main()