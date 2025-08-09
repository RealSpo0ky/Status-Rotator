import os
import time
import json
import requests
import ctypes
import webbrowser
from colorama import init, Fore, Back, Style

def loadConfig():
    try:
        configFile = open("Input/config.json", "r")
        configData = configFile.read()
        configFile.close()
        return json.loads(configData)
    except:
        print("[!] Error: Unable to load configuration. Please check 'Input/config.json'.")
        exit(1)
        
config = loadConfig()
TOKEN = config.get("TOKEN")
STATUS = config.get("STATUS", "dnd")
STATUS_TEXT = config.get("STATUS_TEXT", ["Leck", "Meine", "Eier"])
CHANGE_SPEED = config.get("CHANGE_SPEED", 0.2)

def setConsoleTitle(title):
    try:
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    except:
        pass

def openWebsite():
    try:
        webbrowser.open("https://guns.lol/realspo0ky")
    except:
        pass

def printGradientText(text):
    print(Fore.CYAN + text + Style.RESET_ALL)

def showInfo(message, infoType="info"):
    if infoType == "error":
        print(f"[!] {message}")
    elif infoType == "success":
        print(f"[+] {message}")
    else:
        print(f"{message}")

def askUserChoice():
    setConsoleTitle("Status Rotator | By Spo0ky.wtf | GitHub: RealSpo0ky")
    os.system('cls')
    printGradientText("[1] Start Status-Rotator")
    print()
    userInput = input(Fore.CYAN + "Choose » " + Style.RESET_ALL).strip().lower()
    if userInput == '1':
        os.system('cls')
        printGradientText("[+] Starting the status change process...")
        time.sleep(1)
        os.system('cls')
        return "start"
    else:
        showInfo("Invalid choice. Please select a valid option.", "error")
        return "invalid"

def mainFunction():
    while True:
        userChoice = askUserChoice()
        if userChoice == "start":
            statusIndex = 0
            while True:
                headers = {'Authorization': TOKEN}
                currentStatusText = STATUS_TEXT[statusIndex]
                requestData = {"status": STATUS, "custom_status": {"text": currentStatusText}}
                
                try:
                    response = requests.patch("https://discord.com/api/v8/users/@me/settings", headers=headers, json=requestData)
                    if response.status_code == 200:
                        showInfo(f"Status Successfully Changed: \"{currentStatusText}\"", "success")
                    elif response.status_code == 429:
                        rateLimitInfo = response.json()
                        retryAfter = rateLimitInfo.get('retry_after', 1)
                        showInfo(f"Ratelimited. Retrying in {retryAfter} seconds.", "error")
                        time.sleep(int(retryAfter))
                    else:
                        showInfo(f"Failed to change status -> {response.status_code}", "error")
                    statusIndex = (statusIndex + 1) % len(STATUS_TEXT)
                except requests.exceptions.RequestException as networkError:
                    showInfo(f"Network error: {networkError}", "error")
                time.sleep(CHANGE_SPEED)
        elif userChoice in ["menu", "invalid"]:
            continue
        else:
            break
        
if __name__ == "__main__":
    init(autoreset=True)
    setConsoleTitle("Status Rotator | By Spo0ky.wtf | GitHub: RealSpo0ky")
    openWebsite()
    mainFunction()
