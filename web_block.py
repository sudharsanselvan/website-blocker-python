import time
import os
import json

# Determine the hosts file path based on the operating system
if os.name == 'nt':  # Windows
    HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
else:  # macOS/Linux
    HOSTS_PATH = "/etc/hosts"

REDIRECT_IP = "127.0.0.1"
BLOCKED_WEBSITES_FILE = "blocked_websites.json"

# Load blocked websites from file (if exists)
def load_blocked_websites():
    if os.path.exists(BLOCKED_WEBSITES_FILE):
        with open(BLOCKED_WEBSITES_FILE, "r") as file:
            return json.load(file)
    return []


# Save blocked websites to file
def save_blocked_websites(websites):
    with open(BLOCKED_WEBSITES_FILE, "w") as file:
        json.dump(websites, file)


# Websites to block (loaded from file)
websites_to_block = load_blocked_websites()

# Block hours (default: 9 AM to 6 PM)
block_start_hour = 0
block_end_hour = 23


def check_permissions():
    """Ensure the script has permissions to modify the hosts file."""
    if not os.access(HOSTS_PATH, os.W_OK):
        print(f"Permission denied: Please run this script as an administrator/superuser.")
        exit()


def block_websites():
    """Block the websites by adding them to the hosts file."""
    with open(HOSTS_PATH, "r+") as file:
        content = file.read()
        for website in websites_to_block:
            if f"{REDIRECT_IP} {website}" not in content:
                file.write(f"{REDIRECT_IP} {website}\n")


def unblock_websites():
    """Unblock all websites by removing entries from the hosts file."""
    with open(HOSTS_PATH, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if not any(website in line for website in websites_to_block):
                file.write(line)
        file.truncate()


def interactive_menu():
    """Interactive menu for managing website blocker."""
    global block_start_hour, block_end_hour, websites_to_block

    while True:
        print("\nWebsite Blocker")
        print("1. View blocked websites")
        print("2. Add a website to block")
        print("3. Set blocking hours")
        print("4. Start blocking")
        print("5. Exit (Websites remain blocked)")
        print("6. Unblock all websites and exit")
        choice = input("Enter your choice (1/2/3/4/5/6): ").strip()

        if choice == "1":
            print("\nBlocked Websites:")
            for i, site in enumerate(websites_to_block, start=1):
                print(f"{i}. {site}")
            if not websites_to_block:
                print("No websites are currently in the block list.")

        elif choice == "2":
            new_site = input("Enter the website to block (e.g., www.facebook.com): ").strip()
            if new_site and new_site not in websites_to_block:
                websites_to_block.append(new_site)
                save_blocked_websites(websites_to_block)
                print(f"{new_site} has been added to the block list.")
            else:
                print("Invalid input or website already in the block list.")

        elif choice == "3":
            try:
                start = int(input("Enter blocking start hour (0-23): ").strip())
                end = int(input("Enter blocking end hour (0-23): ").strip())
                if 0 <= start < 24 and 0 <= end < 24:
                    block_start_hour, block_end_hour = start, end
                    print(f"Blocking hours set from {block_start_hour}:00 to {block_end_hour}:00.")
                else:
                    print("Invalid hours. Please enter values between 0 and 23.")
            except ValueError:
                print("Invalid input. Please enter numeric values.")

        elif choice == "4":
            print(f"\nStarting website blocking from {block_start_hour}:00 to {block_end_hour}:00...")
            try:
                while True:
                    current_time = time.localtime()
                    if block_start_hour <= current_time.tm_hour < block_end_hour:
                        block_websites()
                        print(f"Websites are blocked. Next check in 60 seconds...", end="\r")
                    else:
                        unblock_websites()
                        print(f"Websites are unblocked. Next check in 60 seconds...", end="\r")
                    time.sleep(60)
            except KeyboardInterrupt:
                print("\nBlocking stopped by user. Exiting...")
                break

        elif choice == "5":
            print("Exiting... Websites will remain blocked.")
            block_websites()
            break

        elif choice == "6":
            print("Unblocking all websites and exiting...")
            unblock_websites()
            websites_to_block.clear()
            save_blocked_websites([])  # Clear the saved list
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    check_permissions()
    interactive_menu()
