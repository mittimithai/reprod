import os
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

if not os.path.exists(f"{config.density_path}\\after"):
    os.makedirs(f"{config.density_path}\\after")

if not os.path.exists(f"{config.density_path}\\before"):
    os.makedirs(f"{config.density_path}\\before")

if not os.path.exists(f"{config.run_dir}\\dotFiles"):
    os.makedirs(f"{config.run_dir}\\dotFiles")

if not os.path.exists(f"{config.pmlPath}"):
    os.makedirs(f"{config.pmlPath}")

if not os.path.exists(f"{config.pmlDonePath}"):
    os.makedirs(f"{config.pmlDonePath}")        

if not os.path.exists(f"{config.xmlPath}"):
    os.makedirs(f"{config.xmlPath}")

if not os.path.exists(f"{config.sreenshotsPath}"):
    os.makedirs(f"{config.sreenshotsPath}")

print("setup done")
