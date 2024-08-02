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
version = "0.1.8"

try:
    from octoprint.access import ADMIN_GROUP
except:
    self_logger.info("An Admin Group error occured")
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
__plugin_name__ = "OctoMail"
__plugin_version__ = version
__plugin_pythoncompat__ = ">=3,<4"
__plugin_description__ = "Makes OctoPrint Work Over Email!!!"
__plugin_author__ = "Fleecy"
##myEmails()
class OctoMailPlugin(octoprint.plugin.StartupPlugin, octoprint.printer.PrinterInterface, octoprint.plugin.TemplatePlugin, octoprint.plugin.WebcamProviderPlugin):
    get_line = lambda self, name, line, split: open(name, "r").readlines()[line].strip().split(split)
## Cut 1
## Cut bottom 1
## Cut top cut 2
## Cut Bottom
##        except:
##            print("An Error Occured")
try:
    __plugin_hooks__ = {
        "octoprint.access.permissions": get_additional_permissions
    }
except:
    self._logger.info("A Perms error occured")
try:
    __plugin_implementation__ = OctoMailPlugin()
except:
    self._logger.info("A fatal Error occured")


##class OctoMailRun(octoprint.plugin.types.OctoPrintPlugin):
##    myEmails()
##__plugin_implementation__ = OctoMailRun, OctoMailPlugin
