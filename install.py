import os
import subprocess
import sys

def create_virtual_environment():
    """Creates a Python virtual environment."""
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    print("Virtual environment created successfully.")

def activate_virtual_environment():
    """Activates the virtual environment."""
    if os.name == 'nt':  # For Windows
        activate_script = os.path.join("venv", "Scripts", "activate")
    else:  # For Linux/Mac
        activate_script = os.path.join("venv", "bin", "activate")
    
    print(f"To activate the virtual environment, run: source {activate_script}")

def install_requirements():
    """Installs the dependencies listed in requirements.txt."""
    subprocess.run([os.path.join("venv", "bin", "pip"), "install", "--no-cache-dir", "-r", "requirements.txt"], check=True)
    print("Dependencies installed successfully.")

def main():
    create_virtual_environment()
    activate_virtual_environment()
    install_requirements()

if __name__ == "__main__":
    main()
