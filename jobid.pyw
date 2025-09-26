import os,sqlite3,shutil,requests,pyperclip,threading,tkinter as tk

class RobloxPresence:
    def __init__(self):
        self.r=tk.Tk();self.r.title("Roblox Presence Tracker");self.r.geometry("500x600");self.r.minsize(400,500)
        self.bg="#0f0f0f";self.card="#1a1a1a";self.accent="#ff4757";self.acch="#ff6b7d"
        self.txt="#fff";self.txt2="#b0b0b0";self.success="#4cd137";self.warn="#ffa502"
        self.r.configure(bg=self.bg)
        self.cookie=None;self.user=None;self.place=None;self.job=None
        self.frame=tk.Frame(self.r,bg=self.bg);self.frame.pack(fill="both",expand=True,padx=15,pady=15)
        self.name=tk.Label(self.frame,text="Loading...",font=("Segoe UI",18,"bold"),fg=self.txt,bg=self.card);self.name.pack(pady=(20,5))
        self.userlbl=tk.Label(self.frame,text="@username",font=("Segoe UI",12),fg=self.txt2,bg=self.card);self.userlbl.pack(pady=(0,20))
        self.status=tk.Label(self.frame,text="Checking presence...",font=("Segoe UI",11),fg=self.txt,bg=self.card,justify="left",wraplength=450);self.status.pack(fill="x",pady=(0,20))
        self.btns=tk.Frame(self.frame,bg=self.card);self.btns.pack(fill="both",expand=True)
        self.buttons=[("Copy Job ID",self.copy_job_id,"📋"),("Copy Place ID",self.copy_place_id,"🏗️"),
                      ("Copy Join Script",self.copy_join_script,"📝"),("Copy Join Link",self.copy_join_link,"🔗"),
                      ("Refresh",self.refresh,"🔄")]
        for t,c,i in self.buttons:self.make_btn(self.btns,t,c,i)
        self.r.bind("<Configure>",lambda e:self.rescale_widgets())
        threading.Thread(target=self.load_data,daemon=True).start()

    def make_btn(self,p,t,c,i):
        f=tk.Frame(p,bg=self.card);f.pack(fill="x",pady=5)
        b=tk.Frame(f,bg=self.accent,highlightthickness=0);b.pack(fill="x")
        l=tk.Label(b,text=f"{i}  {t}",font=("Segoe UI",11,"bold"),fg=self.txt,bg=self.accent,cursor="hand2");l.pack(padx=5,pady=8)
        def on_enter(e): b.config(bg=self.acch,highlightbackground="#fff",highlightthickness=2)
        def on_leave(e): b.config(bg=self.accent,highlightthickness=0)
        l.bind("<Enter>",on_enter);l.bind("<Leave>",on_leave);l.bind("<Button-1>",lambda e,c=c:c())

    def get_chrome(self):
        try: import win32crypt
        except: return None
        p=[os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\Cookies"),
           os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data\Default\Cookies")]
        for path in p:
            if os.path.exists(path):
                cpy=path+"_cpy";shutil.copy2(path,cpy);conn=sqlite3.connect(cpy);cur=conn.cursor()
                cur.execute("SELECT name,encrypted_value FROM cookies WHERE host_key LIKE '%roblox.com%'")
                for n,v in cur.fetchall():
                    if n==".ROBLOSECURITY":r=win32crypt.CryptUnprotectData(v,None,None,None,0)[1];conn.close();os.remove(cpy);return r.decode()
                conn.close();os.remove(cpy)
        return None

    def get_firefox(self):
        p=os.path.expanduser(r"~\AppData\Roaming\Mozilla\Firefox\Profiles")
        if not os.path.exists(p):return None
        for prof in os.listdir(p):
            db=os.path.join(p,prof,"cookies.sqlite")
            if os.path.exists(db):
                cpy=db+"_cpy";shutil.copy2(db,cpy);conn=sqlite3.connect(cpy);cur=conn.cursor()
                cur.execute("SELECT name,value FROM moz_cookies WHERE host LIKE '%roblox.com%'")
                for n,v in cur.fetchall(): 
                    if n==".ROBLOSECURITY":conn.close();os.remove(cpy);return v
                conn.close();os.remove(cpy)
        return None

    def load_data(self):
        self.cookie=self.get_chrome() or self.get_firefox()
        if not self.cookie:return self.status.config(text="❌ Cookie not found",fg=self.accent)
        headers={"Cookie":f".ROBLOSECURITY={self.cookie}","User-Agent":"RobloxJobIdFetcher"}
        try:
            u=requests.get("https://users.roblox.com/v1/users/authenticated",headers=headers).json();self.user=u
            self.r.after(0,lambda:self.name.config(text=u["displayName"]))
            self.r.after(0,lambda:self.userlbl.config(text=f"@{u['name']}"))
            p=requests.post("https://presence.roblox.com/v1/presence/users",headers=headers,json={"userIds":[u["id"]]}).json()["userPresences"][0]
            if p["placeId"]==0:self.r.after(0,lambda:self.status.config(text="⚠️ Not in game",fg=self.warn))
            else:self.place,self.job=p["placeId"],p["gameId"];self.r.after(0,lambda:self.status.config(
                text=f"✅ In game\nPlace ID: {self.place}\nJob ID: {self.job[:8]}...",fg=self.success
            ))
            self.r.after(5000,lambda:threading.Thread(target=self.load_data,daemon=True).start())
        except Exception as e:self.r.after(0,lambda:self.status.config(text=f"❌ Error: {e}",fg=self.accent))

    def copy_job_id(self):pyperclip.copy(self.job) if self.job else None
    def copy_place_id(self):pyperclip.copy(str(self.place)) if self.place else None
    def copy_join_script(self):
        if self.place and self.job:pyperclip.copy(f'local placeid={self.place}\nlocal jobid="{self.job}"\ngame:GetService("TeleportService"):TeleportToPlaceInstance(placeid,jobid)')
    def copy_join_link(self):
        if self.place and self.job:pyperclip.copy(f"https://www.roblox.com/games/{self.place}?jobId={self.job}")
    def refresh(self):self.status.config(text="Refreshing...",fg=self.txt2);threading.Thread(target=self.load_data,daemon=True).start()
    def rescale_widgets(self):self.status.config(wraplength=self.r.winfo_width()-50)
    def run(self):self.r.mainloop()

if __name__=="__main__":RobloxPresence().run()
