import platform
import os
import json
import copy

class SettingsHandler(object):
    default = { "windowX": 100, "windowY": 100,
                 "windowHeight": 500, "windowWidth": 750,
                 "auth": []
                }
    def __init__(self):
        if (platform.system() == "Windows"):
            self.path = os.environ['APPDATA'] + "\\FusionChat"
            filename = "fusionchat.json"
        else:
            self.path = os.environ['HOME']
            filename = ".fusionchat"
            
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            
        self.fullPath = os.path.join(self.path, filename)
            
        if not os.path.exists(self.fullPath):
            settingsFile = open(self.fullPath, 'w')
            json.dump(self.default, settingsFile, indent=4)
            settingsFile.close()
            
        settingsFile = open(self.fullPath, 'r')
        self.settings = json.load(settingsFile)
        settingsFile.close()
    
    def setSettings(self, **kwargs):
        self.settings.update(kwargs)
        self.writeSettings()
        
    def getSettings(self):
        return self.settings
    
    def writeSettings(self):
        settingsFile = open(self.fullPath, 'w')
        json.dump(self.settings, settingsFile, indent=4)
        settingsFile.close()
    
settings = SettingsHandler()
