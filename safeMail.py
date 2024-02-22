#! python3
# safeMail.py - Read and send encrypted emails

# TODO: Add option of names with emails

from rich.console import Console
from datetime import datetime as d
from pathlib import Path
import pyinputplus as pyip
import os
import sys
import shutil
import ezgmail
import publicKeyCipher
import makePublicPrivateKeys

console = Console()

try:
    ezgmail.init()
except Exception:
    console.print(
        "Gmail login failed, please check your credentials in credentials.json",
        style="bold red",
    )
    console.print(Exception, style="red")
    console.print(
        "More information about program on https://www.github.com/foglar/safeMail/",
        style="bold blue",
    )
    sys.exit()

encryptedMessages = []


def main():
    logo()
    while True:
        try:
            read_or_send = console.input(
                "To view your emails, press [bold red]ENTER[/bold red] > "
            )
        except KeyboardInterrupt:
            os.system("/bin/clear")
            console.print("\nBye!", style="bold red")
            console.print(
                "More information about program on https://www.github.com/foglar/safeMail/",
                style="bold blue",
            )
            sys.exit()
        print("")
        # View emails
        if (
            read_or_send == ""
            or read_or_send.lower().startswith("v")
            or read_or_send.lower().startswith("view")
        ):
            senders, emails, timestamps = readEmails()
            os.system("clear")
            for i in range(len(emails)):
                preview = emails[i][:50].replace("\n", " ")
                console.print(
                    f"Email from : [bold red] {senders[i]} [/bold red]\tTime: [bold red] {timestamps[i]} [/bold red]\tIndex: {i+1}"
                )
                console.print(f"Message    : [bold cyan] {preview}... [/bold cyan]")
                console.print("")
        # Read email
        elif read_or_send.lower().startswith("r") or read_or_send.lower().startswith(
            "read"
        ):
            emailSender, emailBody, emailTime = readEmail()
            os.system("clear")
            console.print(
                f"Email from : [bold red] {emailSender} [/bold red]\tTime: [bold red] {emailTime} [/bold red]"
            )
            console.print(f"Message    : [bold cyan] {emailBody} [/bold cyan]")
            console.print("")
        # Send email
        elif read_or_send.lower().startswith("s") or read_or_send.lower().startswith(
            "send"
        ):
            os.system("clear")
            sendEmails()
        # Help
        elif read_or_send.lower().startswith("h") or read_or_send.lower().startswith(
            "help"
        ):
            os.system("clear")
            logo()
            console.print(
                "Simple tool for safe communication with friends via gmail, messages are encrypted with public key cipher",
                style="bold blue",
            )
            console.print(
                "\t- To view your emails, press [bold red]ENTER[/bold red]",
                style="bold cyan",
            )
            console.print(
                "\t- To read an email, press [bold red]r[/bold red]", style="bold cyan"
            )
            console.print(
                "\t- To send an email, press [bold red]s[/bold red]", style="bold cyan"
            )
            console.print(
                "\t- To quit, press [bold red]q[/bold red]", style="bold cyan"
            )
            console.print(
                "\t- Create new public and private keys with [bold red]nk[/bold red], or [bold red]newkeys[bold red]\n",
                style="bold cyan",
            )
            console.print(
                "More information about program on https://www.github.com/foglar/safeMail/\n",
                style="bold blue",
            )
        # New keys
        elif read_or_send.lower().startswith("nk") or read_or_send.lower().startswith(
            "newkeys"
        ):
            makeNewKeys()
        # Exit program
        elif read_or_send.lower().startswith("q") or read_or_send.lower().startswith(
            "quit"
        ):
            os.system("/bin/clear")
            for i in range(11):
                if os.path.exists(f"cache/email{i}.txt"):
                    os.remove(f"cache/email{i}.txt")
            if os.path.exists("cache/sendEmail.txt"):
                os.remove("cache/sendEmail.txt")
            console.print("Cache cleared!", style="bold red")
            console.print("Bye!", style="bold red")
            console.print(
                "More information about program on https://www.github.com/foglar/safeMail/",
                style="bold blue",
            )
            sys.exit()


def readEmails():
    senders = []
    emails = []
    timestamps = []
    emailsEncrypted = searchEmails()
    for i in range(len(emailsEncrypted)):

        emailFile = open(f"cache/email{i}.txt", "w")
        emailFile.write(emailsEncrypted[i].messages[0].body)
        emailFile.close()

        emailsDecrypted = decryptEmails(f"cache/email{i}.txt", "my_privkey.txt")
        emails.append(emailsDecrypted)
        senders.append(emailsEncrypted[i].messages[0].sender)
        timestamps.append(emailsEncrypted[i].messages[0].timestamp)

    return senders, emails, timestamps


def readEmail():
    emailEncrypted = searchEmails()

    emailNum = pyip.inputInt("Email number > ", max=len(emailEncrypted))
    emailNum -= 1

    emailFile = open(f"cache/email{emailNum}.txt", "w")
    emailFile.write(emailEncrypted[emailNum].messages[0].body)
    emailFile.close()

    emailDecrypted = decryptEmails(f"cache/email{emailNum}.txt", "my_privkey.txt")
    emailBody = emailDecrypted
    emailSender = emailEncrypted[emailNum].messages[0].sender
    emailTime = emailEncrypted[emailNum].messages[0].timestamp

    return emailSender, emailBody, emailTime


def sendEmails():
    console.print("Send email", style="bold blue")
    recipient = pyip.inputMenu(list_Contacts(), numbered=True)

    if recipient == "New contact":
        recipient = addContact()

    print("")
    publicKey = pyip.inputMenu(list_Keys(), numbered=True)

    if publicKey == "Costume key":
        publicKey = newPathToKey()
    else:
        publicKey = "keys/" + publicKey

    print("")
    message = console.input("Message: ")

    emailFile = open("cache/sendEmail.txt", "w")
    emailFile.write(message)
    emailFile.close()

    messageEncrypted = encryptEmails("cache/sendEmail.txt", publicKey, message)

    ezgmail.send(recipient, "SafeMail", messageEncrypted)
    console.print("Email sent!")


def searchEmails():
    encryptedMessages = ezgmail.search("label:inbox", maxResults=10)
    return encryptedMessages


def decryptEmails(message, key):
    try:
        messageDec = publicKeyCipher.readFromFileAndDecrypt(message, key)
    except Exception:
        messageDec = open(message, "r").read()
    return messageDec


def encryptEmails(file, key, message):
    messageEnc = publicKeyCipher.encryptAndWriteToFile(file, key, message)
    return messageEnc


def makeNewKeys():
    os.system("/bin/clear")
    console.print(
        "[bold red]WARNING[/bold red]: This will delete your current keys, so you would be unable to read all your previous conversations, are you sure you want to continue? (y/n)",
        style="bold red",
    )
    if console.input() == "y":
        date = d.now().strftime("%Y-%m-%d-%H:%M:%S")
        backupFilePath = Path(f"backup/my_pubkey_backup_{date}.txt")
        backupFilePath2 = Path(f"backup/my_privkey_backup_{date}.txt")
        if not os.path.exists("backup"):
            os.mkdir("backup")
        shutil.copy(f"my_pubkey.txt", backupFilePath)
        shutil.copy(f"my_privkey.txt", backupFilePath2)
        os.remove("my_privkey.txt")
        os.remove("my_pubkey.txt")
        makePublicPrivateKeys.makeKeyFiles("my", 1024)
        os.system("/bin/clear")
        console.print(
            "Public key: /keys/my_pubkey.txt, private key: /keys/my_privkey.txt",
            style="bold blue",
        )
        console.print(
            "[bold red]WARNING[/bold red]: Don't share privkey.txt with anyone.",
            style="bold blue",
        )
    else:
        console.print("Aborting...", style="bold red")


def list_Contacts():
    contacts = []
    with open("contacts.txt", "r") as f:
        contacts = f.readlines()
    contacts = [x.strip() for x in contacts]

    contacts.append("New contact")
    return contacts


def list_Keys():
    keys = []
    keys = os.listdir("keys")
    keys.append("Costume key")
    return keys


def addContact():
    while True:
        contact = pyip.inputEmail("Email address: ")
        if contact in list_Contacts():
            console.print(f"Contact {contact} already exists!", style="bold red")
        else:
            with open("contacts.txt", "a") as f:
                f.write(contact + "\n")
                f.close()
                break

    console.print(f"Contact {contact} added!", style="bold green")


def newPathToKey():
    while True:
        key = pyip.inputFilepath("Key path: ")
        if os.path.exists(key):
            console.print(f"Key {key}!", style="bold green")
            break
        else:
            console.print(f"Path to {key} not exist!", style="bold red")
    return key


def logo():
    console.print("            __    ___  ___      _ _ ", style="bold cyan")
    console.print("           / _|   |  \/  |     (_) |", style="bold cyan")
    console.print(" ___  __ _| |_ ___| .  . | __ _ _| |", style="bold cyan")
    console.print("/ __|/ _` |  _/ _ \ |\/| |/ _` | | |", style="bold cyan")
    console.print("\__ \ (_| | ||  __/ |  | | (_| | | |", style="bold cyan")
    console.print(
        "|___/\__,_|_| \___\_|  |_/\__,_|_|_|, by [bold red]foglar[bold red]\n",
        style="bold cyan",
    )


if __name__ == "__main__":
    main()
