import os
from pathlib import Path

def create_test_files(root_dir, folders, files_per_folder=3):
    # Ensure root directory exists
    root_path = Path(root_dir)
    root_path.mkdir(parents=True, exist_ok=True)

    for folder in folders:
        folder_path = root_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)

        # Create test files inside each folder
        for i in range(1, files_per_folder + 1):
            file_path = folder_path / f"file_{i}.txt"
            with open(file_path, "w") as f:
                f.write(f"This is test file {i} in {folder}\n")
            print(f"Created {file_path}")

if __name__ == "__main__":
    # Root directory where files will be created
    root_directory = os.path.expanduser("~")

    # List of subfolders
    folders = ["Desktop", "Documents", "Downloads", "Pictures", "Music", "Videos"]

    # Run the function
    create_test_files(root_directory, folders, files_per_folder=3)

    print("✅ All test files created successfully!")
