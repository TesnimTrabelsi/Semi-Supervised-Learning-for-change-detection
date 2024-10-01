import os

def group_folders_by_longid(main_folder):
    # Dictionary to store the folders grouped by LongID
    folders_by_longid = {}

    # Iterate over the directories in the main folder
    for dir_name in os.listdir(main_folder):
        # Check if the directory name matches the expected pattern
        if not dir_name.startswith("sn7_train_labels"):
            continue

        # Extract the LongID from the directory name
        longid = dir_name.split("_")[3]

        # Add the directory to the list of folders with the same LongID
        if longid not in folders_by_longid:
            folders_by_longid[longid] = []
        folders_by_longid[longid].append(os.path.join(main_folder, dir_name))

    # Create subfolders for each LongID and move the corresponding folders to them
    for longid, folders in folders_by_longid.items():
        subfolder = os.path.join(main_folder, longid)
        os.makedirs(subfolder, exist_ok=True)
        for folder in folders:
            os.rename(folder, os.path.join(subfolder, os.path.basename(folder)))


if __name__ == '__main__':
    group_folders_by_longid("/home/antonimestre/Documents/Tesnime/SiameseSSL-master/SpaceNet7/sn7_train_labels")
