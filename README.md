This repo contains the code that was used to generate the provenance data at:
DOI_FILLIN

Published the the CST'23 FILLIN

Broadly, the code can be used to download batches of malware samples from [MalwareBazaar](https://bazaar.abuse.ch/), run them in a windows virtual machine and extract procmon logs provided as  input to [SPADE](https://github.com/ashish-gehani/SPADE).  The code depends on two virtual machine images, the detailed instructions to create those images can be found in `virtual_machine_setup.txt`.

1. Set the path for VirtualBox in environment variables through the command "SET PATH=%PATH%;"path/to/virtualbox/directory"
2. Download and unzip the [7zip](https://www.7-zip.org/) and [Process Monitor](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) folders in the repo. Make sure the folders are named "7-Zip" and "ProcessMonitor"
3. Move the spade.reporter.ProcMon.pmc from repo folder to "ProcessMonitor" folder
4. run setup.py, this will import the two images into virtualbox (if the respective ovas are present in the repo) and make snapshots of them
5. use the supplied "vm_hashes_exe.txt" file, a list of malware sha256 hashes from MalwareBazaar (this can be easily updated using Malware Bazaar's csv download)
6. run vmAutomation.py to collect logs, file-operations, densities, and screenshots for each hash in the previous step
7. run csv_populate to generate a summary of the dataset


# Requirements
ransomeware vm requirments:
Ram : 8gb
Processor : 1 core
Storage: 68gb

spade vm requirments:
Ram : 32gb
Processor: 2 cores
Storage : 50gb

Note: To change the settings of any vm, first make the desired changes then delete the current snapshot and take a new snapshot with same name.

# vmAutomation.py
This script will read a new line delimeted list of sha256 hashes from the file "hashes_exe.txt", download the corresponding binary from MalwareBazaar,  run the binary in the ransomewareVm and log its activity using ProcMon and 
then extract the logs and densities of desktop files to log.txt and density folder respectively.
It will then take the pml log files from the folder logs and will convert them into xml format using ProcMon filter then runs the script getFileOperations.py

# getFileOperations.py
This script runs in spadeVm and take xml logs from the main folder which is also a shared folder between 
host and spadeVm. The script then runs bash script file_ops.sh within the spadeVm which uses SPADE to
calculate the file operations done by the ransomware.

# csv_populate.py
This script extracts the maximum density changed from densities, number of new files, and file operations
of a ransomware and add that data to the summary.csv file

# SHA256 Collection
A full_sha256.txt file can be downloaded from [Malwarebazaar](https://bazaar.abuse.ch/export/). 
HashesSort.py is the script which will query each SHA256 from malwarebazaar and get metadata in response.
SHA256 will be filtered according to the ransomware tag and sorted according to the binary extension.
