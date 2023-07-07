This repo contains the code that was used to generate the provenance data at:
10.5281/zenodo.7933807

Published in the CSET 2023: DOI

Broadly, the code can be used to download batches of malware samples from [MalwareBazaar](https://bazaar.abuse.ch/), run them in a windows virtual machine and extract procmon logs provided as  input to [SPADE](https://github.com/ashish-gehani/SPADE).  The code depends on two virtual machine images, the detailed instructions to create those images can be found in `virtual_machine_setup.txt`.

1. Ensure that VirtualBox binaries are in your path (this is done by default on most package manager installtions). This can be checked by running `vboxmanage` at the command line.
2. Also, ensure that the main directory (named reprod-main) is an environment variable, as it is used in configuration.py. The variable in configuration.py that contains tha name of this environment variable is 'env_var_name' and the name stored by default is "REPROD_MAIN".
3. Download and unzip the [7zip](https://www.7-zip.org/) and [Process Monitor](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) folders in the root directory of this repo. Make sure the folders are named "7-Zip" and "ProcessMonitor"
4. Move the `spade.reporter.ProcMon.pmc` from repo folder to `ProcessMonitor` folder
5. run `setup.py`, this will import the two virtual machine image (one for the windows malware host and one for the SPADE host) that will run the malware binaries into virtualbox (paths specified in `config.py`) and make snapshots of them
6. use the supplied `vm_hashes_exe.txt` file, a list of malware sha256 hashes from MalwareBazaar (this list can easily be obtained from [Malware Bazaar](https://bazaar.abuse.ch/export/#csv))
7. run `vmAutomation.py` to run the list of malware binaries inside the associated BMcollect logs, file-operations, densities, and screenshots for each hash in the previous step
8. run `csv_populate` to generate a summary of the dataset
9. To rerun the project for a different set of malware binaries based on the summary of the dataset created, run `rerun.py`.


# Requirements
Python version: 3.?

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
This script will take as argumnent the name of the folder you want to run and read a new line delimeted list of sha256 hashes available in that folder, download the corresponding binary from MalwareBazaar, run the binary in the windows malware host and log its activity using ProcMon and then extract the logs and densities of desktop files to log.txt and density folder respectively. It will then take the pml log files from the folder logs and will convert them into xml format using ProcMon filter then runs the script `getFileOperations.py`.

# getFileOperations.py
This script runs in spadeVm and take xml logs from the main folder which is also a shared folder between 
host and spadeVm. The script then runs bash script `file_ops.sh` within the SPADE host which uses SPADE to
calculate the file operations done by the ransomware.

# csv_populate.py
This script extracts the maximum density changed from densities, number of new files, and file operations
of a ransomware and add that data to the `summary.csv` file.

# SHA256 Collection
A `full_sha256.txt` file can be downloaded from [Malwarebazaar](https://bazaar.abuse.ch/export/). 
HashesSort.py is the script which will query each SHA256 from malwarebazaar and get metadata in response.
SHA256 will be filtered according to the ransomware tag and sorted according to the binary extension.

# rerun.py
If one wishes to replicate the information, they can run the `rerun.py` file, which takes inputs as follow:

"folder_to_be_cloned": name of the folder which you want to clone, containing all files beforehand
"cloned_folder": the name you want to give the cloned folder
"query": this could either be:
 "SIMPLE_CLONE", which would simply clone the setup
 "RETRY_FAILED_PML", which would clone the folder but include only those hashes that had failed PMLs in the initial run
 or one could provide a query of its own that follows the rules for DataFrame of the Pandas library and is a valid query based on "summary.csv", created after running vmAutomation.py for a folder

# configuration.py
This file is individual to each folder crearted and contains the configuration for that particular run. If you change the name of any file, make sure to reflect that change in the respective `configuration.py`. For example the deafult way of naming hash files when creates is: `[FOLDER_NAME]_hashes_[RASNOMWARE_EXTENSION].txt`. If you chnage the name of these hash files, make sure to change it accordingly in the varaible 'hashFileName' in the relevant `configuration.py`. You would also have to change the name in variable 'new_hash_name' in `rerun.py`.
