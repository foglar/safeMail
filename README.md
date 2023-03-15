# safeMail

## Quick startguide

:warning: **WARNING** This app is not safe to use if you need security, because it uses student version of RSA encryption, which is not safe to use in real life. It is only for educational purposes, and it is not recommended to use it for real secret communications.

### Installation

1. Download the latest version of safeMail from [here][releases] and unzip it.
2. Download all required libraries with ```pip3 install -r requirements.txt``` (ezgmail, pyperclip, pyinputplus, rich)
3. Create your own public and private keys by running ```python3 makePublicPrivateKeys.py``` save them in the project folder and name them **my_pubkey.txt** and **my_privkey.txt** (:warning:DON'T SHARE private key with anyone) and send your public key to your friends.
4. You have to create your email adress at [gmail](https://www.gmail.com) Then go on [this](https://developers.google.com/gmail/api/quickstart/python) pick option **Enable Gmail API** and fill form. After that you should be able to download file **credentials.json** and upload it to the project folder. It contents your gmail authentication key and code, they act like your gmail password, so be carefull with them.
5. Then you can run ```python3 safeMail.py```, first time the window will pop up and askes you for login to your gmail. This app is not verified by Google, so it will try to stop from using it. Just click **advanced settings** and **continue (unsafe)**. (Consider creating new inbox and some new password only for this project)
6. Now you can read your emails with pressing enter or **v**, terminal will look like this:

   ```bash
      $ python safeMail.py
                  __    ___  ___      _ _ 
                 / _|   |  \/  |     (_) |
       ___  __ _| |_ ___| .  . | __ _ _| |
      / __|/ _` |  _/ _ \ |\/| |/ _` | | |
      \__ \ (_| | ||  __/ |  | | (_| | | |
      |___/\__,_|_| \___\_|  |_/\__,_|_|_|, by foglar

      To view your emails, press ENTER > 

   ```

7. For more commands type **help** or **h**.

### Functions

- **q** or **quit** - quits the program
- **help** or **h** - shows help

- **ENTER** or **v** or **view** - shows emails
- **r** - read one email, after pressing enter you will be asked for email number
- **s** or **send** - send email, after pressing enter you will be asked for email adress and message
- **nk** or **newkey** - create new public and private keys

## How it works

### Cipher

- safeMail uses ezgmail library from Al Sweigart to read and send emails and it is builded on the code of his book **Automate the boring stuff with Python**. It is using public key cipher and RSA encryption from his book **Cracking Codes with Python**.
- How keys work:
  1. You create your own public and private keys with **makePublicPrivateKeys.py** or **nk** command in safeMail.
  2. You send your public key to your friends or contacts.
  3. When they want to send you email, safeMail encrypt it with your public key and then send it to you.
  4. When you want to read your email, safeMail decrypt it with your private key, so you can read it.
  5. So no one can read your emails, because they are encrypted with your public key and only you can decrypt them with your private key, you can share your public key with anyone, but keep your private key safe.

:warning: **WARNING** This app is not safe to use if you need security, because it uses student version of RSA encryption, which is not safe to use in real life. It is only for educational purposes, and it is not recommended to use it for real secret communications.

### Folders and files

- **safeMail** - main folder <br/>
  |- **backup** - folder for backuping your public and private keys if you accidentaly delete them<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|- **my_privkey_backup_????-??-??-??:??:??.txt** - your public key with time when you delete him<br/>
  |- **cache** - folder for caching your encrypted emails (we save only encrypted emails, so no one can read them anyway, and delete them after you exit the program)<br/>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|- **emailSend.txt** - your last sended encrypted email (files are deleted after you leave<br/>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|- **cache?.txt** - your last 10 encrypted emails from inbox (files are deleted after you leave)<br/>
  |- **keys** - folder for storing your public keys of your contacts<br/>
  |- **safeMail.py** - main file running the program<br/>
  |- **makePublicPrivateKeys.py** - file for creating public and private keys<br/>
  |- **my_pubkey.txt** - your public key<br/>
  |- **my_privkey.txt** - your private key<br/>
  |- **credentials.json** - your gmail authentication key and code<br/>
  |- **requirements.txt** - required libraries<br/>
  |- **README.md** - this file<br/>

[releases]: https://www.github.com/foglar/safeMail/releases
