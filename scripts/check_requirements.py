import sys
import pkg_resources

def main():
    # Read command line argument for the requirements file
    requirements_file = sys.argv[1]

    # Read the requirements file and extract package names
    with open(requirements_file, "r") as f:
        required_packages = [
            line.strip().split("#")[0].strip() for line in f.readlines()
        ]

    # Get the list of installed packages
    installed_packages = [package.key for package in pkg_resources.working_set]

    # Initialize a list to store missing packages
    missing_packages = []

    # Check if required packages are installed
    for package in required_packages:
        if not package:  # Skip empty lines
            continue
        package_name = package.strip().split("==")[0]
        if package_name.lower() not in installed_packages:
            missing_packages.append(package_name)

    # Print missing packages or a success message
    if missing_packages:
        print("Missing packages:")
        print(", ".join(missing_packages))
        sys.exit(1)
    else:
        print("All packages are installed.")


if __name__ == "__main__":
    main()