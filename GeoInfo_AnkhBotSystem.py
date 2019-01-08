

#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
#from Settings_Module import MySettings
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Geoinfo"
Website = ""
Description = "information useful for geoguessr game"
Creator = "Fizzix"
Version = "1.0.0.0"


import codecs

#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
defaultsettingsFile = os.path.join(os.path.dirname(__file__), "defaultsettings.json")

countryFile = os.path.join(os.path.dirname(__file__), "countries.json")
countryDetails = os.path.join(os.path.dirname(__file__), "countryfiles/")

class Settings(object):
    def __init__(self, settingsfile=None):
        if settingsFile and os.path.isfile(settingsFile):
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-8-sig")
        else:
            self.GeoInfo = "!geo"
            self.AdminPermission = "Moderator"
            self.InfoPermission = "Everyone"
            self.PermissionInfo = ""

    def Reload(self, jsondata):
        self.__dict__ = json.loads(jsondata, encoding="utf-8")
        return

    def Save(self, settingsfile):
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8")
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
        except:
            Parent.Log(ScriptName, "Failed to save settings to file.")
        return
        
#load the country data
with open(countryFile, "r") as rf:
    countries = json.load(rf)

ctydict = {}
    
for ctykey in list(countries):
    #print cty, countries[cty]
    try:
        with open(countryDetails+ctykey+'.json', 'r') as rf:
            ctydict[ctykey] = json.load(rf)
        # Store configuration file values
    except IOError:
        # Keep preset values
        ctydict[ctykey] = None



def GeoInfo(s):
    numparams = s.GetParamCount()
    #Parent.SendStreamMessage('num params:' + str(numparams))
    if numparams == 1:
        return
    ctykey = s.GetParam(1)
    if numparams == 2:
        
        if ctykey in countries:
            Parent.SendStreamMessage(ctykey + ': ' + countries[ctykey])
        return
    if numparams > 2:
        ctydata = ctydict[ctykey]
        
        if ctydata == None:
            return
        
        for i in xrange(2, numparams):
            subcom = s.GetParam(2)
            if subcom not in ctydata:
                return
            else:
                ctydata = ctydata[subcom]
    Parent.SendStreamMessage(ctydata)

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():

    global MySettings
    MySettings = Settings(settingsFile)
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):

    if data.IsChatMessage() and data.GetParam(0).lower() == MySettings.GeoInfo.lower():
        HasPerm = Parent.HasPermission(data.User, MySettings.InfoPermission, MySettings.PermissionInfo)
        if HasPerm:
            GeoInfo(data)
    
    
    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    
    if "$myparameter" in parseString:
        return parseString.replace("$myparameter","I am a cat!")
    
    return parseString

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    global MySettings
    MySettings.__dict__ = json.loads(jsonData)
    MySettings.Save(SettingsFile)
    return

