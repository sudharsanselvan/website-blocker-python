# Website Blocker

## Introduction
The Website Blocker is a Python-based utility that allows users to block access to specific websites during certain time periods. It achieves this by modifying the system's `hosts` file to redirect the specified websites to a loopback address (`127.0.0.1`). This can help improve productivity by restricting access to distracting websites like social media during work or study hours.

---

## How It Works
The program works by:
1. **Modifying the Hosts File**: 
   - The `hosts` file is a system configuration file that maps hostnames to IP addresses.
   - By adding entries that redirect specific websites to `127.0.0.1`, access to these websites is effectively blocked.

2. **Blocking Hours**:
   - Users can define specific hours during which the websites should remain blocked. Outside of these hours, the websites are unblocked automatically.

3. **Persistent Block List**:
   - The program saves the list of blocked websites in a JSON file (`blocked_websites.json`) so that it persists across sessions.

4. **Interactive Menu**:
   - The program provides a user-friendly menu to manage blocked websites, set blocking hours, and start/stop blocking.

---

## Features
- **View Blocked Websites**: Check the list of currently blocked websites.
- **Add Websites to Block**: Add new websites to the block list.
- **Set Blocking Hours**: Define specific hours during which websites should be blocked.
- **Start Blocking**: Begin blocking websites based on the configured hours.
- **Unblock All Websites**: Remove all websites from the block list and restore access.

---

## Requirements
- Python 3.x
- Administrator/superuser privileges:
  - On **Windows**, run the script as an administrator.
  - On **Linux/macOS**, use `sudo` to execute the script.

---

## How to Use
1. **Run the Script**:
   - **Windows**: Open Command Prompt as Administrator and run:
     ```bash
     python website_blocker.py
     ```
   - **Linux/macOS**: Open Terminal and run:
     ```bash
     sudo python3 website_blocker.py
     ```

2. **Interactive Menu**:
   After starting the script, you'll see the following menu options:

   ```
   Website Blocker
   1. View blocked websites
   2. Add a website to block
   3. Set blocking hours
   4. Start blocking
   5. Exit (Websites remain blocked)
   6. Unblock all websites and exit
   ```

3. **Menu Usage**:
   - **Option 1: View Blocked Websites**:
     Displays the list of websites currently blocked.

   - **Option 2: Add a Website to Block**:
     - Enter the full website address (e.g., `www.facebook.com`).
     - The program adds it to the block list.

   - **Option 3: Set Blocking Hours**:
     - Define the hours during which websites should be blocked (e.g., from 9 AM to 6 PM).
     - Enter the start and end hours in 24-hour format (0-23).

   - **Option 4: Start Blocking**:
     - Begin blocking websites during the configured hours.
     - Use `Ctrl+C` to stop blocking manually.

   - **Option 5: Exit (Websites Remain Blocked)**:
     - Exit the program, but the websites remain blocked.

   - **Option 6: Unblock All Websites and Exit**:
     - Remove all websites from the block list and restore access.

4. **Example Walkthrough**:
   - Add a website to block:
     ```
     Enter your choice (1/2/3/4/5/6): 2
     Enter the website to block (e.g., www.facebook.com): www.facebook.com
     www.facebook.com has been added to the block list.
     ```
   - Set blocking hours:
     ```
     Enter your choice (1/2/3/4/5/6): 3
     Enter blocking start hour (0-23): 9
     Enter blocking end hour (0-23): 18
     Blocking hours set from 9:00 to 18:00.
     ```
   - Start blocking:
     ```
     Enter your choice (1/2/3/4/5/6): 4
     Starting website blocking from 9:00 to 18:00...
     Websites are blocked. Next check in 60 seconds...
     ```
   - Unblock all websites and exit:
     ```
     Enter your choice (1/2/3/4/5/6): 6
     Unblocking all websites and exiting...
     ```

---

## Notes
1. **Permissions**:
   - The script requires write permissions to the `hosts` file. Make sure to run it with administrator/superuser privileges.

2. **Cross-Platform Compatibility**:
   - The script supports both Windows and Unix-like systems (Linux/macOS).

3. **Blocked Websites File**:
   - The list of blocked websites is saved in a file named `blocked_websites.json` in the same directory as the script. This ensures that the block list persists even after the script is closed.

4. **Stopping the Script**:
   - Use `Ctrl+C` to interrupt and stop the blocking process manually.

---

Enjoy improved focus and productivity with this Website Blocker! 😊
