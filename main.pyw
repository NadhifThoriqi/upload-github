from tkinter import ttk, messagebox, filedialog
from UploadGithub import upload_to_github, load_config
import tkinter as tk

# init 
Window = tk.Tk()
Window.title("🚀 Upload Otomatis ke GitHub")
Window.iconbitmap(bitmap="logo.ico")
Window.geometry("400x500")
# Window.configure(bg="black")

# Variable dan Fungsi
MAINVAR = tk.StringVar()
MASSAGEVAR = tk.StringVar(value="update otomatis")

def cari_folder():
    folder = filedialog.askdirectory()
    if folder: return MAINVAR.set(folder)

def input_main(frame):
    """Untuk input"""
    path_frame = tk.LabelFrame(frame, text="⚙️ Detail Proyek", padx=10, pady=10)
    path_frame.pack(fill='x', pady=5)
    
    # halaman direktori
    ttk.Label(path_frame, text="Path Folder Proyek:", anchor="w").grid(row=0, column=0, sticky="w", pady=5, padx=5)
    direktori = ttk.Entry(path_frame, textvariable=MAINVAR, width=50)
    direktori.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
    tk.Button(path_frame, text="Pilih Folder", command=cari_folder).grid(row=0, column=2, sticky="e", pady=5, padx=5)

    # halaman pesan
    tk.Label(path_frame, text="Pesan Commit:", anchor="w").grid(row=1, column=0, sticky="w", pady=5, padx=5)
    tk.Entry(path_frame, textvariable=MASSAGEVAR, width=50).grid(row=1, column=1, columnspan=2, sticky="ew", pady=5, padx=5)
    
    # Konfigurasi grid
    path_frame.grid_columnconfigure(1, weight=1)


def log_main(frame): 
    """Untuk menampilkan log proses"""
    log_frame = tk.LabelFrame(frame, text="🗒️ Log Proses", padx=5, pady=5)
    log_frame.pack(fill='both', expand=True, pady=5)
        
    global log_text
    log_text = tk.Text(log_frame, height=15, state='disabled', wrap='word', bg='#f0f0f0')
    log_text.pack(side="left", fill="both", expand=True)
        
    scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
    scrollbar.pack(side="right", fill="y")
    log_text.config(yscrollcommand=scrollbar.set)

def log_output(message, *messages: str | list[str] | tuple[str, ...]):
    """Menambahkan pesan ke area log dan menggulir ke bawah."""
    log_text.config(state='normal')
    log_text.insert(tk.END, message + "\n", messages)
    log_text.see(tk.END) # Scroll ke bawah
    log_text.config(state='disabled')
    Window.update_idletasks() # Memaksa update GUI

def start_upload(): 
    path=MAINVAR.get().strip()
    projek=MASSAGEVAR.get().strip() or "update otomatis"
    # messagebox.showinfo(f"👋 Halo, {path}!",f"Ip anda: {ip.address()}")

    # Validasi input
    if not path:
        messagebox.showerror("Error", "Path folder proyek tidak boleh kosong.")
        return

    # Reset log dan disable tombol
    log_text.config(state='normal')
    log_text.delete(1.0, tk.END)
    log_text.config(state='disabled')
    upload_button.config(state='disabled', text="⏳ Sedang Berjalan...")

    # Jalankan logika upload
    log_output("=== 🚀 Memulai Upload ke GitHub ===\n")
    try:
        success = upload_to_github(path, projek, log_output)
        if success:
            messagebox.showinfo("Sukses", "Program telah berhasil diunggah ke GitHub!")
        else:
            messagebox.showerror("Gagal", "Upload Gagal. Periksa log proses untuk detail.")
    except Exception as e:
        log_output(f"\nFATAL ERROR: {e}")
        messagebox.showerror("Error Fatal", f"Terjadi kesalahan tak terduga: {e}")
    finally:
        # Re-enable tombol
        upload_button.config(state='normal', text="✅ Mulai Upload")


# Frame Input
main_frame = ttk.Frame(Window)
main_frame.pack(padx=10, pady=10, fill="both", expand=True)

input_main(main_frame)
log_main(main_frame)

# Tombol Upload
upload_button = tk.Button(main_frame, text="✅ Mulai Upload", command=start_upload, height=2, bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'))
upload_button.pack(fill='x', pady=(10, 0))

# Main loop
Window.mainloop()