# 821C3 Emoji DB Plugin
# v1 5/18/2020

#encoding=utf8
from wox import Wox
from csv import reader
from os import path

#win32 functions - copy to clipboard and type selected emoji
from win32 import *

#Your class must inherit from Wox base class https://github.com/qianlifeng/Wox/blob/master/PythonHome/wox.py
#The wox class here did some works to simplify the communication between Wox and python plugin.
class Emoji(Wox):

    # A function named query is necessary, we will automatically invoke this function when user query this plugin
    def query(self,key):
        key = key.lower()
        if len(key)<3:
            return
        #Load EmojiDB
        with open('emojidb.csv', "r", encoding="utf-8") as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Pass reader object to list() to get a list of lists
            emlist = list(csv_reader)
        results = []
        for row in emlist[1:]:
            searches = [(word in row[3]) for word in key.split(" ")]
            if sum(searches) == len(searches): 
                emoji = ''.join([chr(int(code, 16)) for code in row[1].split('-')])
                if path.exists("Images/Emojis/"+row[1]+".png"):
                    pathImg = "Images/Emojis/"+row[1]+".png"
                else:
                    pathImg = "Images/icon.png"
                results.append({
                    "Title": emoji,
                    "SubTitle":row[2],
                    "IcoPath":pathImg,
                    "JsonRPCAction":{
                        "method": "copy",
                        "parameters":[emoji], 
                        "dontHideAfterAction":False
                    }
                })
        return results

    def copy(self,code):
        put(code)
        ### inputting selected emoji (Alt+Tab + Ctrl+V), too slow to be used !
        #PressAltTab()
        #PressKey(CTRL)
        #PressKey(V)
        #time.sleep(0.1)
        #ReleaseKey(V)
        #ReleaseKey(CTRL)

#Following statement is necessary
if __name__ == "__main__":
    Emoji()