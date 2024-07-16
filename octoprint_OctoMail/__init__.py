#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      unsee
#
# Created:     18/06/2024
# Copyright:   (c) unsee 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------
version = "0.1.5"
from octoprint.access import ADMIN_GROUP
import os
import os.path
import octoprint.plugin
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
import base64



'''
__plugin_hooks__ = {
    "octoprint.access.permissions": get_additional_permissions
} '''
__plugin_implementation__ = OctoMailPlugin()
__plugin_name__ = "OctoMail"
__plugin_version__ = version
__plugin_description__ = "Makes OctoPrint Work Over Email"
__plugin_author__ = "Fleecy"
__plugin_pythoncompat__ = ">=3.7,<4"








##myEmails()
class OctoMailPlugin(octoprint.plugin.StartupPlugin, octoprint.printer.PrinterInterface, octoprint.plugin.TemplatePlugin, octoprint.plugin.WebcamProviderPlugin):
    get_line = lambda self, name, line, split: open(name, "r").readlines()[line].strip().split(split)
    '''
    def get_additional_permissions(*args, **kwargs):
    return [
        dict(key="ADMIN",
             name="Admin access",
             description=gettext("Allows administrating all application keys"),
             roles=["admin"],
             dangerous=True,
             default_groups=[ADMIN_GROUP])
    ]
    '''
    def on_after_startup(self):
        for i in range(0, 3):
            print("#########################")
        print("#####OCTOMAIL ACTIVE#####")
        for i in range(0, 3):
            print("#########################")
        self._logger.info("OctoMail Loaded")
        defaults = "0.0.10\n\n\n\n!, !\nprint, print\nview, view\nignore, ignore\npreheat, preheat\nhelp, help\naddsafeuser, addsafeuser\nremovesafeuser, removesafeuser\naddtempviewer, addtempviewer\naddviewer, addviewer\nremoveviewer, removeviewer\nconfig, config\nresetconfig, resetconfig\nstop, stop\npause, pause\nresume, resume\ncmdselector, cmdselector"
        get_line = lambda name, line, split: (open(name).readlines()[line].strip().split(split))
        try:
            with open("OctoMailConfig.txt", "r") as f:
                f.read()
        except FileNotFoundError:
            try:
                with open("OctoMailDefaults.txt", "r") as f:
                    f.read()
            except FileNotFoundError:
                with open("OctoMailDefaults.txt", "w") as f:
                    f.write(defaults)
                with open("OctoMailConfig.txt", "w") as f:
                    f.write(defaults)
            else:
                with open("OctoMaildefaults.txt", "r") as f:
                    new_defaults = f.readlines()
                with open("OctoMailConfig.txt", "w") as f:
                    f.writelines(new_defaults)


        finally:
            try:
                with open("OctoMailConfig.txt", "r") as f:
                    config_lines = f.readlines()
                    print(config_lines[0][:-1])
                    if config_lines[0][:-1] != version:

                        print("Updating Config defaults...")
                        with open("OctoMailDefaults.txt", "w") as f:
                            f.write(defaults)
                        print("Config Defaults Updated")
                        num1 = 0
                        print("Begining Config Update...")

                        for lines in config_lines:
                            num1 += 1
                        with open("OctoMailDefaults.txt", "r") as df:
                            default_file_lines = df.readlines()
                            num2 = 0
                            for line in default_file_lines:
                                num2 += 1
                            num3 = (num2 - num1)-1
                            num4 = 0
                            print("Updating Config...")
                            with open("OctoMailConfig.txt", "a") as cf:
                                cf.write("\n")
                                cf.writelines(default_file_lines[num1:])

                        with open("OctoMailConfig.txt", "r") as vcf:
                            config_version_change = vcf.readlines()

                            config_version_change[0]=version + "\n"
                        with open("OctoMailConfig.txt", "w") as vcfc:
                            vcfc.writelines(config_version_change)
                        print("Update Complete!")
            except IndexError:
                pass
            except FileNotFoundError:
                with open("OctoMailDefaults.txt", "w") as f:
                    f.write(defaults)
                with open("OctoMailConfig.txt", "w") as f:
                    f.write(defaults)
                
        SCOPES = ["https://mail.google.com/"]

        self.t = octoprint.util.RepeatedTimer(0.25, self.myEmails)
        self.t.start()
        self.myEmails()
##        myEmails()

    def send_message(self, service, message, subject, target, attachment="None"):
        try:
            if attachment == "None":
                msg = MIMEText(message)
                msg["to"] = target
                msg["subject"] = subject
                
                msg_create = {"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode()}
                msg = (service.users().messages().send(userId="me", body=msg_create).execute())
            else:
                part = self.MIMEBase("application", "octet-stream")
                part.set_payload(attachment)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= 'attachment.txt'",
                )
                msg = self.MIMEMultipart()

                msg["To"] = target
                msg["Subject"] = subject
                html_part = MIMEText(message)
                msg.attach(html_part)
                msg.attach(part)
            

                
                msg_create = {"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode()}
                msg = (service.users().messages().send(userId="me", body=msg_create).execute())
            print("Sent Message")
        except HttpError as error:
            print(f"An error occured: {error}")


    ##try:
    ##    with open("OctoMailConfig.txt", "r") as f:
    ##        f.read()
    ##except:
    ##    try:
    ##        with open("OctoMailDefaults.txt", "r") as f:
    ##            f.read()
    ##    except:
    ##        with open("OctoMailDefaults.txt", "w") as f:
    ##            f.write(defaults)
    ##        with open("OctoMailConfig.txt", "w") as f:
    ##            f.write(defaults)
    ##    else:
    ##        with open("OctoMaildefaults.txt", "r") as f:
    ##            new_defaults = f.readlines()
    ##        with open("OctoMailConfig.txt", "w") as f:
    ##            f.writelines(new_defaults)
    ##
    ##
    ##finally:
    ##    try:
    ##        with open("OctoMailConfig.txt", "r") as f:
    ##            config_lines = f.readlines()
    ##            print(config_lines[0][:-1])
    ##            if config_lines[0][:-1] != version:
    ##
    ##                print("Updating Config defaults...")
    ##                with open("OctoMailDefaults.txt", "w") as f:
    ##                    f.write(defaults)
    ##                print("Config Defaults Updated")
    ##                num1 = 0
    ##                print("Begining Config Update...")
    ##
    ##                for lines in config_lines:
    ##                    num1 += 1
    ##                with open("OctoMailDefaults.txt", "r") as df:
    ##                    default_file_lines = df.readlines()
    ##                    num2 = 0
    ##                    for line in default_file_lines:
    ##                        num2 += 1
    ##                    num3 = (num2 - num1)-1
    ##                    num4 = 0
    ##                    print("Updating Config...")
    ##                    with open("OctoMailConfig.txt", "a") as cf:
    ##                        cf.write("\n")
    ##                        cf.writelines(default_file_lines[num1:])
    ##
    ##                with open("OctoMailConfig.txt", "r") as vcf:
    ##                    config_version_change = vcf.readlines()
    ##
    ##                    config_version_change[0]=version + "\n"
    ##                with open("OctoMailConfig.txt", "w") as vcfc:
    ##                    vcfc.writelines(config_version_change)
    ##                print("Update Complete!")
    ##    except:
    ##        pass

    def cmd_decoder(self, cmd_num, info, info_2, info_3, service, sender, safe_emails):
        print(f"CMD Num: {cmd_num}")
        cmd_num - 4
        with open("OctoMailConfig.txt", "r") as f:
            line = f.readlines()
            help_command = line[9][5:-1]
            view_command = line[6][5:-1]
            command_selector = line[4][3]

        if cmd_num == 1:
            print(f"printing {info}")
            if not self._printer.is_printing():
                if self._printer.get_current_connection() == ("Closed", None, None, None):
                    self._printer.connect()
                self._printer.select_file(info, False, False)
                self._printer.start_print()
                if len(info) == 0:
                    self.send_message(service, "You must add the name of the file you wish to print in the subject (<command selector><print command> <file>)", "Error Starting Print", sender)
            else:
                self.send_message(service, "You must wait for the printer to stop printing before you can start a print", "Error Starting Print", sender)
        elif cmd_num == 2:
            print("viewing")
            snapshot = []
            if self._printer.get_current_connection() == ("Closed", None, None, None):
                    self._printer.connect()
            webcam = ""
            for i in self.get_webcam_configurations():
                webcam = i
            self.send_message(service, "", "Report:", sender, self.take_webcam_snapshot(webcam))

                

        elif cmd_num == 3:
            print("ignoring")
        elif cmd_num == 4:
            print("Preheating Bed: {info}, Tool: {info_2}")
            if self._printer.get_current_connection() == ("Closed", None, None, None):
                    self._printer.connect()
            self._printer.set_temperature("bed", int(info))
            self._printer.set_temperature("chamber", int(info_2))
        elif cmd_num == 5:
            help_text = "NOTE: All commands listed are the defaults ONLY:\n\n\nPrint: !print <file>, Starts printing the chosen file\n\nView: !view, Shows what the printer is currently doing\n\nIgnore: !ignore, Prevents GCODE files from being downloaded if they otherwise would be\n\nPreheat: !preheat <bed temperature> <tool temperature>, Preheats to selected temperatures\n\nAdd Safe User: !addsafeuser <email>, Allows the chosen email to use all commands, WARNING ONLY GIVE PEOPLE YOU TRUST THIS PERMISSION\n\nRemove Safe User: !removesafeuser <email> Disallows the chosen email from being able to run commands\n\nAdd Viewer: !addviewer <email> Allows the selected user to use the '!view' command, This permission is best for people you trust enough to view the printer but not enough with full permissions\n\nRemove Viewer: !removeviewer <email>, Disallows the selected email from being able to use the '!view' command\n\nAdd Temporary Viewer: !addtempviewer, Allows the selected user to use the '!view' command but only on that print, This is best for prints for others so they can watch it print\n\nConfig: !config <default command name> <new command name>, Changes the name of the selected command to a different name\n\nReset Config: !resetconfig <optional command to be reset if left empty all commands will be reset>, Resets chosen commmand/ all commands ONLY it will not delete anyone's permissions\n\nStop: !stop, Stops the print\n\nPause: !pause, Pauses the print\n\nResume: !resume, Resumes the print\n\nCommand Selector: !cmdselector <new command selector>, Replaces the '!' at the start of the command with a different symbol, WARNING DO NOT SET IT TO A LETTER/NUMBER"
            self.send_message(service, help_text, "All Commands:", sender)
        elif cmd_num == 6:
            with open("OctoMailConfig.txt", "r") as f:
                lines = f.readlines()
                lines[1] = lines[1][:-1] + " " + info + "\n"
            with open("OctoMailConfig.txt", "w") as f:
                f.writelines(lines)
                print(f'Added User: "{info}"')
                self.send_message(service, f"You have been added to the Safe Users list meaning you can now use all of the bot commands, Use '{command_selector+help_command}' to get a list of all default commands", "Permissions update", info)
                for i in safe_emails:
                    self.send_message(service, f"{info} has been added to the safe senders list", "A user's permission has been updated", i)
        elif cmd_num == 7:
            safe_emails = []
            new_safe_emails = ""
            with open("OctoMailConfig.txt", "r") as f:
                user = ""
                for i in f.readlines()[1]:
                    if i != " ":
                        user += i
                    elif i == " ":
                        safe_emails.append(user)
                        user = ""
                safe_emails.append(user[:-1])
            with open("OctoMailConfig.txt", "r") as f:
                config_lines = f.readlines()
                for email in safe_emails:
                    if email != info:
                        if new_safe_emails == "":
                            new_safe_emails = email
                        else:
                            new_safe_emails += " " + email

                config_lines[1] = new_safe_emails + "\n"
            with open("OctoMailConfig.txt", "w") as f:
                f.writelines(config_lines)
                print(f'Removed User: "{info}"')
                self.send_message(service, "You have been removed from the Safe Users list meaning you can no longer use all of the bot commands use ", "Permissions update", info)
                for i in safe_emails:
                    self.send_message(service, f"{info} has been removed from the safe senders list", "A user's permission has been updated", i)
        elif cmd_num == 8:
            with open("OctoMailConfig.txt", "r") as f:
                lines = f.readlines()
                lines[3] = lines[3][:-1] + " " + info + "\n"
            with open("OctoMailConfig.txt", "w") as f:
                f.writelines(lines)
                print(f'Added Temporary Viewer: "{info}"')
                self.send_message(service, f"You have been added to the Temporary Viewer list meaning you can now use the view command: '{command_selector+view_command}' to view the printer for the rest of the print", "Permissions update", info)
                self.send_message(service, f"Added {info} to the Temporary Viewer list", "A user's permission has been updated", sender)
        elif cmd_num == 9:
            with open("OctoMailConfig.txt", "r") as f:
                lines = f.readlines()
                lines[2] = lines[2][:-1] + " " + info + "\n"
            with open("OctoMailConfig.txt", "w") as f:
                f.writelines(lines)
                print(f'Added Viewer: "{info}"')
                self.send_message(service, f"You have been added to the Viewer list meaning you can now use the view command: '{command_selector+view_command}' to view the printer", "Permissions update", info)
                self.send_message(service, f"Added {info} to the Viewer list", "A user's permission has been updated", sender)
        elif cmd_num == 10:
            viewers = []
            new_viewers = ""
            with open("OctoMailConfig.txt", "r") as f:
                user = ""
                for i in f.readlines()[2]:
                    if i != " ":
                        user += i
                    elif i == " ":
                        viewers.append(user)
                        user = ""
                viewers.append(user[:-1])
            with open("OctoMailConfig.txt", "r") as f:
                lines = f.readlines()
                for email in viewers:
                    if email != info:
                        if len(new_viewers) == 0:
                            new_viewers = email
                        else:
                            new_viewers += " " + email

                lines[2] = new_viewers + "\n"
            with open("OctoMailConfig.txt", "w") as f:
                f.writelines(lines)
            viewers = []
            new_viewers = ""
            with open("OctoMailConfig.txt", "r") as f:
                user = ""
                for i in f.readlines()[3]:
                    if i != " ":
                        user += i
                    elif i == " ":
                        viewers.append(user)
                        user = ""
                viewers.append(user[:-1])
            with open("OctoMailConfig.txt", "r") as f:
                lines = f.readlines()
                for email in viewers:
                    if email != info:
                        if len(new_viewers) == 0:
                            new_viewers = email
                        else:
                            new_viewers += " " + email

                lines[3] = new_viewers + "\n"
            with open("OctoMailConfig.txt", "w") as f:
                f.writelines(lines)
                print(f'Removed Viewer: "{info}"')
                self.send_message(service, f"You have been removed to the Viewer list meaning you can no longer use the view command: '{command_selector+view_command}'", "Permissions update", info)
                self.send_message(service, f"Removed {info} from the the Viewer list", "A user's permission has been updated", sender)
        elif cmd_num == 11:
            with open("OctoMailConfig.txt", "r") as f:
                lines = f.readlines()
                num = 4
                default_cmd_location = 0
                default_cmd_save = ""
                for i in lines[5:]:
                    default_cmd = ""
                    cmd_recorded = False

                    for x in i:
                        if x != " " and x != "," and not cmd_recorded:
                            default_cmd += x
                        elif x == " ":
                            cmd_recorded = True
                    num += 1
                    if default_cmd == info:
                        default_cmd_location = num
                        default_cmd_save = default_cmd
                print(f"default CMD Location: {default_cmd_location}")
                lines[default_cmd_location] = default_cmd_save + ", " + info_2 + "\n"
            if len(default_cmd_save) != 0:
                with open("OctoMailConfig.txt", "w") as f:
                    f.writelines(lines)
                    print(f'Changed CMD: "{default_cmd_save}" To: "{info_2}"')

        elif cmd_num == 12:
            with open("OctoMailDefaults.txt", "r") as f:
                default_lines = f.readlines()
            with open("OctoMailConfig.txt", "r") as f:
                lines = f.readlines()
            with open("OctoMailConfig.txt", "w") as f:
                if len(info) == 0:
                    f.writelines(lines[:4])
                    f.writelines(default_lines[4:])
                    print("RESETTING CONFIG")
                else:
                    num = 3
                    cmd_location = 0
                    for i in lines[4]:
                        default_cmd = ""
                        current_cmd = ""
                        cmd_recorded = False

                        for x in i:
                            if x != " " and x != "," and not cmd_recorded:
                                default_cmd += x
                            elif x == " ":
                                cmd_recorded = True
                            elif x != " " and x != "," and cmd_recorded:
                                current_cmd += x
                        num += 1
                        if default_cmd == info:
                            cmd_location = num
                        elif current_cmd == info:
                            cmd_location = num
                    lines[cmd_location] = default_lines[cmd_location]
                    f.writelines(lines)
                    print(f"RESETTING COMMAND '{info}' IN CONFIG")



        elif cmd_num == 13:
            print("Stopping...")
            if self._printer.get_current_connection() == ("Closed", None, None, None):
                self._printer.connect()
            self._printer.cancel_print()
        elif cmd_num == 14:
            print("Pausing...")
            if self._printer.get_current_connection() == ("Closed", None, None, None):
                self._printer.connect()
            self._printer.pause_print()
        elif cmd_num == 15:
            print("Resuming...")
            if self._printer.get_current_connection() == ("Closed", None, None, None):
                self._printer.connect()
            self._printer.resume_print()
        elif cmd_num == 16:
            with open("OctoMailConfig.txt", "r") as f:
                lines = f.readlines()
                lines[4] = "!, " + info + "\n"
            with open("OctoMailConfig.txt", "w") as f:
                f.writelines(lines)
    def send_perms_error(self, raw_senders, safe_emails, viewers, tempviewers, service, subject):
        try:
            with open("OctoMailConfig.txt", "r") as f:
                config_lines = f.readlines()
                found_cmd = False
                found_cmd_select = False
                cmd = ""
                cmd_selector = ""
                for i in config_lines[8]:
                    if i == " " and not found_cmd:
                        found_cmd = True
                    elif found_cmd and not i == " ":
                        cmd += i
                for n in config_lines[4]:
                    if n == " " and not found_cmd_select:
                        found_cmd_select = True
                    elif found_cmd_select and not n == " ":
                        cmd_selector += n
                cmd_selector = cmd_selector[0]
                print(f"Command Selector: {cmd_selector}")
            num = 0
            for n in raw_senders:
                if len(subject[num]) != 0:
                    print(subject[num][0])
                    if n in safe_emails or len(safe_emails) == 1 and safe_emails[0] == "":
                        print(f"{n} is Safe and Valid")
                    else:
                        if subject[num][0] == cmd_selector:
                            with open("OctoMailConfig.txt", "r") as f:
                                found_cmd = False
                                cmd = ""
                                for i in f.readlines()[6]:
                                    if i == " " and not found_cmd:
                                        found_cmd = True
                                    elif found_cmd and not i == " ":
                                        cmd += i
                                cmd = cmd[:-1]
                                print(f"View CMD: {cmd}")
                            if subject[num][1:] != cmd or (not n in viewers and not n in tempviewers):

                                print(f"{n} is not safe or valid")
                                perms_error_msg = MIMEText("I'm Sorry But You Do Not Have The Permisions To Use That Command")
                                perms_error_msg["to"] = n
                                perms_error_msg["subject"] = "Permisions Error"
                                perms_error_msg_create = {"raw": base64.urlsafe_b64encode(perms_error_msg.as_bytes()).decode()}
                                perms_error_msg = (service.users().messages().send(userId="me", body=perms_error_msg_create).execute())
                num += 1
        except HttpError as error:
            print(f"An error occured: {error}")
    def myEmails(self):
        SCOPES = ["https://mail.google.com/"]
        #watched_path = "C:\Users\unsee\AppData\Roaming\OctoPrint\watched\ "[:-1]
        watched_path = "C:\\Users\\unsee\\AppData\\Roaming\\OctoPrint\\watched\\"
        subject = []
        senders = []
        body = []
        safe_emails = []
        viewers = []
        tempviewers = []
        all_paths = []
        all_file_datas = []
    ##    with open("OctoMailConfig.txt", "r") as f:
    ##        lines = f.readlines()
    ##        user = ""
    ##        for i in lines[1]:
    ##            if i != " ":
    ##                user += i
    ##            elif i == " ":
    ##                safe_emails.append(user)
    ##                user = ""
    ##        safe_emails.append(user[:-1])
    ##        user = ""
    ##        for i in lines[2]:
    ##            if i != " ":
    ##                user += i
    ##            elif i == " ":
    ##                viewers.append(user)
    ##                user = ""
    ##        viewers.append(user[:-1])
    ##        user = ""
    ##        for i in lines[3]:
    ##            if i != " ":
    ##                user += i
    ##            elif i == " ":
    ##                tempviewers.append(user)
    ##                user = ""
    ##        tempviewers.append(user[:-1])
    ##        viewers.pop(0)
    ##        tempviewers.pop(0)
        safe_emails = self.get_line("OctoMailConfig.txt", 1, " ")
        viewers = self.get_line("OctoMailConfig.txt", 2, " ")
        tempviewers = self.get_line("OctoMailConfig.txt", 3, " ")
        print(f"Safe Users: {safe_emails}")
        print(f"Safe Emails Length: {len(safe_emails)}")
        print(f"Viewers: {viewers}")
        print(f"Temporary Viewers: {tempviewers}")
        already_read = False
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
                self._logger.info(InstalledAppFlow.authorization_url())
            with open("token.json", "w") as f:
                f.write(creds.to_json())


        try:

            service = build("gmail", "v1", credentials=creds, cache_discovery=False)
            result = service.users().messages().list(userId="me").execute()
            unchecked_messages = result.get("messages")
            check = service.users().messages().list(userId="me", q=["label:fleecyprinterbotread "])
            check2 = service.users().messages().list(userId="me", labelIds=["SENT"]).execute().get("messages")
            spam_msgs = service.users().messages().list(userId="me", labelIds=["SPAM"]).execute().get("messages")
    ##        check = service.users().messages().list(userId="me", labelIds=["INBOX"])
    ##        print(spam_msgs)
            try:
                for z in spam_msgs:
                    unchecked_messages.append(z)
            except TypeError:
                pass
    ##        print(check.execute().get("messages"))
            check_results = check.execute().get("messages")
            message_checking = []
            messages = []
            for n in check_results:
                message_checking.append(n)
            for c in check2:
                message_checking.append(c)
    ##        print(message_checking)
    ##        print(unchecked_messages)
            for x in unchecked_messages:
    ##            print("looped")
                if not x in message_checking:
                    messages.append(x)
    ##                print("Appending...")
    ##        print(service.users().messages().list(userId="me").execute()["FleecyPrinterBotRead"])
    ##        label_body = {
    ##"name": "FleecyPrinterBotRead",
    ##"messageListVisibility": "show",
    ##"labelListVisibility": "labelShow",
    ##}
    ##        service.users().labels().create(userId='me', body=label_body).execute()
            for i in messages:
                paths = []
                file_datas = []
                txt = service.users().messages().get(userId="me", id=i["id"]).execute()
    ##            print(f"TXT: {txt}")
                for part in txt['payload']['parts']:
                    if part['filename']:
                        if 'data' in part['body']:
                            data = part['body']['data']
                        else:

                            att_id = part['body']['attachmentId']
                            att = service.users().messages().attachments().get(userId="me", messageId=i["id"],id=att_id).execute()
                            data = att['data']
                        file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                        path = part['filename']
                        print(f"Path: {path}")
                        if ".gcode" in str(path.strip()):
                            print("Appended Path")
                            paths.append(path)
                            file_datas.append(file_data)
                all_paths.append(paths)
                all_file_datas.append(file_datas)



                payload = txt["payload"]
                headers = payload["headers"]
                service.users().messages().modify(userId="me", id=i["id"], body={"addLabelIds": ["Label_5"], "removeLabelIds": ["SPAM"]}).execute()
                for i in headers:
    ##                already_read = service.users().labels().get(userId="me", id="Processed")

                    already_read = i in message_checking
                    if i["name"] == "Subject" and not already_read:
                        subject.append(i["value"])
                    if i["name"] == "From" and not already_read:
                        sender = i["value"]
                        if sender != "fleecyprinter1@gmail.com":
                            senders.append(sender)
    ##            print(payload.get("parts"))
    ##            parts = payload.get("parts")[0]
    ##            data = parts["body"]["data"]
    ##            data = data.replace("-", "+").replace("_", "/")
    ##            decode_data = base64.b64decode(data)
    ##            if not already_read:
    ##                body.append(decode_data.strip())
    ##        print(f"Body: {body}")
            print(f"Subject: {subject}")
            print(f"Sender: {senders}")

            raw_senders = []
            for d in senders:
                start_adding_to_raw_senders = False
                current_raw_sender = ""
                for x in d:
                    if x == "<":
                        start_adding_to_raw_senders = True
                    elif start_adding_to_raw_senders and x != "<" and x!= ">":
                        current_raw_sender += x.lower()
                raw_senders.append(current_raw_sender)
            print(f"Raw Senders: {raw_senders}")
            raw_senders = raw_senders[::-1]
            subject = subject[::-1]
            all_file_datas = all_file_datas[::-1]
            all_paths = all_paths[::-1]
            self.send_perms_error(raw_senders, safe_emails, viewers, tempviewers, service, subject)
            num = 0
            with open("OctoMailConfig.txt", "r") as f:
                found_cmd = False
                cmd = ""
                for i in f.readlines()[6]:
                    if i == " " and not found_cmd:
                        found_cmd = True
                    elif found_cmd and not i == " ":
                        cmd += i
                view_cmd = cmd[:-1]
                print(f"View CMD: {cmd}")
            with open("OctoMailConfig.txt", "r") as f:
                config_lines = f.readlines()
    ##            found_cmd = False
                found_cmd_select = False
    ##            cmd = ""
                cmd_selector = ""
    ##            cmd_count = 0
    ##            target_cmd_num = 0
    ##            for line in config_lines[4:]:
    ##                cmd = ""
    ##                found_cmd = False
    ##
    ##                for i in line:
    ##                    if i == " " and not found_cmd:
    ##                        found_cmd = True
    ##                    elif found_cmd and not i == " ":
    ##                        cmd += i
    ##
    ##                if cmd == subject[num][0:]:
    ##                    target_cmd_num = cmd_count
    ##                cmd_count += 1
    ##                cmd_decoder(target_cmd_num)
                for n in config_lines[4]:
                    if n == " " and not found_cmd_select:
                        found_cmd_select = True
                    elif found_cmd_select and not n == " ":
                        cmd_selector += n
                cmd_selector = cmd_selector[0]
            cmd_count = 0
            current_sender = ""
            for n in raw_senders:
                current_sender = n
                if len(subject[num]) == 0:
                    subject[num] = "Empty"
                if len(subject[num]) != 0:
                    print(subject[num][0])
                    print(f"Current Subject: {subject[num][1:]}")
                    sub_cmd = ""
                    sub_info = ""
                    sub_info_2 = ""
                    sub_info_3 = ""
                    if_still_cmd = True
                    info_tag = 0
                    for x in subject[num][1:]:
                        if x != " " and if_still_cmd:
                            sub_cmd += x
                        elif x != " " and not if_still_cmd:
                            if info_tag == 1:
                                sub_info += x
                            elif info_tag == 2:
                                sub_info_2 += x
                            elif info_tag == 3:
                                sub_info_3 += x
                        elif x == " ":
                            if_still_cmd = False
                            info_tag += 1
                if n in safe_emails or len(safe_emails) == 1 and safe_emails[0] == "":
                    print(f"{n} is Safe and Valid")
                    if len(subject[num]) == 0:
                        subject[num] = "Empty"
                    if subject[num][0] == cmd_selector:
                        with open("OctoMailConfig.txt", "r") as f:
                            config_lines = f.readlines()
                            found_cmd = False
                            found_cmd_select = False
                            cmd = ""
                            cmd_selector = ""
                            cmd_count = 0
                            target_cmd_num = 0
                            for line in config_lines[4:]:
                                cmd = ""
                                found_cmd = False

                                for i in line.strip():
                                    if i == " " and not found_cmd:
                                        found_cmd = True
                                    elif found_cmd and not i == " ":
                                        cmd += i
        ##                        print(f"CMD: {cmd}")
                                if cmd == sub_cmd:
                                    print("subject cmd found")
                                    self.cmd_decoder(cmd_count, sub_info, sub_info_2, sub_info_3, service, raw_senders[num], safe_emails)
                                    
                                cmd_count += 1
                    

                            for n in config_lines[4]:
                                if n == " " and not found_cmd_select:
                                    found_cmd_select = True
                                elif found_cmd_select and not n == " ":
                                    cmd_selector += n
                            cmd_selector = cmd_selector[0]

        ##                    for lines in config_lines:
                    if cmd_count != 4:

                        print("Begining Writing Gcode Files...")
                        num2 = 0
                        for path_N in all_paths[num]:
                            print("LOOPED")
                            with open(str(watched_path+path_N).strip(), 'wb') as f:
                                f.write(all_file_datas[num][num2])
                                print("Uploaded")
                                self.send_message(service, "Successfully uploaded file", "Upload Successful", current_sender, "None")
                                num2 += 1
                        print("Finished Writing Gcode Files")



                elif subject[num][1:] == view_cmd and (n in viewers or n in tempviewers):
                    print("viewing")

                else:
                    if subject[num][0] == cmd_selector:
                        with open("OctoMailConfig.txt", "r") as f:
                            found_cmd = False
                            cmd = ""
                            for i in f.readlines()[6]:
                                if i == " " and not found_cmd:
                                    found_cmd = True
                                elif found_cmd and not i == " ":
                                    cmd += i
                            cmd = cmd[:-1]
                            print(f"View CMD: {cmd}")
                        if subject[num][1:] != cmd or (not n in viewers and not n in tempviewers):
                            print(f"{n} is not safe or valid")
                num+=1

        except HttpError as error:
            print(f"An error occured: {error}")
            self._logger.info(error)
##        except:
##            print("An Error Occured")






##class OctoMailRun(octoprint.plugin.types.OctoPrintPlugin):
##    myEmails()
##__plugin_implementation__ = OctoMailRun, OctoMailPlugin
