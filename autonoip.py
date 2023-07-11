import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import argparse

def sign_in(username, password, show_browser):
    if show_browser:
        # Set up Chrome WebDriver
        driver = webdriver.Chrome()
    else:
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--headless")  # Hide the browser window
        driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(10)  # Adjust the waiting time as per your requirements

    # Register user
    driver.get('https://www.noip.com/sign-up')  # Open the registration page
    time.sleep(2)  # Wait for page to load

    # Fill in the registration form
    user = driver.find_element(By.ID, "email")
    user.send_keys(username)
    password_input = driver.find_element(By.ID, "inputPassword")
    password_input.send_keys(password)
    driver.find_element(By.ID, "free-signup").click()
    time.sleep(2)  # Wait for registration to complete

    # Close the WebDriver
    driver.quit()


def create_subdomain(email_input, password_input, hostname, ip_address ,show_browser):
    if show_browser:
        # Set up Chrome WebDriver
        driver = webdriver.Chrome()
    else:
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--headless")  # Hide the browser window
        driver = webdriver.Chrome(options=options)

    # Login to No-IP
    driver.get("https://www.noip.com/login?ref_url=console")
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")

    # Enter your login credentials
    username.send_keys(email_input)
    password.send_keys(password_input)

    # Click on the login button
    driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]").click()
    time.sleep(3)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    # Wait for the dynamic DNS page to load
    driver.get("https://my.noip.com/dynamic-dns")

    button = driver.find_element(By.XPATH, "//button[contains(text(), 'Create Hostname')]")
    # Click on the button
    button.click()
    time.sleep(1)
    # Fill in the form fields
    hostname_input = driver.find_element(By.ID, "name")
    ipv4_address_input = driver.find_element(By.NAME, "target")

    hostname_input.send_keys(hostname)
    ipv4_address_input.send_keys(ip_address)
    # TODO: fix choose domain.
    # wait = WebDriverWait(driver, 10)
    # dropdown = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "chosen-single")))
    # dropdown.click()
    # webdriver.ActionChains(driver).send_keys("ddnsking.com").perform()
    # time.sleep(1)
    webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
    print("[*] The task has been completed successfully.")
    print(f"[*] Your domain name is: {hostname}.ddns.net")

    print("[*] You can log in here and access your account at this link: https://www.noip.com/login, using your credentials.")


def generate_temporary_email():
    response = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox')
    if response.status_code == 200:
        return response.text.strip('[]"')
    return None


def get_activation_email(email):
    print("[*] Strating to active you mail account...")
    url = f'https://www.1secmail.com/api/v1/?action=getMessages&login={email.split("@")[0]}&domain={email.split("@")[1]}'
    start_time = time.time()
    while time.time() - start_time < 60:
        response = requests.get(url)
        data = response.json()

        if data:
            # Check if the response is not an empty list
            if len(data) > 0:
                email_id = data[-1]['id']
                break

        print("[*] Still there is no response yet. Waiting for", 3, "seconds...")
        time.sleep(3)

    if not data:
        print("No response received within the specified timeout.")
        exit(1)

    email_url = f'https://www.1secmail.com/api/v1/?action=readMessage&login={email.split("@")[0]}&domain={email.split("@")[1]}&id={email_id}'
    response = requests.get(email_url)
    messages = response.json()
    link_matches = re.findall(r'<a\s+href="(.*?)"', messages['body'], re.IGNORECASE)

    if len(link_matches) >= 2:
        check_activation = requests.get(link_matches[1]).text
        if "Your account is now active!" in check_activation:
            print("[*] Your account is active.")
    else:
        print("No second link found in the email body.")
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--password", help="password (at least 6 characters)")
    parser.add_argument("--IP", help="IP address")
    parser.add_argument("-sb","--subdomain", help="subdomain name (up to 19 characters). "
                                                  "This should be globally unique. If it is not unique, you'll need to choose another domain name.")
    parser.add_argument("--show-browser", action="store_true", help="show browser")

    args = parser.parse_args()

    # Validate the password
    if not args.password:
        args.password = input("[*] Insert password (at least 6 characters): \n")
        while len(args.password) < 6:
            print("Password must be at least 6 characters long. Please try again.")
            args.password = input("[*] Insert password (at least 6 characters): \n")

    # Validate the IP address
    ipv4_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if not args.IP or not re.match(ipv4_pattern, args.IP):
        args.IP = input("[*] Insert IP address: \n")
        while not re.match(ipv4_pattern, args.IP):
            print("Please enter a valid IPv4 address.")
            args.IP = input("[*] Insert IP address: \n")

    # Validate the subdomain name
    if not args.subdomain or not 3 < len(args.subdomain) < 19:
        args.subdomain = input("[*] Insert subdomain name: \n")
        while len(args.subdomain) < 3:
            print("Subdomain name must be at least 3 characters long. Please try again.")
            args.subdomain = input("[*] Insert subdomain name: \n")

    # Generate a temporary email
    temporary_email = generate_temporary_email()
    if temporary_email:
        print(f'Temporary email: {temporary_email}')

        # Register user on No-IP using the temporary email
        sign_in(temporary_email, args.password, args.show_browser)

        # Get the activation email
        get_activation_email(temporary_email)
        create_subdomain(temporary_email, args.password, args.subdomain, args.IP, args.show_browser)
    else:
        print('Failed to generate a temporary email.')
