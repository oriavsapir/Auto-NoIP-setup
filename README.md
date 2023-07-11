# AutoNoIP
AutoNoIP is a FREE Python script that automates the process of creating a user in No-IP, activating it, and creating a DNS record using a FREE No-IP subdomain. It utilizes a fake email for any purpose.

## WHY?!

Many times, we need a subdomain for testing purposes, temporary apps that require SSL/TLS connections, or when we don't want to buy a new domain. 
This script can integrate with your code and fulfill your subdomain needs.

This script simplifies the setup of creating subdomains without any cost! No-IP allows you to create a free account and provides you with one free subdomain.

### Flow
User input:
- Password (This is relevant for managing the account and should be at least 6 characters long.)
- Domain name that the user desires, and the IP.

The script performs the following steps:
1. Creates a fake email.
2. Signs up for No-IP using the fake email.
3. Activates the No-IP account using the received email.
4. Register a new domain name.

## Requirements

- Python 3.x
- Requests library: Install it by running `pip install requests`
- Selenium library: Install it by running `pip install selenium`

## Usage

1. Clone the repository: `git clone https://github.com/oriavsapir/Auto-NoIP-setup.git`
2. Install the required dependencies.
3. Run the program: ```python autonoip.py``` and nsert the input one by one.
   or you can input with args:    
   example:  
   ```
   python autonoip.py --password mypassword123 --IP 192.168.0.1 --subdomain example
   ```
<pre>
python test1.py --help                                                           
usage: test1.py [-h] [-p PASSWORD] [--IP IP] [-sb SUBDOMAIN] [--show-browser]  
  
options:  
  -h, --help                            | show this help message and exit  
  -p PASSWORD, --password PASSWORD      | password for No-IP account (at least 6 characters)  
  --IP IP                               | IP address.
  -sb SUBDOMAIN, --subdomain SUBDOMAIN  | subdomain name for your new domain  (up to 19 characters)    
  --show-browser                        | show browser    
</pre>

## P.O.C
<pre>
   python .\autonoip.py --password mypas.... --IP 192.168.0.1 --subdomain nice-name       
Temporary email: 7olmvr81...@kz..v.com
[*] Strating to active you mail account...
[*] Your account is active.
[*] The task has been completed successfully.
[*] Your domain name is: nice-name.ddns.net
[*] You can log in here and access your account at this link: https://www.noip.com/login, using your credentials.

</pre>
![image](https://github.com/oriavsapir/Auto-NoIP-setup/assets/85383966/00c5f811-2a77-4475-a9a0-0d25da81b5bc)

### note:
Every 30 days, you need to log in to this account and "Confirm" your domain name. Otherwise, the domain will be deactivated.  
So keep your Creds.
# Disclaimer:

This tool is provided "as is" without any warranty. I do not assume any responsibility or liability for the usage of this tool or any consequences resulting from its use. It is your sole responsibility to ensure that your use of this tool complies with the terms and conditions of the website you are automating.

Please note that automated actions, including repetitive requests and accessing a website multiple times from the same IP address, can potentially violate the terms of service of the website and may lead to temporary or permanent blocks. It is important to use automation tools responsibly and in accordance with the guidelines provided by the website.

Always ensure that you are aware of the website's policies and terms of service before using automation tools. Use delays between actions, consider rotating IP addresses or proxies, and monitor your usage to avoid any adverse consequences. Respect the website's terms and conditions and adhere to ethical guidelines when using automation.

Please use this tool responsibly and at your own risk.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
