import os
import psutil
import subprocess
import shutil
import time
import winshell

def check_disk_usage():
    """Check disk usage and clean temp files if usage is above 80%"""
    usage = psutil.disk_usage('/')
    print(f"Disk usage: {usage.percent}%")
    if usage.percent > 80:
        print("Disk usage is high!")
        clean_temp_files()

def find_locking_process(file_path):
    """Find the process that is locking the specified file."""
    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        if proc.info['open_files'] is not None:
            for f in proc.info['open_files']:
                if f.path == file_path:
                    print(f"File {file_path} is locked by process {proc.info['name']} (PID: {proc.info['pid']})")

def clean_temp_files():
    """Clean temp files"""
    temp_dirs = [
        'C:/Windows/Temp/',
        f'C:/Users/{os.getlogin()}/AppData/Local/Temp/',
        f'C:/Users/{os.getlogin()}/AppData/Local/Microsoft/Windows/INetCache/',
        f'C:/Users/{os.getlogin()}/AppData/Local/Microsoft/Edge/User Data/Default/Cache/',
        f'C:/Users/{os.getlogin()}/AppData/Local/Google/Chrome/User Data/Default/Cache/',
    ]
   
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            print(f"Cleaning files in {temp_dir}")
            for file_name in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file_name)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
                    find_locking_process(file_path)  # Find the process that is locking the file

def empty_recycle_bin():
    """Empty the recycle bin"""
    print("Emptying recycle bin...")
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
        print("Recycle bin emptied successfully.")
    except Exception as e:
        print(f"Failed to empty recycle bin: {e}")

def check_cpu_usage():
    """Check CPU usage"""
    usage = psutil.cpu_percent(interval=1)
    print(f"CPU usage: {usage}%")

def check_memory_usage():
    """Check memory usage"""
    usage = psutil.virtual_memory().percent
    print(f"Memory usage: {usage}%")
    if usage > 80:
        print("Memory usage is high!")

def check_high_usage_programs():
    """Check for any high usage programs"""
    high_cpu_usage = []
    high_memory_usage = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        if proc.info['cpu_percent'] > 50:  # or any threshold you want
            high_cpu_usage.append(proc.info)
        if proc.info['memory_percent'] > 50:  # or any threshold you want
            high_memory_usage.append(proc.info)

    if high_cpu_usage:
        print("These processes are using a high amount of CPU:")
        for proc in high_cpu_usage:
            print(f"{proc['name']} (PID: {proc['pid']}) - {proc['cpu_percent']}%")

    if high_memory_usage:
        print("These processes are using a high amount of memory:")
        for proc in high_memory_usage:
            print(f"{proc['name']} (PID: {proc['pid']}) - {proc['memory_percent']}%")

def check_startup_programs():
    """Check startup programs"""
    print("Checking startup programs...")
    with open('temp.txt', 'w') as f:
        subprocess.call('wmic startup list full', shell=True, stdout=f)

    with open('temp.txt', 'r', encoding='utf-16') as f:
        startup_programs = f.read()

    print(startup_programs)

def update_software():
    """Update software"""
    print("Updating software...")
    subprocess.run('choco upgrade all -y', shell=True)

def defrag_disk():
    """Defrag disk"""
    print("Defragging disk...")
    subprocess.run('defrag C: /U /V', shell=True)

def monitor_pc():
    """Monitor PC status and perform cleanup"""
    while True:
        print("Checking PC status...")
        check_disk_usage()
        check_cpu_usage()
        check_memory_usage()
        check_high_usage_programs()  # check for high usage programs
        check_startup_programs()
        update_software()
        defrag_disk()
        empty_recycle_bin()  # This is where you empty the recycle bin
        time.sleep(60 * 60 * 24)  # wait for 24 hours

if __name__ == "__main__":
    monitor_pc()