import os
import requests
import logging
import json
import smtplib
from email.mime.text import MIMEText

# Function to load environment variables from a .env file
def load_env_vars(filepath):
    """Load environment variables from a .env file."""
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"The .env file {filepath} does not exist.")
    
    with open(filepath) as file:
        for line in file:
            # Strip comments and blank lines
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Split on '=' and strip extra spaces
            key, value = map(str.strip, line.split('=', 1))
            os.environ[key] = value

# Load environment variables from .env file
load_env_vars('.env')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_my_ipv4():
    """
    Fetches the public IPv4 address of the current machine.
    
    Returns:
        str: The public IPv4 address.
    """
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        ip_address = response.json().get("ip")
        logging.info(f"Yay! Successfully retrieved your public IP address: {ip_address}.")
        return ip_address
    except requests.RequestException as e:
        logging.error(f"Oops! Something went wrong while fetching your IP address: {e}. Let's try again later!")
        exit(1)

def get_current_firewall_rules(firewall_id, headers):
    """
    Retrieves the current firewall rules from Hetzner Cloud.
    
    Args:
        firewall_id (str): The ID of the firewall to retrieve rules for.
        headers (dict): The headers containing the authorization token.
    
    Returns:
        list: A list of current firewall rules.
    """
    try:
        response = requests.get(f"https://api.hetzner.cloud/v1/firewalls/{firewall_id}", headers=headers)
        response.raise_for_status()
        rules = response.json().get('firewall', {}).get('rules', [])
        logging.info(f"Good news! Retrieved {len(rules)} firewall rules to work with.")
        return rules
    except requests.RequestException as e:
        logging.error(f"Uh-oh! Failed to fetch firewall rules: {e}. No worries, we'll get it sorted!")
        exit(1)

def update_firewall_rules(firewall_id, headers, rules):
    """
    Updates the firewall rules on Hetzner Cloud.
    
    Args:
        firewall_id (str): The ID of the firewall to update.
        headers (dict): The headers containing the authorization token.
        rules (list): The list of updated firewall rules.
    
    Returns:
        bool: True if the update was successful, False otherwise.
    """
    api_url = f"https://api.hetzner.cloud/v1/firewalls/{firewall_id}/actions/set_rules"
    data = {"rules": rules}
    
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        logging.info("Hooray! The firewall rules have been successfully updated. Your connection is safe and sound!")
        return True
    except requests.RequestException as e:
        logging.error(f"Oh no! Something went wrong while updating the firewall: {e}. Don't worry, we're in this together!")
        return False

def send_email_notification(subject, body, to_email):
    """
    Sends an email notification with a subject and body.
    
    Args:
        subject (str): The subject of the email.
        body (str): The body content of the email.
        to_email (str): The recipient's email address.
    """
    from_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.your-email-provider.com", 465) as server:
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        logging.info(f"Notification email sent to {to_email}.")
    except Exception as e:
        logging.error(f"Failed to send email notification: {e}.")

def interactive_mode(current_rules, new_rule):
    """
    Allows the user to interactively approve each step before proceeding.
    
    Args:
        current_rules (list): The current firewall rules.
        new_rule (dict): The new rule to be added.
    
    Returns:
        bool: True if the user approves the rule addition, False otherwise.
    """
    print("Current firewall rules:")
    for rule in current_rules:
        print(rule)
    print("New rule to be added:")
    print(new_rule)
    confirm = input("Do you want to proceed with adding this rule? (yes/no): ")
    return confirm.lower() == 'yes'

def track_ip_file():
    """
    Retrieves the file where the last used IP address is stored.
    
    Returns:
        str: The path to the file containing the last used IP address.
    """
    return "last_ip.txt"

def get_last_ip():
    """
    Retrieves the last used IP address from a file.
    
    Returns:
        str: The last used IP address, or None if the file does not exist.
    """
    if os.path.exists(track_ip_file()):
        with open(track_ip_file(), 'r') as f:
            return f.read().strip()
    return None

def set_last_ip(ip_address):
    """
    Sets the current IP address as the last used IP address in a file.
    
    Args:
        ip_address (str): The IP address to be stored.
    """
    with open(track_ip_file(), 'w') as f:
        f.write(ip_address)

def remove_ip_rule(rules, ip_to_remove):
    """
    Removes a rule that allows a specific IP address from the firewall rules.
    
    Args:
        rules (list): The current firewall rules.
        ip_to_remove (str): The IP address to be removed from the rules.
    
    Returns:
        list: The updated list of firewall rules.
    """
    updated_rules = [rule for rule in rules if ip_to_remove not in rule.get('source_ips', [])]
    return updated_rules

def main():
    # Load API token and firewall ID from environment variables
    api_token = os.getenv("HETZNER_API_TOKEN")
    firewall_id = os.getenv("FIREWALL_ID")
    
    if not api_token or not firewall_id:
        logging.critical("Uh-oh! We couldn't find your API token or firewall ID. Please set them as environment variables so we can get started.")
        exit(1)
    
    # Define headers for Hetzner API requests
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # Get the current public IP and convert it to CIDR notation
    my_ip_address = get_my_ipv4()
    cidr_ip = f"{my_ip_address}/32"
    
    # Fetch current firewall rules
    current_rules = get_current_firewall_rules(firewall_id, headers)
    
    # Retrieve the last used IP address
    last_ip_address = get_last_ip()
    
    if last_ip_address and last_ip_address != my_ip_address:
        # Remove old IP rule
        current_rules = remove_ip_rule(current_rules, f"{last_ip_address}/32")
        logging.info(f"Old IP address ({last_ip_address}) removed from firewall rules.")
    
    # Add the new rule to allow the current IP
    new_rule = {
        "direction": "in",
        "source_ips": [cidr_ip],
        "port": "any",
        "protocol": "tcp"
    }
    current_rules.append(new_rule)
    
    # Update the firewall with the new set of rules
    if update_firewall_rules(firewall_id, headers, current_rules):
        logging.info(f"Awesome! Your IP address ({my_ip_address}) has been successfully added to the allowed list on firewall {firewall_id}.")
        # Update the stored IP address
        set_last_ip(my_ip_address)
        # Send email notification
        send_email_notification(
            "Firewall Rules Updated",
            f"Your IP address has been updated to {my_ip_address}.",
            os.getenv("NOTIFY_EMAIL")
        )
    else:
        logging.error(f"Something didn't go as planned. Let's revisit the steps and try updating the firewall rules again.")
        restore_firewall_rules(firewall_id, headers)

if __name__ == "__main__":
    logging.info("Hello, wonderful human! Let's get started with updating your firewall rules.")
    main()
    logging.info("Thanks for using this script! You're doing great, and your firewall is all set. Take care!")
