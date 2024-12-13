import tkinter as tk
from tkinter import filedialog, messagebox
import os
import hashlib
import shutil

class FileHasherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Hasher")
        self.root.geometry("600x150")

        # Source path
        self.source_label = tk.Label(root, text="Source Folder:")
        self.source_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        self.source_entry = tk.Entry(root, width=50)
        self.source_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.source_button = tk.Button(root, text="Browse", command=self.browse_source)
        self.source_button.grid(row=0, column=2, padx=5, pady=5)

        # Destination path
        self.dest_label = tk.Label(root, text="Output Folder:")
        self.dest_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        
        self.dest_entry = tk.Entry(root, width=50)
        self.dest_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.dest_button = tk.Button(root, text="Browse", command=self.browse_dest)
        self.dest_button.grid(row=1, column=2, padx=5, pady=5)

        # Process button
        self.process_button = tk.Button(root, text="Process Files", command=self.process_files)
        self.process_button.grid(row=2, column=1, pady=20)

    def browse_source(self):
        folder_path = filedialog.askdirectory()
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, folder_path)

    def browse_dest(self):
        folder_path = filedialog.askdirectory()
        self.dest_entry.delete(0, tk.END)
        self.dest_entry.insert(0, folder_path)

    def calculate_md5(self, filepath):
        md5_hash = hashlib.md5()
        with open(filepath, "rb") as f:
            # Read file in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()

    def process_files(self):
        source_path = self.source_entry.get()
        dest_path = self.dest_entry.get()

        if not source_path or not dest_path:
            messagebox.showerror("Error", "Please select both source and destination folders")
            return

        # Dictionary to store MD5 hashes
        processed_hashes = {}
        total_files = 0
        copied_files = 0

        # Walk through all files in source directory
        for root, _, files in os.walk(source_path):
            for file in files:
                total_files += 1
                file_path = os.path.join(root, file)
                
                try:
                    # Calculate MD5 hash
                    file_hash = self.calculate_md5(file_path)
                    
                    # Get file extension
                    _, file_extension = os.path.splitext(file)
                    
                    # If hash not already processed
                    if file_hash not in processed_hashes:
                        processed_hashes[file_hash] = file_path
                        new_filename = file_hash + file_extension
                        new_filepath = os.path.join(dest_path, new_filename)
                        
                        # Copy file with new name
                        shutil.copy2(file_path, new_filepath)
                        copied_files += 1
                
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")

        messagebox.showinfo("Complete", 
                          f"Processing complete!\nTotal files scanned: {total_files}\n"
                          f"Files copied: {copied_files}\n"
                          f"Duplicate files skipped: {total_files - copied_files}")

def main():
    root = tk.Tk()
    app = FileHasherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
