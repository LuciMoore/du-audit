import os
import csv
import subprocess
import argparse
from datetime import datetime, timedelta, date
import pwd

def get_file_owner(file_path):
    try:
        # Get owner information using the pwd module (for Unix-like systems)
        owner_uid = os.stat(file_path).st_uid
        owner_name = pwd.getpwuid(owner_uid).pw_name
        return owner_name
        
    except Exception as e:
        print(f"Error getting owner: {e}")
        return None

def get_disk_usage(path):
    # Get the disk usage in bytes
    try:
        command = "du -s {}".format(path)
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            usage_in_kb = int(result.stdout.decode().split()[0])
            usage_in_gb = usage_in_kb / (1024 * 1024)  # Convert from KB to GB
            return round(usage_in_gb, 2)  # Return the usage in GB rounded to 2 decimal places
        else:
            return "Error: {}".format(result.stderr.decode().strip())
    except Exception as e:
        return str(e)  # Return an error message if there's an exception
    
def get_disk_usage(path):
    # Get the disk usage in bytes
    try:
        command = "du -s {}".format(path)
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            usage_in_kb = int(result.stdout.decode().split()[0])
            usage_in_gb = usage_in_kb / (1024 * 1024)  # Convert from KB to GB
            return round(usage_in_gb, 2)  # Return the usage in GB rounded to 2 decimal places
        else:
            return "Error: {}".format(result.stderr.decode().strip())
    except Exception as e:
        return str(e)  # Return an error message if there's an exception
    
def list_directories_and_disk_usage(folder_path, min_disk_usage_gb=50):
    # Initialize an empty list to store directory information
    directory_info = []

    min_days=50
    now = datetime.now()
    date_limit = datetime.timestamp(now - timedelta(days=min_days))

    err_file = os.path.join("disk_audit.err")

    # Walk through the directory tree and list all directories
    for root, dirs, _ in os.walk(folder_path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)

            try:
                creation_time = os.path.getctime(dir_path)

                #Only include folders that are greater than 3 years old
                if creation_time < date_limit:
                    disk_usage = get_disk_usage(dir_path)
                    formatted_creation_time = datetime.utcfromtimestamp(creation_time).strftime('%Y-%m-%d')
                    owner=get_file_owner(dir_path)
                    #access_time = os.path.getatime(dir_path)
                    #formatted_access_time = datetime.utcfromtimestamp(access_time).strftime('%Y-%m-%d')
                
                    # Check if disk usage is greater than or equal to the specified minimum
                    if float(disk_usage) >= min_disk_usage_gb:
                        directory_info.append((dir_path, disk_usage, formatted_creation_time, owner))
            except Exception as err:
                with open(err_file, "a+") as file:
                    file.write(f"{err}\n")

    return directory_info

def main():
    parser = argparse.ArgumentParser(description="Generate a CSV file listing directory paths and their disk usage in GB.")
    parser.add_argument("folder_path", help="The path to the folder to analyze")

    args = parser.parse_args()
    folder_path = args.folder_path

    # Check if the folder exists
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return

    # Generate the list of directories and their disk usage
    directory_info = list_directories_and_disk_usage(folder_path)

    # Define the CSV file name
    csv_file_name = "directory_disk_usage_olderthan50days_50GBthreshold.csv"

    # Write the information to a CSV file
    with open(csv_file_name, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Directory Path", "Disk Usage (GB)", "Date Created", "Owner"])
        for dir_path, disk_usage, formatted_creation_time, owner in directory_info:
            csv_writer.writerow([dir_path, disk_usage, formatted_creation_time, owner])

    print("CSV file '{}' has been generated with directory information.".format(csv_file_name))

if __name__ == "__main__":
    main()
