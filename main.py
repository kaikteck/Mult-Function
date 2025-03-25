import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
import speedtest
from PIL import Image, ImageTk
import json

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Multi-Function App")
        self.geometry("1000x600")
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create sidebar
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Create main content area
        self.main_frame = MainFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Load saved data
        self.load_data()
    
    def load_data(self):
        try:
            with open('app_data.json', 'r') as f:
                data = json.load(f)
                self.main_frame.task_manager.tasks = data.get('tasks', [])
                self.main_frame.task_manager.update_task_list()
        except FileNotFoundError:
            pass

    def save_data(self):
        data = {
            'tasks': self.main_frame.task_manager.tasks
        }
        with open('app_data.json', 'w') as f:
            json.dump(data, f)

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=200)
        
        self.parent = parent
        
        # Create buttons
        buttons = [
            ("Task Manager", lambda: self.show_frame("tasks")),
            ("Video Player", lambda: self.show_frame("video")),
            ("Music Player", lambda: self.show_frame("music")),
            ("Speed Test", lambda: self.show_frame("speed"))
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ctk.CTkButton(self, text=text, command=command)
            btn.pack(pady=10, padx=20)
    
    def show_frame(self, frame_name):
        self.parent.main_frame.show_frame(frame_name)

class MainFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.frames = {}
        
        # Initialize all feature frames
        self.task_manager = TaskManager(self)
        self.video_player = VideoPlayer(self)
        self.music_player = MusicPlayer(self)
        self.speed_tester = SpeedTester(self)
        
        self.frames = {
            "tasks": self.task_manager,
            "video": self.video_player,
            "music": self.music_player,
            "speed": self.speed_tester
        }
        
        # Show initial frame
        self.show_frame("tasks")
    
    def show_frame(self, frame_name):
        # Hide all frames
        for frame in self.frames.values():
            frame.pack_forget()
        
        # Show selected frame
        self.frames[frame_name].pack(fill="both", expand=True)

class TaskManager(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.tasks = []
        
        # Create widgets
        self.task_entry = ctk.CTkEntry(self, placeholder_text="Enter new task...")
        self.task_entry.pack(pady=10, padx=20, fill="x")
        
        self.add_button = ctk.CTkButton(self, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)
        
        self.task_list = tk.Listbox(self, bg="#2b2b2b", fg="white", selectmode=tk.SINGLE)
        self.task_list.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.remove_button = ctk.CTkButton(self, text="Remove Selected", command=self.remove_task)
        self.remove_button.pack(pady=5)
        
        self.complete_all_button = ctk.CTkButton(self, text="Complete All", command=self.complete_all)
        self.complete_all_button.pack(pady=5)
    
    def add_task(self):
        task = self.task_entry.get()
        if task and len(self.tasks) < 7:
            self.tasks.append(task)
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
    
    def remove_task(self):
        selection = self.task_list.curselection()
        if selection:
            index = selection[0]
            self.tasks.pop(index)
            self.update_task_list()
    
    def complete_all(self):
        if len(self.tasks) == 7:
            self.tasks = []
            self.update_task_list()
    
    def update_task_list(self):
        self.task_list.delete(0, tk.END)
        for task in self.tasks:
            self.task_list.insert(tk.END, task)

class VideoPlayer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.videos = []
        
        # Create widgets
        self.add_button = ctk.CTkButton(self, text="+ Add Video", command=self.add_video)
        self.add_button.pack(pady=10)
        
        self.video_list = tk.Listbox(self, bg="#2b2b2b", fg="white")
        self.video_list.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.info_label = ctk.CTkLabel(self, text="Note: Video playback requires external media player")
        self.info_label.pack(pady=5)
    
    def add_video(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.avi *.mkv")]
        )
        if file_path:
            self.videos.append(file_path)
            self.video_list.insert(tk.END, os.path.basename(file_path))

class MusicPlayer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.playlist = []
        
        # Create widgets
        self.add_button = ctk.CTkButton(self, text="+ Add Music", command=self.add_music)
        self.add_button.pack(pady=10)
        
        self.playlist_box = tk.Listbox(self, bg="#2b2b2b", fg="white")
        self.playlist_box.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.info_label = ctk.CTkLabel(self, text="Note: Music playback requires external media player")
        self.info_label.pack(pady=5)
    
    def add_music(self):
        if len(self.playlist) < 10:
            file_path = filedialog.askopenfilename(
                filetypes=[("Audio files", "*.mp3 *.wav")]
            )
            if file_path:
                self.playlist.append(file_path)
                self.playlist_box.insert(tk.END, os.path.basename(file_path))

class SpeedTester(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.test_button = ctk.CTkButton(self, text="Start Speed Test", command=self.start_test)
        self.test_button.pack(pady=20)
        
        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack(pady=10)
    
    def start_test(self):
        self.test_button.configure(state="disabled")
        self.result_label.configure(text="Testing... Please wait.")
        self.update()
        
        try:
            st = speedtest.Speedtest()
            download = st.download() / 1_000_000  # Convert to Mbps
            upload = st.upload() / 1_000_000
            ping = st.results.ping
            
            if download < 1:
                download = (st.download() / 1_000)  # Convert to Kbps
                download_unit = "Kbps"
            else:
                download_unit = "Mbps"
            
            if upload < 1:
                upload = (st.upload() / 1_000)  # Convert to Kbps
                upload_unit = "Kbps"
            else:
                upload_unit = "Mbps"
            
            result_text = f"Download: {download:.2f} {download_unit}\n"
            result_text += f"Upload: {upload:.2f} {upload_unit}\n"
            result_text += f"Ping: {ping:.2f} ms"
            
            self.result_label.configure(text=result_text)
        except Exception as e:
            self.result_label.configure(text=f"Error: {str(e)}")
        finally:
            self.test_button.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()
