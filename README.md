# PynAuth

PynAuth is a python-based proof of concept framework for performing OAuth token stealing campaigns against Office365 accounts with the Microsoft Graph API. The tool is built on top of the Microsoft Quick Start Python [code](https://developer.microsoft.com/en-us/graph/get-started/python).

"PynAuth" is a play on the naming of FireEye's ["PwnAuth"](https://github.com/fireeye/PwnAuth), which is a web application framework for launching the same types of campaigns. 

I developed this framework as I wanted a quick-start, python-based, modular way to perform these attacks with little over-head. I am also old-school and like terminal based tools. This project is very much in beta and I am sure there are bugs or more efficient ways to code the functionality. (Still working on those python skills :D).

Do not use this tool for unauthorized malicious purposes.

# Acknowledgments

For other great resources on this type of attack and tools, be sure to check out the following research from FireEye and MDSec which sparked this:

+ [FireEye's PwnAuth](https://www.fireeye.com/blog/threat-research/2018/05/shining-a-light-on-oauth-abuse-with-pwnauth.html)

+ [MDSec's Office 365 Attack Toolkit](https://www.mdsec.co.uk/2019/07/introducing-the-office-365-attack-toolkit/)

# Setup

1. Create an application within the [Azure Portal.](https://portal.azure.com)
2. Add the following attributes from your app to the '*app_config.py*' file:

+ Client ID
+ Client Secret
+ Redirect Path
+ Scope (Permissions)

3. Modify the '*login.html*' and '*index.html*' page within the '*templates*' folder to your liking. Currently, they are basically just the Microsoft Quick Start defaults

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

(Blog coming soon which will go more in depth on this setup)

# Usage

1. Start webserver by running '*app.py*'. This will start a Flask based web server. 
(Securing the server is up to you. Recommend putting behind a HTTPS redirector if open to the internet)

2. Have a user open the configured link to sign-in to the portal
3. An access and refresh token will be returned and written to a pickle file. Currently, only one set of tokens can be stored per user.
4. Once tokens have been collected, run '*mainAPI.py*' and choose the action you wish to take

# Current Modules

### 1. Get User/Check Token
This module will pull user's information from the Graph API. Good way to check if token is still valid.

### 2. Send Email
This module can send a new or templated email. The template email can be edited within the '*apiSendMail.py*' module. Attachments are not currently supported. 

### 3. Query Mail
Due to the built-in permissions of the Graph API, this module will only work for work and school accounts (not personal Microsoft accounts). This module will query the users inbox for a specified keyword and return up to 25 results (can be modified). For each result, it can display the received time, sender, receiver, attachment list, and body text to the terminal. If the email has attachments, they can be downloaded. 

### 4. Access OneDrive
This module works as an interactive terminal to the user's OneDrive. To traverse to a folder or download a file, simply choose the corresponding number. 

### 5. Create Inbox Rules
This module will create a mail rule for the user's Outlook inbox. The rule can be modified within the '*apiCreateInboxRule.py*' module. Current config looks for "password" and "reset" in an email. Please see the official Microsoft [documentation](https://docs.microsoft.com/en-us/graph/api/mailfolder-post-messagerules?view=graph-rest-1.0&tabs=http) on how to create these rules.

### 6. List/Delete Inbox Rules
This module will list any current inbox rules for the user. If any exist, it will give you the option to delete them. This is a good way to remove your created rule in the previous module after it is no longer needed. (I need to work on making the output prettier).

### 7. Refresh Token
By default, the user's access token is only valid for one hour. This module uses the refresh token provided by OAuth to refresh the access token for another hour. The refresh token is valid for 14 days.

# Todo
1. Make some outputs prettier
2. Add additional error handing as necessary
3. Make code more efficient
4. Change user-agent. Currently in Azure logs, shows as "Python-urllib"
5. Add more modules

Constructive feedback always welcome.
