import sys
import os
import subprocess

def main():
    try:
        with open("requirements.txt", "r") as requirements_file:
            requirements = requirements_file.read()
    except FileNotFoundError:
        print("Error: requirements.txt not found.")
        sys.exit(1)

    check_requirements = subprocess.run(["python", "scripts/check_requirements.py", "requirements.txt"], capture_output=True)

    if check_requirements.returncode == 1:
        print("Installing missing packages...")
        install_packages = subprocess.run(["pip", "install", "-r", "requirements.txt"], capture_output=True)
        if install_packages.returncode != 0:
            print("Error: Failed to install packages.")
            sys.exit(1)

    run_cli = subprocess.run(["python", "-m", "cli"], capture_output=True)
    if run_cli.returncode != 0:
        print("Error: Failed to run CLI.")
        sys.exit(1)

    input("Press any key to continue...")

if __name__ == "__main__":
    main()