import re
import time
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def sign_in(username):
    # WebDriver setup
    driver = webdriver.Chrome()  # Provide the path to the ChromeDriver executable
    driver.implicitly_wait(10)  # Adjust the waiting time as per your requirements

    # Register user
    driver.get('https://www.noip.com/sign-up')  # Open the registration page
    time.sleep(2)  # Wait for page to load

    # Fill in the registration form
    user = driver.find_element(By.ID, "email")
    user.send_keys(username)
    password = driver.find_element(By.ID, "inputPassword")
    password.send_keys("password123213")
    driver.find_element(By.ID, "free-signup").click()
    time.sleep(2)  # Wait for registration to complete

    # Close the WebDriver
    driver.quit()


def create_subdomain(email_input, password_input):
    # Set up Chrome WebDriver
    driver = webdriver.Chrome()

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

    hostname_input.send_keys("myhostdfgdfgdgtrt")
    ipv4_address_input.send_keys("34.145.60.74")
  
    webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()



def generate_temporary_email():
    response = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox')
    if response.status_code == 200:
        return response.text.strip('[]"')
    return None


def get_activation_email(email):
    url = f'https://www.1secmail.com/api/v1/?action=getMessages&login={temporary_email.split("@")[0]}&domain={temporary_email.split("@")[1]}'
    start_time = time.time()
    while time.time() - start_time < 60:
        response = requests.get(url)
        data = response.json()

        if data:
            # Check if the response is not an empty list
            if len(data) > 0:
                email_id = data[-1]['id']
                break

        print("[*] Still there is no response yet. Waiting for", 5, "seconds...")
        time.sleep(5)

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
    while True:
        user_password = input("[*] Insert password (at least 6 characters): \n")
        if len(user_password) < 6:
            print("Password must be at least 6 characters long. Please try again.")
        else:
            break
    # Generate a temporary email
    temporary_email = generate_temporary_email()
    if temporary_email:
        print(f'Temporary email: {temporary_email}')

        # Register user on No-IP using the temporary email
        sign_in(temporary_email)

        # Get the activation email
        session = get_activation_email(temporary_email)
        create_subdomain(temporary_email, user_password)
    else:
        print('Failed to generate a temporary email.')
