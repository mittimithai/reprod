import os
import configuration as config

if not os.path.exists(f"{config.density_path}\\after"):
    os.makedirs(f"{config.density_path}\\after")

if not os.path.exists(f"{config.density_path}\\before"):
    os.makedirs(f"{config.density_path}\\before")

if not os.path.exists(f"{config.current_directory}\\dotFiles"):
    os.makedirs(f"{config.current_directory}\\dotFiles")

if not os.path.exists(f"{config.pmlPath}"):
    os.makedirs(f"{config.pmlPath}")

if not os.path.exists(f"{config.pmlDonePath}"):
    os.makedirs(f"{config.pmlDonePath}")        

if not os.path.exists(f"{config.xmlPath}"):
    os.makedirs(f"{config.xmlPath}")

if not os.path.exists(f"{config.sreenshotsPath}"):
    os.makedirs(f"{config.sreenshotsPath}")

print("setup done")
