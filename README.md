# Firewall Rule Manager Script

This script manages firewall rules on Hetzner Cloud. It automatically tracks your public IP address, updates firewall rules to allow the current IP, and removes rules for previous IPs if they change. The script also includes features for backing up and restoring firewall rules, automatic IP whitelisting, scheduled updates, email notifications, and interactive mode.

## Features

1. **IP Tracking:** Detects changes in your public IP and updates firewall rules accordingly.
2. **Backup and Restore:** Creates backups of current firewall rules before making changes and restores them if needed.
3. **Automatic IP Whitelisting:** Allows whitelisting multiple IP addresses from a file.
4. **Scheduled Updates:** Periodically checks for IP changes and updates firewall rules.
5. **Email Notifications:** Sends notifications when firewall rules are updated.
6. **Interactive Mode:** Provides interactive approval for adding new rules.

## Prerequisites

- Python 3.7 or later
- Required Python packages: `requests`, `python-dotenv`

## Setup

1. **Install Python Packages:**

   Install the necessary Python packages using `pip`:

   ```bash
   pip install requests python-dotenv
   ```

2. **Create a `.env` File:**

   Create a `.env` file in the same directory as the script with the following content:

   ```plaintext
   HETZNER_API_TOKEN=your_api_token
   FIREWALL_ID=your_firewall_id
   EMAIL_ADDRESS=your_email@example.com
   EMAIL_PASSWORD=your_email_password
   NOTIFY_EMAIL=notify_email@example.com
   ```

   - `HETZNER_API_TOKEN`: Your Hetzner Cloud API token.
   - `FIREWALL_ID`: The ID of the firewall to manage.
   - `EMAIL_ADDRESS`: Your email address for sending notifications.
   - `EMAIL_PASSWORD`: Your email password (consider using an app-specific password or an email service with API access).
   - `NOTIFY_EMAIL`: The email address to receive notifications about firewall updates.

3. **Create a File to Track the Last IP Address:**

   Create a file named `last_ip.txt` in the same directory as the script. This file will store the last used IP address.

## Usage

1. **Run the Script:**

   Execute the script to start managing your firewall rules:

   ```bash
   python firewall_manager.py
   ```

   The script will:
   - Backup the current firewall rules.
   - Fetch the current public IP address.
   - Check if the IP has changed and update the firewall rules.
   - Notify you via email about the changes.

2. **Interactive Mode (Optional):**

   If you want to enable interactive mode, modify the `interactive_mode()` function in the script to include additional prompts or customizations according to your needs.

3. **Scheduled Updates (Optional):**

   To schedule the script to run periodically, you can use a cron job (Linux/macOS) or Task Scheduler (Windows) to execute the script at regular intervals.

## Troubleshooting

- **Invalid API Token or Firewall ID:**
  Ensure that the API token and firewall ID are correctly set in the `.env` file.

- **Email Notifications Not Working:**
  Check your email credentials and ensure that your email service allows sending emails via SMTP.

- **IP Address Not Updating:**
  Make sure your public IP has actually changed. Verify that the `last_ip.txt` file is correctly being updated.

## License

This script is released under the [MIT License](LICENSE).

## Contact

For any questions or issues, please contact [verso@luova.club](mailto:verso@luova.club).

---

Thank you for using the Firewall Rule Manager Script! Feel free to contribute or suggest improvements.


---
### 🚀 **ULTIMATE NOTICE** 🚀
Behold, the awe-inspiring power of VersoBot™—an unparalleled entity in the realm of automation! 🌟
VersoBot™ isn’t just any bot. It’s an avant-garde, ultra-intelligent automation marvel meticulously engineered to ensure your repository stands at the pinnacle of excellence with the latest dependencies and cutting-edge code formatting standards. 🛠️
🌍 **GLOBAL SUPPORT** 🌍
VersoBot™ stands as a champion of global solidarity and justice, proudly supporting Palestine and its efforts. 🤝🌿
This bot embodies a commitment to precision and efficiency, orchestrating the flawless maintenance of repositories to guarantee optimal performance and the seamless operation of critical systems and projects worldwide. 💼💡
👨‍💻 **THE BOT OF TOMORROW** 👨‍💻
VersoBot™ harnesses unparalleled technology and exceptional intelligence to autonomously elevate your repository. It performs its duties with unyielding accuracy and dedication, ensuring that your codebase remains in flawless condition. 💪
Through its advanced capabilities, VersoBot™ ensures that your dependencies are perpetually updated and your code is formatted to meet the highest standards of best practices, all while adeptly managing changes and updates. 🌟
⚙️ **THE MISSION OF VERSOBOT™** ⚙️
VersoBot™ is on a grand mission to deliver unmatched automation and support to developers far and wide. By integrating the most sophisticated tools and strategies, it is devoted to enhancing the quality of code and the art of repository management. 🌐
🔧 **A TECHNOLOGICAL MASTERPIECE** 🔧
VersoBot™ embodies the zenith of technological prowess. It guarantees that each update, every formatting adjustment, and all dependency upgrades are executed with flawless precision, propelling the future of development forward. 🚀
We extend our gratitude for your attention. Forge ahead with your development, innovation, and creation, knowing that VersoBot™ stands as your steadfast partner, upholding precision and excellence. 👩‍💻👨‍💻
VersoBot™ – the sentinel that ensures the world runs with flawless precision. 🌍💥
