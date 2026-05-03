from django.core.management.utils import get_random_secret_key
import os
from pathlib import Path
import shutil

def main():
    secret_key = get_random_secret_key()
    
    env_path = Path.cwd() / ".env"
    
    if env_path.exists():
        print("既に .env ファイルが存在します。下記の内容を .env ファイルにコピーしてください。")
        content = open(".env.example", "r").read()
        content = content.replace("your-secret-key-here", secret_key)
        print(content)
        
    else:
        content = open(".env.example", "r").read()
        content = content.replace("your-secret-key-here", secret_key)
        env_path.write_text(content, encoding="utf-8")
        print(f".env ファイルが作成されました。\nsecret_key: '{secret_key}'")
    
if __name__ == "__main__":
    main()