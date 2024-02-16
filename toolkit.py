import tkinter as tk
from tkinter import scrolledtext, Listbox, ttk, messagebox
import subprocess
import argparse
import psutil

#Theme Settings
dark_bg = "#333333"
light_text = "#FFFFFF"
dark_button_bg = "#555555"
dark_text_area_bg = "#444444"

root = tk.Tk()
root.title("LDPlayer CLI Toolkit")
root.configure(bg=dark_bg)

#Logging Settings
log_area = scrolledtext.ScrolledText(root, width=80, height=10, bg="black", fg="green", font="Consolas")
log_area.grid(column=0, row=3, columnspan=2, padx=10, pady=10, sticky="nsew")

def add_log_message(message):
    log_area.insert(tk.END, ">>>" + message + "\n")
    log_area.see(tk.END)  # Scroll to the end to see the latest log message
    

memory_label = tk.Label(root, text="Select a memory:", bg=dark_bg, fg=light_text)
memory_label.grid(column=1, row=0, pady=(5,170), padx=5, sticky='w')

memory_values = ['512', '1024', '2048', '4096', '8192',]
memory_combobox = ttk.Combobox(root, values=memory_values, state="readonly")
memory_combobox.grid(column=1, row=0, pady=(10,100), padx=10, sticky='we')
memory_combobox.set('4096')  #Default value


def create_parser():
    parser = argparse.ArgumentParser(description="LDPlayer CLI Toolkit")
    parser.add_argument('--list', action='store_true', help='List LDPlayer instances')
    return parser

def list_ldplayer_instances():
    command = "C:\\LDPlayer\\LDPlayer9\\ldconsole.exe list"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    log_message = "LDPlayer instances are listed."
    print(log_message)
    add_log_message(log_message)
    return ["LDPlayer-Pro Edt.", "LDPlayer-Main-1"]


def update_listbox():
    instances = list_ldplayer_instances()
    listbox.delete(0, tk.END)  
    for instance in instances:
        listbox.insert(tk.END, instance)
   
      
# Selected instances are processed
def process_selected_instances():
    selected_indices = listbox.curselection()
    selected_instances = [listbox.get(i) for i in selected_indices]
    log_message = "Selected instances:", selected_instances
    print(log_message)
    add_log_message(log_message)
    
def quit_all_instances():
    command = "C:\\LDPlayer\\LDPlayer9\\ldconsole.exe quitall"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()

    if process.returncode == 0:
        log_message = "All instances are closed."
        print(log_message)
        add_log_message(log_message)
    else:
        error_message = "Error!:", error
        print(error_message)
        add_log_message(error_message)
        
# Selected instance's memory is modified
def modify_instance_memory():
    selected_indices = listbox.curselection()
    if not selected_indices:
        log_message = "Please select an instance."
        print(log_message)
        add_log_message(log_message)
        return
    instance_name = listbox.get(selected_indices[0])
    new_memory_value = memory_combobox.get()
    command = f"C:\\LDPlayer\\LDPlayer9\\ldconsole.exe modify --name \"{instance_name}\" --memory {new_memory_value}"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    
    if process.returncode == 0:
        log_message = f"Memory for {instance_name} has been successfully set to {new_memory_value}M."
        print(log_message)
        add_log_message(log_message)
    else:
        error_message = "Error! " + error
        print(error_message)
        add_log_message(error_message)

# Update memory settings of LDPlayer instances according to system RAM
def adjust_instance_memory():
    total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)  # Convert bytes to GB
    # Determine the memory value according to the total RAM
    if total_ram_gb >= 16:
        memory_value = "4096"
        log_message = f"{memory_value} MB memory will be set for each instance."
        print(log_message)
        add_log_message(log_message)
    elif total_ram_gb >= 8:
        memory_value = "2048"
        log_message = f"{memory_value} MB memory will be set for each instance."
        print(log_message)
        add_log_message(log_message)
    else:
        memory_value = "1024"
        log_message = f"{memory_value} MB memory will be set for each instance."
        print(log_message)
        add_log_message(log_message)

    # Update the memory value for each instance
    instance_list = ["LDPlayer-Main-1", "LDPlayer-Pro Edt."]  # Replace with the actual instance names
    for instance_name in instance_list:
        subprocess.run(f"C:\\LDPlayer\\LDPlayer9\\ldconsole.exe modify --name {instance_name} --memory {memory_value}", check=True)
        
# Button to adjust memory settings of LDPlayer instances
def on_adjust_memory_button_click():
    adjust_instance_memory()
    log_message = "Memory settings have been adjusted according to the system RAM."
    print(log_message)
    add_log_message(log_message)

parser = create_parser()

listbox = Listbox(root, bg=dark_text_area_bg, fg=light_text, selectmode=tk.MULTIPLE)
listbox.grid(column=0, row=0, padx=10, pady=20, sticky="nsew")

list_button = tk.Button(root, text="List the instances", bg=dark_button_bg, fg=light_text, command=update_listbox)
list_button.grid(column=0, row=1, pady=10)

quit_button = tk.Button(root, text="Force Close All", bg=dark_button_bg, fg=light_text, command=quit_all_instances)
quit_button.grid(column=0, row=2, pady=10)

# Bellek değerini ayarla butonunu oluştur
modify_memory_button = tk.Button(root, text="Adjust the memory (RAM)", bg=dark_button_bg, fg=light_text, command=modify_instance_memory)
modify_memory_button.grid(column=1, row=0, pady=10, padx=10)

adjust_memory_button = tk.Button(root, text="Auto Adjust", command=on_adjust_memory_button_click)
adjust_memory_button.grid(column=1, row=0, pady=(100,10), padx=10)


root.mainloop()
