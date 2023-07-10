This repo contains the code that was used to generate the provenance data at:
[https://doi.org/10.5281/zenodo.7933806](https://doi.org/10.5281/zenodo.7933806)

Published in the CSET 2023: [https://doi.org/10.1145/3607505.3607510](https://doi.org/10.1145/3607505.3607510)

Broadly, the code can be used to download batches of malware samples from [MalwareBazaar](https://bazaar.abuse.ch/), run them in a windows virtual machine and extract procmon logs provided as  input to [SPADE](https://github.com/ashish-gehani/SPADE).  The code depends on two virtual machine images, the detailed instructions to create those images can be found in `virtual_machine_setup.txt`.

1. Ensure that VirtualBox binaries are in your path (this is done by default on most package manager installtions). This can be checked by running `vboxmanage` at the command line.
2. Download and unzip the [7zip](https://www.7-zip.org/) and [Process Monitor](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) folders in the root directory of this repo. Make sure the folders are named "7-Zip" and "ProcessMonitor".
3. Move the `spade.reporter.ProcMon.pmc` from repo folder to `ProcessMonitor` folder.
4. An initial folder, named `run_template`, is provided with `configuration.py` and a complete list of malware hashes from MalwareBazaar (as of time of writing). A list of malware SHA256 hashes from MalwareBazaar (this list can easily be obtained from [Malware Bazaar](https://bazaar.abuse.ch/export/#csv)).
4. Run `setup.py`, this will import the two virtual machine images (one for the windows malware sanbox and one for SPADE operations) into virtualbox (paths specified in `config.py`) and make snapshots of them. You will have to provide the name of the folder where you want to setup the directories in `config.py`.
5. Run `vmAutomation.py` to run the list of malware binaries inside the associated BMcollect logs, file-operations, densities, and screenshots for each hash in the previous step.
6. Run `make_summary` to generate a summary of the dataset.
7. To setup a new run based on the configuration of an existing run run `rerun.py` supplying the run folder that will act as teh template and the name of the new run as command line arguments.


# Requirements
Python version: 3.11.0

Windows malware sandbox virtual machine requirements:
Ram : 8gb
Processor : 1 core
Storage: 68gb

SPADE virtual machine requirments:
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
of a ransomware and add that data to the `summary.csv` file. It takes as argument the name of the folder for which you want to make the csv.

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
This file is individual to each folder created and contains the configuration for that particular run. If you change the name of any file, make sure to reflect that change in the respective `configuration.py`. For example the deafult way of naming hash files when creates is: `[FOLDER_NAME]_hashes_[RASNOMWARE_EXTENSION].txt`. If you chnage the name of these hash files, make sure to change it accordingly in the varaible 'hashFileName' in the relevant `configuration.py`. You would also have to change the name in variable 'new_hash_name' in `rerun.py`.
