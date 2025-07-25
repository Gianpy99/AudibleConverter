#!/usr/bin/env python

# Usage examples:
# python audible-activator.py --username your_email@example.com --password your_password --l uk
# python audible-activator.py --username your_email@example.com --password your_password --l de

# Quick account selection (if accounts.py exists):
# python audible-activator.py --account gianpaolo
# python audible-activator.py --account adriana


import os
import sys
import time
import base64
import common
import hashlib
import binascii
import requests
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from optparse import OptionParser

# Try to import account configurations
try:
    from accounts import get_account, list_accounts
    ACCOUNTS_AVAILABLE = True
except ImportError:
    ACCOUNTS_AVAILABLE = False

PY3 = sys.version_info[0] == 3

if PY3:
    from urllib.parse import urlencode
    from urllib.parse import urlparse, parse_qsl
else:
    from urllib import urlencode
    from urlparse import urlparse, parse_qsl


def fetch_activation_bytes(username, password, options):
    base_url = 'https://www.audible.com/'
    base_url_license = 'https://www.audible.com/'
    lang = options.lang

    # Step 0
    opts = webdriver.ChromeOptions()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko")
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')

    # Step 1
    if '@' in username:  # Amazon login using email address
        login_url = "https://www.amazon.com/ap/signin?"
    else:  # Audible member login using username (untested!)
        login_url = "https://www.audible.com/sign-in/ref=ap_to_private?forcePrivateSignIn=true&rdPath=https%3A%2F%2Fwww.audible.com%2F%3F"
    if lang == "uk":
        login_url = login_url.replace('.com', ".co.uk")
        base_url = base_url.replace('.com', ".co.uk")
    elif lang == "jp":
        login_url = login_url.replace('.com', ".co.jp")
        base_url = base_url.replace('.com', ".co.jp")
    elif lang == "au":
        login_url = login_url.replace('.com', ".com.au")
        base_url = base_url.replace('.com', ".com.au")
    elif lang == "in":
        login_url = login_url.replace('.com', ".in")
        base_url = base_url.replace('.com', ".in")
    elif lang != "us":  # something more clever might be needed
        login_url = login_url.replace('.com', "." + lang)
        base_url = base_url.replace('.com', "." + lang)

    if PY3:
        player_id = base64.encodebytes(hashlib.sha1(b"").digest()).rstrip()  # keep this same to avoid hogging activation slots
        player_id = player_id.decode("ascii")
    else:
        player_id = base64.encodestring(hashlib.sha1(b"").digest()).rstrip()
    if options.player_id:
        player_id = base64.encodestring(binascii.unhexlify(options.player_id)).rstrip()
    print("[*] Player ID is %s" % player_id)

    payload = {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.mode': 'logout',
        'openid.assoc_handle': 'amzn_audible_' + lang,
        'openid.return_to': base_url + 'player-auth-token?playerType=software&playerId=%s=&bp_ua=y&playerModel=Desktop&playerManufacturer=Audible' % (player_id)
    }
    
    opts = webdriver.ChromeOptions()
    
    if options.firefox:
        driver = webdriver.Firefox()
    else:
        if sys.platform == 'win32':
            chromedriver_path = "chromedriver.exe"
        elif os.path.isfile("/usr/bin/chromedriver"):  # Debian/Ubuntu package's chromedriver path
            chromedriver_path = "/usr/bin/chromedriver"
        elif os.path.isfile("/usr/lib/chromium-browser/chromedriver"):  # Ubuntu package chromedriver path
            chromedriver_path = "/usr/lib/chromium-browser/chromedriver"
        elif os.path.isfile("/usr/local/bin/chromedriver"):  # macOS + Homebrew
            chromedriver_path = "/usr/local/bin/chromedriver"
        else:
            chromedriver_path = "./chromedriver"

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=opts)

    query_string = urlencode(payload)
    url = login_url + query_string
    driver.get(base_url + '?ipRedirectOverride=true')
    driver.get(url)
    if os.getenv("DEBUG") or options.debug:  # enable if you hit CAPTCHA or 2FA or other "security" screens
        print("[!] Running in DEBUG mode. You will need to login in a semi-automatic way, wait for the login screen to show up ;)")
        time.sleep(32)
    else:
        wait = WebDriverWait(driver, 20)

        # Step 1: Wait for email input and fill it
        email_field = wait.until(EC.presence_of_element_located((By.ID, "ap_email")))
        email_field.send_keys(username)

        # Step 2: Click 'Continue' button
        continue_button = driver.find_element(By.ID, "continue")
        continue_button.click()

        # Step 3: Wait for password field and fill it
        password_field = wait.until(EC.presence_of_element_located((By.ID, "ap_password")))
        password_field.send_keys(password)

        # Step 4: Submit login
        submit_button = driver.find_element(By.ID, "signInSubmit")
        submit_button.click()
        time.sleep(2)  # give the page some time to load

    # Apparently, automated logins get detected now. The user receives a
    # one-time password via email and is asked to type it into a textbox.
    # After login pause and give user a chance to enter one-time password
    # manually.
    msg = "\nATTENTION: Now you may have to enter a one-time password manually. Once you are done, press enter to continue..."
    if PY3:
        input(msg)
    else:
        raw_input(msg)

    # Step 2
    driver.get(base_url + 'player-auth-token?playerType=software&bp_ua=y&playerModel=Desktop&playerId=%s&playerManufacturer=Audible&serial=' % (player_id))
    current_url = driver.current_url
    o = urlparse(current_url)
    data = dict(parse_qsl(o.query))

    # Step 2.5, switch User-Agent to "Audible Download Manager"
    headers = {
        'User-Agent': "Audible Download Manager",
    }
    cookies = driver.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

    # Step 3, de-register first, in order to stop hogging all activation slots
    # (there are 8 of them!)
    durl = base_url_license + 'license/licenseForCustomerToken?' \
        + 'customer_token=' + data["playerToken"] + "&action=de-register"
    s.get(durl, headers=headers)

    # Step 4
    url = base_url_license + 'license/licenseForCustomerToken?' \
        + 'customer_token=' + data["playerToken"]
    response = s.get(url, headers=headers)

    with open("activation.blob", "wb") as f:
        f.write(response.content)
    activation_bytes, _ = common.extract_activation_bytes(response.content)
    print("activation_bytes: " + activation_bytes)

    # Step 5 (de-register again to stop filling activation slots)
    s.get(durl, headers=headers)

    # driver.get(url)
    time.sleep(8)
    driver.quit()


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]", version="%prog 0.2")
    parser.add_option("-d", "--debug",
                      action="store_true",
                      dest="debug",
                      default=False,
                      help="run program in debug mode, enable this for 2FA enabled accounts or for authentication debugging")
    parser.add_option("-f", "--firefox",
                      action="store_true",
                      dest="firefox",
                      default=False,
                      help="use this option to use firefox instead of chrome",)
    parser.add_option("-l", "--lang",
                      action="store",
                      dest="lang",
                      default="us",
                      help="us (default) / au / in / de / fr / jp / uk (untested)",)
    parser.add_option("-p",
                      action="store",
                      dest="player_id",
                      default=None,
                      help="Player ID in hex (for debugging, not for end users)",)
    parser.add_option("--username",
                      action="store",
                      dest="username",
                      default=False,
                      help="Audible username, use along with the --password option")
    parser.add_option("--password",
                      action="store",
                      dest="password",
                      default=False,
                      help="Audible password")
    parser.add_option("--account",
                      action="store",
                      dest="account",
                      default=None,
                      help="Use predefined account from accounts.py (e.g., gianpaolo, adriana)")
    (options, args) = parser.parse_args()

    # Handle account selection
    if options.account:
        if not ACCOUNTS_AVAILABLE:
            print("Error: accounts.py not found. Create this file with your account configurations.")
            sys.exit(1)
        
        account_config = get_account(options.account)
        if not account_config:
            print(f"Error: Account '{options.account}' not found.")
            if ACCOUNTS_AVAILABLE:
                print(f"Available accounts: {', '.join(list_accounts())}")
            sys.exit(1)
        
        username = account_config['username']
        password = account_config['password']
        if not options.lang or options.lang == "us":  # Use account's region if lang not specified
            options.lang = account_config.get('region', 'us')
        
        print(f"[*] Using account: {options.account} ({username}) - Region: {options.lang}")
    
    elif options.username and options.password:
        username = options.username
        password = options.password
    else:
        if PY3:
            username = input("Username: ")
        else:
            username = raw_input("Username: ")
        password = getpass("Password: ")

    fetch_activation_bytes(username, password, options)
