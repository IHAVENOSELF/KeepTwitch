import requests
import os
import time
import json
import sys
import subprocess
import win32api
import datetime
import getopt
import threading
import time
import signal
import webview
import tkinter.filedialog
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pathlib import *

root = Tk()
root.resizable(False, False)

class TwitchRecorder:
    sbar = Label(root, text="Starting...", bd=1, relief=SUNKEN)
    sbar.pack(side=BOTTOM, fill=X)

    def __init__(self):
        tkinter.messagebox.showinfo("Before Start", "Choose a save folder and authorize with Twitch")
        self.root_path = os.path.normpath(tkinter.filedialog.askdirectory(title="Choose Save Folder"))
        self.sbar.config(text="Save Folder Set")

        #set_save_folder_text()

        # global configuration
        self.client_id = "jzkbprff40iqj646a697cyrvl0zt2m6" # don't change this
        # get oauth token value by typing `streamlink --twitch-oauth-authenticate` in terminal
        self.ffmpeg_path = 'H:\Programs\Streamlink\ffmpeg\ffmpeg.exe'
        self.refresh = 15
        #self.root_path = "F:\Videos\Twitch"

        # user configuration
        #self.username =
        #self.quality = "best"
        self.t2 = threading.Thread(target=self.loopcheck)


        def authorize():
            def get_current_url():
                time.sleep(3)
                while "streamlink.github.io/twitch_oauth.html#access_token=" not in webview.get_current_url():
                    time.sleep(5)
                    print(webview.get_current_url())
                token1 = (webview.get_current_url().split("="))
                print(token1)
                #token1 = (str(token1[1]).strip("&scope"))
                token1 = (str(token1[1]))[:30]
                print(token1)
                self.oauth_token = token1
                webview.destroy_window()
                b2.config(state=DISABLED)
                self.sbar.config(text="Successfully Authorized")

            if __name__ == '__main__':
                t = threading.Thread(target=get_current_url)
                t.start()

            webview.create_window("Authenticate", "https://api.twitch.tv/kraken/oauth2/authorize/?response_type=token&client_id=pwkzresl8kj2rdj6g7bvxl9ys1wly3j&redirect_uri=https%3A%2F%2Fstreamlink.github.io%2Ftwitch_oauth.html&scope=user_read+user_subscriptions")

        def change_root_path():
            self.root_path = os.path.normpath(tkinter.filedialog.askdirectory(title="Choose Folder", parent=root))
            print(self.root_path)
            e2.config(state=NORMAL)
            e2.delete(0, END)
            e2.insert(0, (str(self.root_path)))
            e2.config(state="readonly")

        def set_params():
            #global usernamself.e1
            #self.t2 = threading.Thread(target=self.loopcheck)
            #self.t2.isAlive()
            try:
                self.username = self.e1.get()
                print(self.oauth_token)
                self.quality = (str(dd1.get()).lower())
                print(self.quality)
                #self.root_path = change_root_path()
                print(self.root_path)
                #self.loopcheck()
            finally:
                print(self.t2.is_alive())
                #self.t2.__init__()
                if self.t2.is_alive() is True:
                    self.t2.__init__(self)
                    print("alive")
                    self.loopcheck()
                else:
                    self.t2.start()

        def exitprog():
            os.kill(os.getpid(), signal.CTRL_C_EVENT)
            #os.kill(self.pid, signal.CTRL_C_EVENT)


        qualities = ["Best", "High", "Medium", "Low", "Mobile", "Audio"]

        oneFrame = Frame(root)
        oneFrame.pack()
        l1 = Label(oneFrame, text="Streamer Username")
        #l1.grid(row=0,column=0, sticky="e")
        l1.pack(side="left")

        self.e1 = Entry(oneFrame)
        #self.e1.grid(row=0, column=1)
        self.e1.pack(side="right")

        twoFrame = Frame(root)
        twoFrame.pack()

        l2 = Label(twoFrame, text="Quality")
        #l2.grid(row=2, column=0, sticky="e")
        l2.pack(side=LEFT)

        dd1 = ttk.Combobox(twoFrame, values=qualities, state="readonly")
        dd1.current(0)
        #dd1.grid(row=2, column=1)
        dd1.pack(side=RIGHT)

        fourFrame = Frame(root)
        fourFrame.pack(side=TOP)

        l3 = Label(fourFrame, text="Save Folder")
        l3.pack(side=LEFT)

        b3 = Button(fourFrame, text="Change", command=change_root_path)
        b3.pack(side=LEFT)

        e2 = Entry(fourFrame)
        e2.pack()
        e2.config(state=NORMAL)
        e2.delete(0, END)
        e2.insert(0, self.root_path)
        e2.config(state="readonly")

        self.threeFrame = Frame(root)
        self.threeFrame.pack(side=BOTTOM)

        b2 = Button(self.threeFrame, text="Authorize", command=authorize)
        #b2.grid(row=3, column=0)
        b2.pack(side=LEFT)

        b4 = Button(self.threeFrame, text="Exit", command=exitprog)
        b4.pack(side=RIGHT)

        b1 = Button(self.threeFrame, text="Start", command=set_params)
        #b1.grid(row=3, column=1)
        b1.pack(side=LEFT)
        root.mainloop()

        #def cont():
        #    self.loopcheck()



    def check_user(self):
        # 0: online,
        # 1: offline,
        # 2: not found,
        # 3: error
        url = 'https://api.twitch.tv/kraken/streams/' + self.username
        url2 = 'https://api.twitch.tv/kraken/channels/' + self.username
        info = None
        status = 3
        if self.username == "":
            self.sbar.config(text="Process Stopped")
            status = 4
            return status

        try:
            r = requests.get(url, headers = {"Client-ID" : self.client_id}, timeout=15)
            #print(r)
            r2 = requests.get(url2, headers = {"Client-ID" : self.client_id}, timeout=15)
            #print(r2)
            r.raise_for_status()
            info = r.json()
            #print(str(info))
            r2.raise_for_status()
            info2 = r2.json()
            #print(str(info2))
            if info['stream'] is None:
                countdown = self.refresh
                self.sbar.config(text="Checking")
                time.sleep(.25)
                self.sbar.config(text="Checking.")
                time.sleep(.25)
                self.sbar.config(text="Checking..")
                time.sleep(.25)
                self.sbar.config(text="Checking...")
                time.sleep(.25)
                while countdown != 0 and status != 4:
                    if self.username != self.e1.get():
                        self.username = ""
                        #self.t2.__init__()
                        self.check_user()
                        # tempname = self.e1.get()
                        # if self.e1.get() != tempname:
                        #     time.sleep(5)
                        # else:
                        #     #self.sbar.config(text="Changing Username")
                        #     self.sbar.config(text=("Username changed, checking for {} in {} seconds".format(self.e1.get(), countdown)))
                        #     time.sleep(1)
                        #     countdown -= 1
                    else:
                        self.sbar.config(text=("{} is currently offline, checking again in {} seconds".format(self.username, countdown)))
                        time.sleep(1)
                        countdown -= 1
                        status = 1
                #self.username = self.e1.get()
                #countdown = self.refresh
                #while countdown != 0:
                #    self.sbar.config(text=(self.username + "is currently offline, checking again in", countdown, "seconds."))
                #    time.sleep(1)
                #    countdown -= 1

                #root.update_idletasks()
                #status = 1
            else:
                status = 0
        except requests.exceptions.RequestException as e:
            if e.response.reason == 'Not Found' or e.response.reason == 'Unprocessable Entity':
                    status = 2
                    self.sbar.config(text="Invalid username or typo.")
                    return

        print(status)

        return status, info

    def loopcheck(self):
        while True:
            status, info = self.check_user()
            if status == 2:
                self.sbar.config(text="Username not found. Invalid username or typo.")


            elif status == 3:
                self.sbar.config(text=(datetime.datetime.now().strftime("%Hh%Mm%Ss")," ","unexpected error. will try again in 5 minutes."))
                time.sleep(300)

            if status == 4:
                self.sbar.config(text="Username not found. Invalid username or typo.")

            elif status == 1:
                print("got to loopcheck")

            elif status == 0:
                def stopsub():
                    os.kill(pid, signal.CTRL_BREAK_EVENT)
                    #os.kill()
                    #status = 4
                    self.username = ""
                    self.check_user()
                self.sbar.config(text=(self.username, "online. Stream recording in session."))
                self.recorded_path = os.path.join(self.root_path, "recorded", self.username)
                filename = self.username + " - " + datetime.datetime.now().strftime("%Y-%m-%d %Hh%Mm%Ss") + " - " + (info['stream']).get("channel").get("status") + ".mp4"

                # clean filename from unecessary characters
                filename = "".join(x for x in filename if x.isalnum() or x in [" ", "-", "_", "."])

                recorded_filename = os.path.join(self.recorded_path, filename)

                # start streamlink process
                sp = subprocess.Popen(["streamlink", "--twitch-oauth-token", self.oauth_token, "twitch.tv/" + self.username, self.quality, "-o", recorded_filename], shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                pid = sp.pid
                print(pid)
                b5 = Button(self.threeFrame, text="Stop", command=stopsub)
                b5.pack(side=RIGHT)
                sp.wait()
                # if sp.returncode == 2:
                #     root.destroy()
                #     self.__init__()



                # subprocess.run(sp)

                self.sbar.config(text="Recording stream is done. Fixing video file.")
                if(os.path.exists(recorded_filename) is True):
                    try:
                        subprocess.call([self.ffmpeg_path, '-err_detect', 'ignore_err', '-i', recorded_filename, '-c', 'copy', os.path.join(self.processed_path, filename)])
                        os.remove(recorded_filename)
                    except Exception as e:
                        self.sbar.config(text=e)
                else:
                    self.sbar.config(text="Skip fixing. File not found.")
                self.sbar.config(text="Fixing is done. Going back to checking..")
                self.run()

    def run(self):
        # path to recorded stream
        self.recorded_path = os.path.join(self.root_path, "recorded", self.username)
        print(self.recorded_path)

        # path to finished video, errors removed
        self.processed_path = os.path.join(self.root_path, "processed", self.username)

        # create directory for recordedPath and processedPath if not exist
        if(os.path.isdir(self.recorded_path) is False):
            os.makedirs(self.recorded_path)
        if(os.path.isdir(self.processed_path) is False):
            os.makedirs(self.processed_path)

        # make sure the interval to check user availability is not less than 15 seconds
        if(self.refresh < 15):
            self.sbar.config(text="Check interval should not be lower than 15 seconds.")
            self.refresh = 15
            self.sbar.config(text="System set check interval to 15 seconds.")

        # fix videos from previous recording session
        try:
            video_list = [f for f in os.listdir(self.recorded_path) if os.path.isfile(os.path.join(self.recorded_path, f))]
            if(len(video_list) > 0):
                self.sbar.config(text='Fixing previously recorded files.')
            for f in video_list:
                recorded_filename = os.path.join(self.recorded_path, f)
                self.sbar.config(text=('Fixing ' + recorded_filename + '.'))
                try:
                    subprocess.call([self.ffmpeg_path, '-err_detect', 'ignore_err', '-i', recorded_filename, '-c', 'copy', os.path.join(self.processed_path,f)])
                    os.remove(recorded_filename)
                except Exception as e:
                    self.sbar.config(text=e)
        except Exception as e:
            self.sbar.config(text=e)

        self.sbar.config(text=("Checking for", self.username, "every", self.refresh, "seconds. Record with", self.quality, "quality."))
        self.loopcheck()

def main(argv):
    twitch_recorder = TwitchRecorder()
    usage_message = 'twitch-recorder.py -u <username> -q <quality>'

    try:
        opts, args = getopt.getopt(argv,"hu:q:",["username=","quality="])
    except getopt.GetoptError:
        print (usage_message)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            TwitchRecorder.sbar.config(text=usage_message)
            sys.exit()
        elif opt in ("-u", "--username"):
            twitch_recorder.username = arg
        elif opt in ("-q", "--quality"):
            twitch_recorder.quality = arg

    twitch_recorder.run()

if __name__ == "__main__":
    main(sys.argv[1:])
