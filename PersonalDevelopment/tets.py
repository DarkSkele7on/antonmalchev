import Tkinter as tk

def run_script():
    # Insert code to run your script here
    print("Running script...")

# Create the root window
root = tk.Tk()

# Create a button to run the script
run_button = tk.Button(root, text="Run script", command=run_script)
run_button.pack()

# Start the event loop
root.mainloop() 