import os
import time

# --- CONFIGURATION ---
CSV_FILE = "echarge_whampoa_log.csv"
CHECK_INTERVAL = 60

def get_last_modified_time(filepath):
    """Returns the last modified time of a file."""
    try:
        return os.path.getmtime(filepath)
    except FileNotFoundError:
        return None

def push_to_github():
    """Pushes to GitHub using native system Git commands."""
    print("⚡ New data detected! Forcing push to GitHub...")
    
    # 1. Stage the file
    os.system(f'git add "{CSV_FILE}"')
    
    # 2. Commit the file
    os.system('git commit -m "Automated log update"')
    
    # 3. Push to GitHub main branch
    print("🔄 Uploading file via Git...")
    exit_code = os.system('git push origin main')
    
    if exit_code == 0:
        print("✅ Successfully pushed CSV to GitHub!")
    else:
        print(f"❌ Git push failed with exit code {exit_code}.")
    print("-" * 40)

def monitor_csv():
    print(f"👀 Monitoring '{CSV_FILE}' using native system Git...")
    print("Press Ctrl+C to stop.")
    print("-" * 40)
    
    last_known_mod_time = get_last_modified_time(CSV_FILE)
    
    while True:
        try:
            time.sleep(CHECK_INTERVAL)
            current_mod_time = get_last_modified_time(CSV_FILE)
            
            if current_mod_time and current_mod_time != last_known_mod_time:
                last_known_mod_time = current_mod_time
                push_to_github()
                
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped by user.")
            break
        except Exception as e:
            print(f"⚠️ Monitoring loop encountered an error: {e}")

if __name__ == "__main__":
    monitor_csv()
