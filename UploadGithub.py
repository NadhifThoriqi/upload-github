from tkinter import simpledialog
import subprocess, json, os, time, tkinter as tk

config_file = "assets/github_config.json"

def add_config(project_path: str, isi):
    window = tk.Tk()
    window.withdraw()
    repo_url = simpledialog.askstring("Konfigurasi Baru", 
            "Masukkan URL repository GitHub (contoh: https://github.com/username/repo.git):", 
            parent=None)
    
    if not repo_url:
        return None

    branch = simpledialog.askstring("Konfigurasi Baru", 
            "Masukkan nama branch (default: {'main'}):", 
            initialvalue="main", 
            parent=None) or "main"
    
    config = {"repo_url": repo_url, "branch": branch}
    isi.update({project_path: config})
    with open(config_file, "w") as f:
        json.dump(isi, f, indent=4)
    return config
    
def cek_config():
    with open(config_file, 'r') as x:
        return json.load(x)

def load_config(project_path:str):
    file = cek_config()
    if project_path in file:
        return {"repo_url": file[project_path]["repo_url"], "branch": file[project_path]["branch"]}
    else: return add_config(project_path, file)

def run_command(command, cwd=None, output: str|bytes|None=None, get_output: bool|None=False):
    """Jalankan perintah terminal dan tampilkan output-nya"""
    output(f"\n👉 Menjalankan: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True, cwd=cwd)
    if result.returncode != 0:
        output("❌ Terjadi kesalahan:\n", result.stderr)
    else:
        output(result.stdout)
    if get_output: return result.stdout 

def upload_to_github(project_path: str, commit_message: str, output: bytes):
    output("=== 🚀 Program Upload ke GitHub ===\n")
    
    # 1️⃣ Minta lokasi folder proyek
    if not os.path.exists(project_path):
        output("❌ Folder tidak ditemukan. Pastikan path sudah benar!")
        return

    # 2️⃣ Pindahkan ke folder proyek
    output(f"📂 Mengakses folder: {project_path}")
    time.sleep(1)

    config = load_config(project_path)
    repo_url = config["repo_url"]
    branch = config["branch"]

    # 3️⃣ Pastikan ada git repo
    if not os.path.exists(os.path.join(project_path)):
        output("⚙️  Menginisialisasi repository Git baru...")
        run_command("git init", cwd=project_path, output=output)
        run_command(f"git remote add origin {repo_url}", cwd=project_path, output=output)

    # 4️⃣ Tambahkan semua file, commit, dan push
    output("\n📦 Menambahkan file ke Git...")
    run_command("git add .", cwd=project_path, output=output)

    output("\n📝 Melakukan commit...")
    run_command(f'git commit -m "{commit_message}"', cwd=project_path, output=output)

    output(f"\n🌐 Mengunggah ke GitHub branch '{branch}'...")
    run_command(f"git push -u origin {branch}", cwd=project_path, output=output)

    output("\n✅ Selesai! Program telah diunggah ke GitHub.")