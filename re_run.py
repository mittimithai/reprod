import sys
import shutil
import os
import pandas as pd
import importlib.util
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('folder_to_be_cloned', type=str, help= "name of folder to be cloned")
parser.add_argument('cloned_folder', type=str, help= "name you want to give the cloned folder")
parser.add_argument('query', help = '''If \'SIMPLE_CLONE\' provided, this file will simply clone the folder and the test file of hashes will contain the same hashes as the original folder.
                                        If \'RETRY_FAILED_PML\' provided, this would clone the folder and include only those hashes that has failed PMLs in the original folder.
                                        Or one could provide a query that follows the rules for DataFrame of the Pandas library and is a valid query based on \"summary.csv\", created after running vmAutomation.py for the main folder.
                                    ''')
args = parser.parse_args()
folder_name = args.folder_to_be_cloned
cloned_folder = args.cloned_folder
query = args.query

# importing configuration as config from the folder specified by user 
# folder_name = sys.argv[1]
folder_path = os.path.join(os.path.dirname(__file__), folder_name)
config_path = f"{folder_path}\\configuration.py"
module_name = f"{config_path}_config"
spec = importlib.util.spec_from_file_location(module_name, config_path)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

path = os.path.dirname(__file__)

# main_folder = os.getenv('REPROD_MAIN')
# print(os.listdir(main_folder))
# path_other = os.getcwd()

old_file = os.path.join(path, folder_name)
new_file = os.path.join(path, cloned_folder)
new_hash_name = f"{cloned_folder}_hashes_{config.ransomwareExtension}"


if query == "SIMPLE_CLONE":
    query = False
elif query == "RETRY_FAILED_PML":
    query ='failed_pml_extract == 1'


if os.path.exists(f"{new_file}"):
    print("a file with this name already exists, please choose another name")
else:
    os.mkdir(new_file)

        
    shutil.copy(f"{old_file}\\setup.py", f"{new_file}\\setup.py")
    shutil.copy(f"{old_file}\\configuration.py", f"{new_file}\\configuration.py")
    shutil.copy(f"{old_file}\\csv_populate.py", f"{new_file}\\csv_populate.py")
    
    df =  pd.read_csv(f"{old_file}\\summary.csv")
    
    if query:
       filtered_df = df.query(query)
    else:
        filtered_df = df.copy()
        
    my_list = filtered_df["sha256"].tolist()
    text = '\n'.join(my_list)
    with open(f"{new_file}\\{new_hash_name}.txt", "w") as f:
        f.write(text)
        
