import random
import os
import time
import platform
import subprocess
import osascript

class Annoying:
    def __init__(self):
        self.os_name = platform.system()

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
    annoy.open_text_editor_and_start_typing()
    #while True:
        # Open the random program at a random time
        #time.sleep(random.randint(1, 10))
    #annoy.open_random_program()