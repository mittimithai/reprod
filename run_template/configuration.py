import os
import threading
import time
import signal

#vm configuration
vmName = "ransomwareVm"
username = "ransomware"
password = "helloworld"
snapshotName = "Snapshot1"
cmdPath = "C:\Windows\System32\cmd.exe"
procmonPath = f"C:\\Users\\{username}\\Downloads\\ProcessMonitor\\Procmon.exe"
ProcmonfilterFilePath = f"C:\\Users\\{username}\\Downloads\\ProcessMonitor\\spade.reporter.ProcMon.pmc"
ransomwareDownloadPath = f"C:\\Users\\{username}\\Downloads"
BazaarApiKey = "82ea76c5b51d6e9ea0b08dba6a18771e"
logSavingPathVm = "E:\\"
densityscoutPath = "E:\\densityscout_build_45_windows\\win64\\densityscout.exe"
densitySavingPath = "E:\\"
folderForDensity = f"C:\\Users\\{username}\\Desktop"
vmStartTime = 70
vmClosingTime = 5
logsDumpVdiPathVm = "F:\\"

#host configuration
# env_var_name = "REPROD_MAIN"
run_dir = os.path.dirname(__file__)
current_folder = run_dir.split('\\')[-1]

reprod_dir = os.path.dirname(run_dir)
main_folder = reprod_dir.split('\\')[-1]

secondaryVdiPath = f"{reprod_dir}\\vm_logsDump.vdi"
ransomwareExecTime = 600
ransomwareExtension = "exe"
hashFilePath = f"{run_dir}" #remove this
hashFileName = f"{current_folder}_hashes_{ransomwareExtension}.txt"
runs = 200

sreenshotsPath = f"{run_dir}\\screenshots"
zipPath = f"{reprod_dir}\\7-Zip\\7z.exe"
hostName = "phdlab"
procmonPathHost = f"{reprod_dir}\\ProcessMonitor\\Procmon64"
ProcmonfilterFilePathHost = f"{reprod_dir}\\ProcessMonitor\\spade.reporter.ProcMon.pmc"
pmlPath = f"{run_dir}\\logs"
pmlDonePath = f"{run_dir}\\pmlDone"
xmlPath = f"{run_dir}\\xmls"
density_path = f"{run_dir}\\density"
file_ops_path = f"{run_dir}\\file_ops" 
summary_csv_file_path = f"{run_dir}\\summary.csv"

# sampleDensityPath = f"{run_dir}\\sampleDensity.txt" 

csvPopulatePath = f"{reprod_dir}\\csv_populate.py" 
vmAutomationPath = f"{reprod_dir}\\vmAutomation.py"
extractXmlPath = f"{reprod_dir}\\extractXML.py"
procmonTimeout = 1200

#spadeVm Configuration
spadeVmName = "spadeVm"
spadeVmUsername = "spades"
spadeVmPass = "helloworld"
spadeVmStartTime = 30
spadeVmSnapshot = "Snapshot1"
spadeVmCloseTime = 5
# changes these two as well
getFileOperationsPath = f"/media/sf_{main_folder}/getFileOperations.py"
sharedFolderPath = f"{reprod_dir}"

print(run_dir, reprod_dir)