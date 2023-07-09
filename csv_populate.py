import os
import subprocess
import csv
import argparse
import importlib.util

parser = argparse.ArgumentParser()
parser.add_argument('config_folder', help="name of folder that you want to create the csv for")
args = parser.parse_args()
folder_name = args.config_folder

folder_path = os.path.join(os.path.dirname(__file__), folder_name)
config_path = f"{folder_path}\\configuration.py"
module_name = f"{config_path}_config"
spec = importlib.util.spec_from_file_location(module_name, config_path)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

cols = ['SHA256', 'file_operations', 'delta_density', 'new_files', 'failed_pml_extract']
print(cols)
rows = [cols]

def getDeltaDensity(before, after):

    unchanged_entropy = {}
    changed_entropy = {}
    new_files = {}

    files_changed = False

    '''
    take only file name and make sure they are not same cuz this is in our control
    check number of files in original and dictionary to make sure there is no key duplication
    '''
    try:
        with open(before, 'r') as beforeDensityFile:
            beforeDensity = [each.strip() for each in beforeDensityFile.readlines()]
    except:
        beforeDensity = []

    try:
        with open(after, 'r', encoding='utf-8') as afterDensityFile:
            afterDensity = [each.strip() for each in afterDensityFile.readlines()]
    except:
        afterDensity = []

    for file in beforeDensity:
        density, filename = file.split("|")
        filename = filename.split(".")[0]
        unchanged_entropy[filename] = density

    for file in afterDensity:
        try:
            density, filename = file.split("|")
            filename = filename.split(".")[0]
        except:
            return 0, 0


        if filename not in unchanged_entropy.keys():
            new_files[filename] = density

        elif unchanged_entropy[filename] != density:
            changed_entropy[filename] = abs(float(density)-float(unchanged_entropy[filename]))
            files_changed = True

    if len(changed_entropy) == 0:
        delta_density = 0
    else:
        delta_density = max(changed_entropy.values())

    numberNewFiles = len(new_files.items())
    return delta_density, numberNewFiles

fileOpsFile = open (config.file_ops_path, "r")
fileOpsList = fileOpsFile.readlines()

f = open(f"{config.run_dir}\\vm_hashes_done_{config.ransomwareExtension}.txt", "r")
hashes_done = f.read().split('\n')

for line in fileOpsList:
    file_ops = line.split(" ")[0]
    ransomware = line.split(" ")[1].split("/")[-1].split(".")[0]
    before = f"{config.density_path}\\before\\{ransomware}_before.txt"
    after = f"{config.density_path}\\after\\{ransomware}_after.txt"
    deltaDensity, numberNewFiles = getDeltaDensity(before, after)
    print(ransomware, file_ops, deltaDensity, numberNewFiles)
    if ransomware in hashes_done:
        rows.append([ransomware, file_ops, deltaDensity, numberNewFiles, 0])
    else:
        rows.append([ransomware, file_ops, deltaDensity, numberNewFiles, 1])
fileOpsFile.close()

#open the file in the write mode
with open(config.summary_csv_file_path, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(rows)