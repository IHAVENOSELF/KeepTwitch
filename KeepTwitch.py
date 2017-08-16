import datetime
import getopt
import os
import signal
import subprocess
import threading
import time
import tkinter.filedialog
from configparser import ConfigParser as config
from tkinter import *
from tkinter import ttk
import requests
import webview
from ttkthemes import themed_tk as tk

root = tk.ThemedTk()

root.wm_title("KeepTwitch")
root.set_theme("arc")
root.configure(background="#F5F6F7")
root.geometry("400x150")
root.resizable(False, False)

try:
    file = open("config.ini", "x+")
except FileExistsError:
    file = open("config.ini", "r+")


class TwitchRecorder:
    sbar = ttk.Label(root, text="Starting...", relief=SUNKEN, anchor=CENTER)
    sbar.pack(side=BOTTOM, fill=X)

    def __init__(self):

        self.conf = config(allow_no_value=True)
        self.conf.optionxform = str
        self.conf.read(file.name)
        # file.close()
        if self.conf.has_section("settings") is False:

            self.conf.set("DEFAULT", "username", "")
            self.conf.set("DEFAULT", "auth_token", "")
            self.conf.set("DEFAULT", "save_dir", str("{}\\Videos\\Twitch".format(os.path.expanduser("~"))))
            self.conf.set("DEFAULT", "refresh", "15")

            self.conf.set("DEFAULT", "quality", "0")  # 0=best 1=high 2=medium 3=low 4=mobile 5=audio
            self.conf.add_section("settings")
            file.close()
        else:
            file.close()


        def authorize():
            def get_current_url():
                time.sleep(1)
                while 1:
                    time.sleep(3)
                    if webview._initialized is True:
                        try:
                            token1 = (webview.get_current_url().split("="))
                            token1 = (str(token1[1]))[:30]
                            self.oauth_token = token1
                            if len(self.oauth_token) != 30:
                                time.sleep(1)
                                continue
                            webview.destroy_window()
                            b2.config(state=DISABLED, text="Authenticated")
                            self.sbar.config(text="Authenticated")
                            # print(len(self.oauth_token))
                        except AttributeError:
                            # print("caught")
                            time.sleep(1)

                    else:
                        continue

            if __name__ == '__main__':
                t = threading.Thread(target=get_current_url)
                t.start()

            webview.create_window("Authenticate",
                                  "https://api.twitch.tv/kraken/oauth2/authorize/?response_type=token&client_id=pwkzresl8kj2rdj6g7bvxl9ys1wly3j&redirect_uri=https%3A%2F%2Fstreamlink.github.io%2Ftwitch_oauth.html&scope=user_read+user_subscriptions",
                                  resizable=False, width=350, height=530)

        def change_root_path():
            self.root_path = os.path.normpath(tkinter.filedialog.askdirectory(title="Choose Folder", parent=root))

            e2.config(state=NORMAL)
            e2.delete(0, END)
            e2.insert(0, (str(self.root_path)))
            e2.config(state="readonly")

        def set_params():
            try:
                self.username = self.e1.get()

                self.quality = (str(dd1.get()).lower().replace(" ", "_"))

            finally:
                if self.t2.is_alive() is True:
                    self.t2.__init__(self)

                    self.loopcheck()
                elif self.threadstopped == 1:

                    threading.Thread(target=self.loopcheck).start()
                else:
                    threading.Thread(target=self.loopcheck).start()

        def exitprog():

            with open("config.ini", "w+") as file2:
                self.conf.set("settings", "username", str(self.e1.get()))
                self.conf.set("settings", "auth_token", str(self.oauth_token))
                self.conf.set("settings", "quality", str(dd1.current()))
                self.conf.set("settings", "save_dir", str(self.root_path))

                self.conf.write(file2)
                file2.close()
            os.kill(os.getpid(), signal.CTRL_C_EVENT)

        # tkinter.messagebox.showinfo("Before Start", "Choose a save folder and authorize with Twitch")
        self.root_path = self.conf.get("settings", "save_dir")

        self.sbar.config(text="Save Folder Set")

        # global configuration
        self.client_id = "jzkbprff40iqj646a697cyrvl0zt2m6"  # don't change this
        # get oauth token value by typing `streamlink --twitch-oauth-authenticate` in terminal
        self.ffmpeg_path = 'H:\Programs\Streamlink\ffmpeg\ffmpeg.exe'
        self.refresh = int(self.conf.get("settings", "refresh"))

        # user configuration
        self.username = self.conf.get("settings", "username")
        self.oauth_token = self.conf.get("settings", "auth_token")

        self.t2 = threading.Thread(target=self.loopcheck)
        self.threadstopped = 0


        root.protocol("WM_DELETE_WINDOW", exitprog)

        qualities = ["Best", "720p", "480p", "360p", "160p", "Audio Only"]


        oneFrame = ttk.Frame(root)
        oneFrame.pack(fill=X, padx=(10, 10), pady=(4, 2))

        l1 = ttk.Label(oneFrame, text="Streamer Username")
        l1.pack(side="left")

        self.e1 = ttk.Entry(oneFrame)
        self.e1.config()
        self.e1.pack(side="right", anchor=E)
        self.e1.insert(0, self.username)

        twoFrame = ttk.Frame(root)
        twoFrame.pack(fill=X, padx=(10, 10), pady=(2, 2))

        l2 = ttk.Label(twoFrame, text="Quality")
        l2.pack(side=LEFT, anchor=W)

        dd1 = ttk.Combobox(twoFrame, values=qualities, state="readonly")
        dd1.current(self.conf.get("settings", "quality"))
        dd1.pack(side=RIGHT)

        fourFrame = ttk.Frame(root)
        fourFrame.pack(side=TOP, fill=X, padx=(10, 10), pady=(2, 2))

        l3 = ttk.Label(fourFrame, text="Save Folder")
        l3.pack(side=LEFT, anchor=W)

        b3 = ttk.Button(fourFrame, text="Change", command=change_root_path)
        b3.pack(side=LEFT)

        e2 = ttk.Entry(fourFrame)
        e2.pack(anchor=E)
        e2.config(state=NORMAL)
        e2.delete(0, END)
        e2.insert(0, self.root_path)
        e2.config(state="readonly")

        self.threeFrame = ttk.Frame(root)
        self.threeFrame.pack(side=BOTTOM, padx=(10, 10), pady=(2, 2))

        b2 = ttk.Button(self.threeFrame, text="Authenticate", command=authorize)
        b2.pack(side=LEFT)
        if self.oauth_token is not "":
            url3 = "https://api.twitch.tv/kraken?oauth_token={}".format(self.oauth_token)
            r3 = requests.get(url3, headers={"Client-ID": self.client_id}, timeout=15)
            info3 = r3.json()
            info4 = str(info3).split("'")[25]
            if "'scopes': ['user_read', 'user_subscriptions']" in str(info3):
                b2.config(state=DISABLED, text="Authenticated")
                self.sbar.config(text="Authenticated")
            else:
                self.sbar.config(text="Auth token expired. Click Authenticate")

        b4 = ttk.Button(self.threeFrame, text="Exit", command=exitprog)
        b4.pack(side=RIGHT)

        b1 = ttk.Button(self.threeFrame, text="Start", command=set_params)
        b1.pack(side=LEFT)

        self.e1.focus_force()
        root.mainloop()

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
            r = requests.get(url, headers={"Client-ID": self.client_id}, timeout=15)
            r2 = requests.get(url2, headers={"Client-ID": self.client_id}, timeout=15)
            r.raise_for_status()
            info = r.json()
            r2.raise_for_status()
            info2 = r2.json()
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
                        self.check_user()
                    else:
                        self.sbar.config(text=(
                        "{} is currently offline, checking again in {} seconds".format(self.username, countdown)))
                        time.sleep(1)
                        countdown -= 1
                        status = 1
            else:
                status = 0
        except requests.exceptions.RequestException as e:
            if e.response.reason == 'Not Found' or e.response.reason == 'Unprocessable Entity':
                status = 2
                self.sbar.config(text="{} not found. Invalid username or typo.".format(self.username))
                return status

        print(status)

        return status, info

    def loopcheck(self):
        status, info = self.check_user()
        while True:
            # status, info = self.check_user()
            if status == 2:
                self.sbar.config(text="{} not found. Invalid username or typo.".format(self.username))


            elif status == 3:
                self.sbar.config(text=(
                datetime.datetime.now().strftime("%Hh%Mm%Ss"), " ", "unexpected error. will try again in 5 minutes."))
                time.sleep(300)

            if status == 4:
                self.sbar.config(text="{} not found. Invalid username or typo.".format(self.username))

            elif status == 1:
                print("got to loopcheck")

            elif status == 0:
                def stopsub():
                    os.kill(pid, signal.CTRL_BREAK_EVENT)
                    self.username = ""
                    self.check_user()
                    self.threadstopped = 1
                    b5.destroy()
                    root.wm_title("KeepTwitch")

                def printcli():
                    print("made it")
                    while True:
                        out = sp.stderr.read(80)
                        if out == b'' and sp.poll() is None:
                            break
                        if out != b'':
                            print(out)
                            out = str(out)
                            written = out.split(".mp4] ")
                            written = str(written[1]).strip("'").strip()
                            print(written)
                            self.sbar.config(text="Recording: {}".format(written))
                            # sys.stdout.write(str(out))
                            sys.stdout.flush()

                    # while 1:
                    #     for line in sp.stdout.readlines(1):
                    #         print(line)
                        # line = sp.stderr.readlines(1)
                        # print(line)
                        # print("fundest", sp.stdout.readlines(1))
                        # print("fundestin", sp.stdin.readlines())
                        # print("fundesterr", sp.stderr.readline())
                        # out = sp.stdout.read()
                        # print(out)
                        # time.sleep(1)
                        # sys.stdout.flush()

                self.sbar.config(text=("{} online. Stream recording in session.".format(self.username)))
                self.recorded_path = os.path.join(self.root_path, "recorded", self.username)
                filename = self.username + " - " + datetime.datetime.now().strftime("%Y-%m-%d %Hh%Mm%Ss") + " - " + (
                info['stream']).get("channel").get("status") + ".mp4"

                # clean filename from unecessary characters
                filename = "".join(x for x in filename if x.isalnum() or x in [" ", "-", "_", "."])

                recorded_filename = os.path.join(self.recorded_path, filename)

                # start streamlink process
                # sp = subprocess.Popen(
                #     ["streamlink", "--twitch-oauth-token", self.oauth_token, "twitch.tv/" + self.username, self.quality,
                #      "-o", recorded_filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                sp = subprocess.Popen(
                    ["streamlink", "--twitch-oauth-token", self.oauth_token, "twitch.tv/" + self.username, self.quality,
                     "-o", recorded_filename], stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

                pid = sp.pid
                print(pid)

                root.wm_title("KeepTwitch - Recording")

                b5 = ttk.Button(self.threeFrame, text="Stop", command=stopsub)
                b5.pack(side=RIGHT)

                printcli()

                sp.wait()

                self.sbar.config(text="Recording stream is done. Going back to checking")
                threading.Thread(self.run())

    def run(self):
        # path to recorded stream
        self.recorded_path = os.path.join(self.root_path, "recorded", self.username)
        print(self.recorded_path)

        # create directory for recordedPath and processedPath if not exist
        if (os.path.isdir(self.recorded_path) is False):
            os.makedirs(self.recorded_path)

        # make sure the interval to check user availability is not less than 15 seconds
        if (self.refresh < 15):
            self.sbar.config(text="Check interval should not be lower than 15 seconds.")
            self.refresh = 15
            self.sbar.config(text="System set check interval to 15 seconds.")

        print("funny")
        self.sbar.config(text=(
        "Checking for", self.username, "every", self.refresh, "seconds. Record with", self.quality, "quality."))
        self.loopcheck()


def main(argv):
    twitch_recorder = TwitchRecorder()
    usage_message = 'twitch-recorder.py -u <username> -q <quality>'

    try:
        opts, args = getopt.getopt(argv, "hu:q:", ["username=", "quality="])
    except getopt.GetoptError:
        print(usage_message)
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
