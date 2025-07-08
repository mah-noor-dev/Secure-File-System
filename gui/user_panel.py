import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from encryption import FileEncryptor
from file_tracker import FileTracker
from decryption import FileDecryptor 
import os

class UserPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f2f5")
        self.pack(fill=tk.BOTH, expand=True)
        
        self.encryptor = FileEncryptor()
        self.decryptor = FileDecryptor()
        self.tracker = FileTracker()
        
        self._create_widgets()
    
    def _create_widgets(self):
        # Header
        header = tk.Frame(self, bg="#3498db", height=80)
        header.pack(fill=tk.X)
        tk.Label(header, text="📤 User Dashboard", font=('Arial', 18), 
                bg="#3498db", fg="white").pack(side=tk.LEFT, padx=20)
        
        # Main Content
        content = tk.Frame(self, bg="#f0f2f5", padx=20, pady=20)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Upload Section
        upload_frame = tk.LabelFrame(content, text=" File Encryption ", 
                                   font=('Arial', 12), bg="white", padx=10, pady=10)
        upload_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(upload_frame, text="Select File to Encrypt", 
                 command=self._select_file, bg="#2ecc71", fg="white").pack(pady=10)
        
        self.file_label = tk.Label(upload_frame, text="No file selected", bg="white")
        self.file_label.pack()
        
        # Password Entry
        tk.Label(upload_frame, text="Encryption Password:", bg="white").pack(pady=(10,0))
        self.password_entry = tk.Entry(upload_frame, show="*")
        self.password_entry.pack(fill=tk.X, pady=5)
        
        tk.Button(upload_frame, text="Encrypt File", 
                 command=self._encrypt_file, bg="#2980b9", fg="white").pack(pady=10)
        
        # Decryption Section
        decrypt_frame = tk.LabelFrame(content, text=" File Decryption ", 
                                    font=('Arial', 12), bg="white", padx=10, pady=10)
        decrypt_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(decrypt_frame, text="Select Encrypted File", 
                 command=self._select_encrypted_file, bg="#e67e22", fg="white").pack(pady=10)
        
        self.encrypted_file_label = tk.Label(decrypt_frame, text="No file selected", bg="white")
        self.encrypted_file_label.pack()
        
        tk.Label(decrypt_frame, text="Decryption Password:", bg="white").pack(pady=(10,0))
        self.decrypt_password_entry = tk.Entry(decrypt_frame, show="*")
        self.decrypt_password_entry.pack(fill=tk.X, pady=5)
        
        tk.Button(decrypt_frame, text="Decrypt File", 
                 command=self._decrypt_file, bg="#d35400", fg="white").pack(pady=10)
        
        # Recent Files Table
        tk.Label(content, text="Recent Encrypted Files", font=('Arial', 12), 
                bg="#f0f2f5").pack(pady=(20,5), anchor=tk.W)
        
        columns = ("original_name", "encryption_date")
        self.tree = ttk.Treeview(content, columns=columns, show="headings")
        
        self.tree.heading("original_name", text="File Name")
        self.tree.heading("encryption_date", text="Encrypted On")
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Load recent files
        self._load_recent_files()
    
    def _select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_label.config(text=file_path)
    
    def _encrypt_file(self):
        file_path = self.file_label.cget("text")
        password = self.password_entry.get()
        
        if file_path == "No file selected":
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        if not password:
            messagebox.showerror("Error", "Please enter a password!")
            return
        
        try:
            encrypted_path, key_path = self.encryptor.encrypt_file(file_path, password)
            self.tracker.add_file_entry(
                original_name=os.path.basename(file_path),
                encrypted_path=encrypted_path,
                key_path=key_path
            )
            messagebox.showinfo("Success", f"File encrypted successfully!\nSaved to: {encrypted_path}")
            self._load_recent_files()
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")
    
    def _select_encrypted_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.encrypted_file_label.config(text=file_path)
    
    def _decrypt_file(self):
        file_path = self.encrypted_file_label.cget("text")
        password = self.decrypt_password_entry.get()
        
        if file_path == "No file selected":
            messagebox.showerror("Error", "Please select an encrypted file first!")
            return
        
        if not password:
            messagebox.showerror("Error", "Please enter a password!")
            return
        
        try:
            decrypted_path = self.decryptor.decrypt_file(file_path, password)  # Use decryptor instead of encryptor
            messagebox.showinfo("Success", f"File decrypted successfully!\nSaved to: {decrypted_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")
    
    def _load_recent_files(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        files = self.tracker.get_all_files()
        for file in files[-5:]:  # Show last 5 files
            self.tree.insert("", "end", values=(
                file['original_name'],
                file['encryption_date']
            ))