import random
import os
import time
import platform
import subprocess


# This function opens a random program from the computer
def open_text_editor_and_start_typing():
    os_name = platform.system()
    if(os_name) == "MacOS":
        subprocess.run(TextEdit.app)

def open_random_program():
    # Get the name of the operating system
    os_name = platform.system()

    # Check the operating system and open a program accordingly
    if os_name == "Windows":
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
    elif os_name == "Darwin":
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
    elif os_name == "Linux":
        # Get a list of all the programs on the computer
        programs = [f for f in os.listdir("/usr/bin") if os.access(f, os.X_OK)]
        
        # Select a random program from the list
        program = random.choice(programs)
        print(type(program))
        # Open the program
        subprocess.run(program)

    elif os_name == "MacOS":
        # Get a list of all the programs on the computer
        programs = [f for f in os.path.join(home_dir, "Applications") if f.endswith(".app")]

        # Select a random program from the list
        program = random.choice(programs)
        print(type(program))
        # Open the program
        subprocess.run(program)


# Main function
if __name__ == "__main__":
    # Run the program in an infinite loop
    open_text_editor_and_start_typing()
    while True:
        # Open the random program at a random time
        time.sleep(random.randint(1, 10))
        open_random_program()