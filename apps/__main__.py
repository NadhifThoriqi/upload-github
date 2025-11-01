from app import main
import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME="github_configs.json"
config = os.path.join(BASE_DIR, "resources", FILE_NAME)

def file_json():
    if not os.path.exists(config):
        os.makedirs(os.path.dirname(config), exist_ok=True) # Pastikan folder ada
        default_data = {
            "directory": {
                "repo_url": "",
                "branch": ""
            }
        }
        with open(config, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    file_json()
    x=main()
    x.mainloop()
