import tkinter as tk
from tkinter import ttk
from gui.user_panel import UserPanel
from gui.admin_panel import AdminPanel
from admin_auth import AdminAuth
import os

class MainDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure File System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f2f5")
        
        # Initialize auth system
        self.auth = AdminAuth()
        if not self.auth.is_admin_configured():
            self._setup_admin()
        
        self._create_sidebar()
        self._create_main_content()
    
    def _setup_admin(self):
        from tkinter import simpledialog
        password = simpledialog.askstring("Admin Setup", "Set admin password:", show='*')
        if password:
            confirm = simpledialog.askstring("Admin Setup", "Confirm password:", show='*')
            if password == confirm:
                self.auth.setup_admin(password)
                tk.messagebox.showinfo("Success", "Admin account created!")
            else:
                tk.messagebox.showerror("Error", "Passwords don't match!")
                self.root.destroy()
    
    def _create_sidebar(self):
        # Sidebar Frame
        sidebar = tk.Frame(self.root, bg="#2c3e50", width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Logo
        tk.Label(sidebar, text="🔒 SecureFile", bg="#2c3e50", fg="white", 
                font=('Arial', 18, 'bold'), pady=20).pack()
        
        # Navigation Buttons
        buttons = [
            ("📤 User Panel", self._show_user_panel),
            ("👨‍💻 Admin Panel", self._show_admin_panel),
            ("ℹ️ About", self._show_about),
            ("🚪 Exit", self.root.quit)
        ]
        
        for text, command in buttons:
            btn = tk.Button(sidebar, text=text, bg="#34495e", fg="white", 
                          font=('Arial', 12), bd=0, padx=20, pady=10,
                          command=command)
            btn.pack(fill=tk.X, padx=10, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#3d566e"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#34495e"))
    
    def _create_main_content(self):
        # Main Content Frame
        self.main_content = tk.Frame(self.root, bg="#f0f2f5")
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Default view
        self._show_welcome()
    
    def _show_welcome(self):
        self._clear_main_content()
        tk.Label(self.main_content, text="Welcome to SecureFile System", 
                font=('Arial', 24), bg="#f0f2f5").pack(pady=50)
        
        # Stats Frame
        stats_frame = tk.Frame(self.main_content, bg="white", padx=20, pady=20)
        stats_frame.pack(pady=20, padx=50, fill=tk.X)
        
        stats = [
            ("📁 Encrypted Files", "8"),
            ("🔑 Keys Generated", "8"),
            ("👥 Active Users", "2")
        ]
        
        for text, value in stats:
            frame = tk.Frame(stats_frame, bg="white")
            frame.pack(side=tk.LEFT, expand=True)
            tk.Label(frame, text=value, font=('Arial', 24), bg="white").pack()
            tk.Label(frame, text=text, font=('Arial', 12), bg="white").pack()
    
    def _show_user_panel(self):
        self._clear_main_content()
        UserPanel(self.main_content)
    
    def _show_admin_panel(self):
        if self.auth.authenticate_admin():
            self._clear_main_content()
            AdminPanel(self.main_content)
    
    def _show_about(self):
        self._clear_main_content()
        tk.Label(self.main_content, text="About SecureFile System", 
                font=('Arial', 20), bg="#f0f2f5").pack(pady=20)
        
        about_text = """
        SecureFile System - Version 1.0
        
        Features:
        - AES-256 File Encryption
        - User/Admin Roles
        - Password Protection
        - Secure Key Management
        
        Developed by Mah Noor
        """
        tk.Label(self.main_content, text=about_text, 
                font=('Arial', 12), bg="#f0f2f5", justify=tk.LEFT).pack()
    
    def _clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    # Initialize required directories
    os.makedirs("encrypted_files", exist_ok=True)
    os.makedirs("decrypted_files", exist_ok=True)
    os.makedirs("keys", exist_ok=True)
    os.makedirs("metadata", exist_ok=True)
    
    root = tk.Tk()
    app = MainDashboard(root)
    root.mainloop()