import tkinter as tk
from tkinter import ttk, messagebox
from decryption import FileDecryptor
from file_tracker import FileTracker

class AdminPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f2f5")
        self.pack(fill=tk.BOTH, expand=True)
        
        self.decryptor = FileDecryptor()
        self.tracker = FileTracker()
        self.admin_password = "admin123"  # secure password
        
        self._create_widgets()
        self._load_file_list()
    
    def _create_widgets(self):
        # Header
        header = tk.Frame(self, bg="#e74c3c", height=80)
        header.pack(fill=tk.X)
        tk.Label(header, text="👨‍💻 Admin Dashboard", font=('Arial', 18), 
                bg="#e74c3c", fg="white").pack(side=tk.LEFT, padx=20)
        
        # Main Content
        content = tk.Frame(self, bg="#f0f2f5", padx=20, pady=20)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Admin Password Entry
        admin_frame = tk.Frame(content, bg="#f0f2f5")
        admin_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(admin_frame, text="Admin Password:", bg="#f0f2f5").pack(side=tk.LEFT)
        self.admin_pwd_entry = tk.Entry(admin_frame, show="*")
        self.admin_pwd_entry.pack(side=tk.LEFT, padx=5)
        
        # Files Table
        tk.Label(content, text="All Encrypted Files", font=('Arial', 12), 
                bg="#f0f2f5").pack(pady=(0,10), anchor=tk.W)
        
        self.tree = ttk.Treeview(content, columns=("name", "date", "path"), show="headings")
        
        self.tree.heading("name", text="Original Name")
        self.tree.heading("date", text="Encryption Date")
        self.tree.heading("path", text="Storage Path")
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Action Buttons
        btn_frame = tk.Frame(content, bg="#f0f2f5")
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="Decrypt Selected", 
                 command=self._decrypt_selected, bg="#27ae60", fg="white").pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Refresh List", 
                 command=self._load_file_list, bg="#3498db", fg="white").pack(side=tk.LEFT, padx=5)
    
    def _load_file_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        files = self.tracker.get_all_files()
        for file in files:
            self.tree.insert("", "end", values=(
                file['original_name'],
                file['encryption_date'],
                file['encrypted_path']
            ))
    
    def _decrypt_selected(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a file first!")
            return
        
        admin_pwd = self.admin_pwd_entry.get()
        if admin_pwd != self.admin_password:
            messagebox.showerror("Error", "Incorrect admin password!")
            return
        
        item = self.tree.item(selected)
        file_info = {
            'original_name': item['values'][0],
            'encrypted_path': item['values'][2]
        }
        
        # Ask for user password
        from tkinter import simpledialog
        user_password = simpledialog.askstring("Password", 
                                            f"Enter user password to decrypt {file_info['original_name']}:", 
                                            show='*')
        
        if user_password:
            try:
                decrypted_path = self.decryptor.decrypt_file(
                    encrypted_path=file_info['encrypted_path'],
                    password=user_password
                )
                messagebox.showinfo("Success", 
                                  f"File decrypted successfully!\nSaved to: {decrypted_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Decryption failed: {str(e)}")