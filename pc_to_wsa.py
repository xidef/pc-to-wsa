import os
import tkinter as tk
from tkinter import messagebox

try:
    from tkinter.filedialog import askopenfilename, askdirectory
except ImportError:
    os.system("pip install tkinter")
    from tkinter.filedialog import askopenfilename, askdirectory


# crea una finestra
window = tk.Tk()


def copy_to_device():
    os.system(f"adb disconnect")
    os.system(f"adb connect 127.0.0.1:58526")

    # seleziona il file da copiare dal computer al dispositivo
    file_path = askopenfilename()
    if not file_path:
        return

    # rinomina il file se contiene spazi nel nome
    old_file_path = os.path.abspath(file_path)
    old_file_name = os.path.basename(old_file_path)
    if " " in old_file_name:
        new_file_name = old_file_name.replace(' ', '_')
        new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name)

        os.rename(old_file_path, new_file_path)
        file_path = new_file_path

    # copia il file sul dispositivo
    os.system(f"adb push {file_path} /storage/emulated/0/")

    result = os.popen("adb shell ls /storage/emulated/0/").read()

    if os.path.basename(file_path).lower() in result.lower():
        messagebox.showinfo("Successo", "Il file è stato copiato sul dispositivo.")
    else:
        messagebox.showerror("Errore", "Si è verificato un errore durante la copia del file sul dispositivo.")


def copy_to_computer():
    os.system(f"adb disconnect")
    os.system(f"adb connect 127.0.0.1:58526")

    # seleziona la cartella di destinazione sul PC
    dest_dir = askdirectory()
    if not dest_dir:
        return

    # ottiene la lista dei file sul dispositivo
    result = os.popen("adb shell ls /storage/emulated/0/").read()
    file_list = result.split()

    # crea un pulsante per ogni file nella lista
    for file_name in file_list:
        def copy_file(selected_file=file_name):
            os.system(f"adb pull /storage/emulated/0/{selected_file} {dest_dir}")
            messagebox.showinfo("Successo", f"Il file '{selected_file}' è stato copiato sul PC.")
            window.quit()

        file_button = tk.Button(window, text=file_name, command=copy_file)
        file_button.pack()


def on_start():
    # chiede all'utente se vuole copiare dal computer al dispositivo o viceversa
    file2_button = tk.Button(window, text="copy to coputer", command=copy_to_computer)
    file2_button.pack()
    
    file3_button = tk.Button(window, text="copy to device", command=copy_to_device)
    file3_button.pack()



# crea un pulsante per avviare l'operazione di copia
start_button = tk.Button(window, text="Inizia", command=on_start)
start_button.pack()

# avvia il loop principale della finestra
window.mainloop()
