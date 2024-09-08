import webbrowser
import time
import subprocess
import sys
import os
import json
import pkg_resources

def check_and_install_node():
    try:
        # Check if node is in PATH
        subprocess.run(["node", "--version"], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["npm", "--version"], check=True, stdout=subprocess.DEVNULL)
        print("Node.js and npm are already installed.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Node.js or npm is not found in PATH. Checking common installation locations...")
        
        # Check common installation locations
        common_paths = [
            r"C:\Program Files\nodejs",
            r"C:\Program Files (x86)\nodejs",
            os.path.expanduser("~\\AppData\\Roaming\\npm"),
        ]
        
        for path in common_paths:
            node_path = os.path.join(path, "node.exe")
            npm_path = os.path.join(path, "npm.cmd")
            if os.path.exists(node_path) and os.path.exists(npm_path):
                print(f"Found Node.js installation at {path}")
                # Add to PATH temporarily
                os.environ["PATH"] = f"{path};{os.environ['PATH']}"
                return True
        
        print("Node.js installation not found. Please install Node.js manually.")
        print("1. Download Node.js from https://nodejs.org/")
        print("2. Run the installer and make sure to check the option to add Node.js to PATH during installation.")
        print("3. After installation, restart your command prompt or PowerShell.")
        print("4. Run this script again.")
        return False

def check_homebrew():
    try:
        subprocess.run(["brew", "--version"], check=True, stdout=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def install_homebrew():
    print("Homebrew is not installed. Installing...")
    homebrew_install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    subprocess.run(homebrew_install_cmd, shell=True, check=True)

def install_node_dependencies():
    print("Installing Node.js dependencies...")
    os.chdir('resume_upload')
    
    npm_path = get_npm_path()
    if npm_path and os.path.exists(npm_path):
        try:
            print(f"Using npm from: {npm_path}")
            if sys.platform.startswith('win'):
                result = subprocess.run(["cmd", "/c", npm_path, "install"], check=True, capture_output=True, text=True)
            else:
                result = subprocess.run([npm_path, "install"], check=True, capture_output=True, text=True)
            print("Node.js dependencies installed successfully.")
            print(f"npm output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing Node.js dependencies: {e}")
            print(f"Error output: {e.stderr}")
    else:
        print(f"npm not found at {npm_path}. Please ensure Node.js and npm are installed and added to PATH.")
    
    os.chdir('..')

def get_npm_path():
    try:
        if sys.platform.startswith('win'):
            npm_path = subprocess.check_output(["where", "npm.cmd"], universal_newlines=True).strip().split('\n')[0]
        else:
            npm_path = subprocess.check_output(["which", "npm"], universal_newlines=True).strip()
        return npm_path
    except subprocess.CalledProcessError:
        # If 'where' or 'which' fails, try to construct the path
        if sys.platform.startswith('win'):
            return os.path.join(os.environ.get('ProgramFiles', ''), 'nodejs', 'npm.cmd')
        else:
            return '/usr/local/bin/npm'

def install_python_dependencies():
    with open('resume_test_api/requirements.txt', 'r') as f:
        required_packages = f.read().splitlines()
    
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    
    for package in required_packages:
        package_name = package.split('==')[0]
        if package_name not in installed_packages:
            print(f"Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
        else:
            print(f"{package_name} is already installed.")

def main():
    print("Checking and installing dependencies...")
    if not check_and_install_node():
        print("Unable to proceed without Node.js. Exiting.")
        sys.exit(1)

    # Add this line to print the current PATH
    print(f"Current PATH: {os.environ['PATH']}")

    # Add this debug print
    npm_path = get_npm_path()
    print(f"npm path: {npm_path}")

    install_node_dependencies()
    install_python_dependencies()
    print("All dependencies are installed.")
    # Run the Python server
    print("Starting Python server...")
    python_process = subprocess.Popen([sys.executable, "resume_test_api/app.py"])
    
    # Run the Node.js server
    print("Starting Node.js server...")
    node_process = subprocess.Popen(["node", "resume_upload/server.js"])
    
    print("Both servers are running. Opening browser...")
    
    # Wait a bit for servers to start
    time.sleep(2)
    
    # Open the default browser
    webbrowser.open('http://localhost:3000')  # Adjust the port if needed
    
    print("Browser opened. Press Ctrl+C to stop servers.")
    
    try:
        # Wait for both processes to complete (which they won't unless stopped)
        python_process.wait()
        node_process.wait()
    except KeyboardInterrupt:
        print("\nStopping servers...")
        python_process.terminate()
        node_process.terminate()
        print("Servers stopped.")

if __name__ == "__main__":
    main()