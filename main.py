import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import configparser
import gettext

def execute_command(choice):
    if choice == _("Shut down"):
        os.system("sudo poweroff")
    elif choice == _("Reboot"):
        os.system("sudo reboot")
    elif choice == _("Log out"):
        os.system("loginctl terminate-user $USER")
    elif choice == _("Switch user / Lock screen"):
        os.system("loginctl lock-session")
    elif choice == _("Sleep mode"):
        os.system("echo -n mem | sudo tee /sys/power/state")

def show_description(event):
    choice = selected_option.get()
    if choice == _("Shut down"):
        description.set(_("Shutting down the computer."))
    elif choice == _("Reboot"):
        description.set(_("Rebooting the computer."))
    elif choice == _("Log out"):
        description.set(_("Logging out from the current session."))
    elif choice == _("Switch user / Lock screen"):
        description.set(_("Locking screen to switch user."))
    elif choice == _("Sleep mode"):
        description.set(_("Putting the computer to sleep."))
    adjust_window_size()

def adjust_window_size():
    main.update_idletasks()
    width = max(main.winfo_reqwidth(), 400)
    height = main.winfo_reqheight()
    main.geometry(f"{width}x{height}")
    center_window(main, width, height)

def show_help():
    messagebox.showinfo(_("HELP"), _("Select an action and click 'OK' to execute."))

def read_sysinfo():
    try:
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), "sysinfo.ini"))
        if "info" in config:
            distro_info.set(f'{config["info"]["distroname"]} {config["info"]["distrover"]}')
            de_info.set(f'{config["info"]["dename"]} {config["info"]["dever"]}')
            lang = config["info"].get("lang", "en")
            set_language(lang)
        else:
            distro_info.set(_("Unknown Distro"))
            de_info.set(_("Unknown DE"))
    except Exception as e:
        distro_info.set(_("Error reading file"))
        de_info.set(_("Error reading file"))

def set_language(lang):
    locale_dir = os.path.join(os.path.dirname(__file__), "locales")
    language = gettext.translation("messages", localedir=locale_dir, languages=[lang], fallback=True)
    language.install()
    global _
    _ = language.gettext

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f'{width}x{height}+{x}+{y}')

main = tk.Tk()

# Set default language to English
locale_dir = os.path.join(os.path.dirname(__file__), "locales")
language = gettext.translation("messages", localedir=locale_dir, languages=["en"], fallback=True)
language.install()
_ = language.gettext

distro_info = tk.StringVar()
de_info = tk.StringVar()

read_sysinfo()
main.title(_("Shut down Linux"))

main.geometry("400x250")  # Initial window size
main.resizable(False, False)  # Prevent user from resizing the window
center_window(main, 400, 250)

# Load images
computer_logo = tk.PhotoImage(file="computer_logo.png")
dist_logo = tk.PhotoImage(file="distro_logo.png")
de_logo = tk.PhotoImage(file="de_logo.png")

# Create a frame for logos and place it at the top
logo_frame = tk.Frame(main)
logo_frame.pack(pady=10)

dist_logo_label = tk.Label(logo_frame, image=dist_logo)
dist_logo_label.pack(side=tk.LEFT, padx=10)

de_logo_label = tk.Label(logo_frame, image=de_logo)
de_logo_label.pack(side=tk.LEFT, padx=10)

# Create a frame for "distroname distrover", "dename dever" strings to the right of the logos
info_frame = tk.Frame(logo_frame)
info_frame.pack(side=tk.RIGHT, padx=10)

distro_label = tk.Label(info_frame, textvariable=distro_info)
distro_label.pack()

de_label = tk.Label(info_frame, textvariable=de_info)
de_label.pack()

# "What should your computer do?" label above the menu
title_label = tk.Label(main, text=_("What should your computer do?"))
title_label.pack()

# Computer icon and menu in one row
selection_frame = tk.Frame(main)
selection_frame.pack(pady=10)

computer_logo_label = tk.Label(selection_frame, image=computer_logo)
computer_logo_label.pack(side=tk.LEFT, padx=10)

options = [_("Shut down"), _("Reboot"), _("Log out"), _("Switch user / Lock screen"), _("Sleep mode")]

selected_option = tk.StringVar()
selected_option.set(options[0])  # Set the default value

dropdown = ttk.Combobox(selection_frame, values=options, textvariable=selected_option, width=30)
dropdown.pack(side=tk.LEFT, pady=10)
dropdown.bind("<<ComboboxSelected>>", show_description)

description = tk.StringVar()
description_label = tk.Label(main, textvariable=description)
description_label.pack()

# Create a frame for buttons and align it to the right
button_frame = tk.Frame(main)
button_frame.pack(side=tk.RIGHT, padx=5, pady=5)

btn_help = tk.Button(button_frame, text=_("HELP"), command=show_help)
btn_help.pack(side=tk.LEFT, padx=5)

btn_ok = tk.Button(button_frame, text=_("OK"), command=lambda: execute_command(selected_option.get()))
btn_ok.pack(side=tk.LEFT, padx=5)

btn_cancel = tk.Button(button_frame, text=_("CANCEL"), command=main.quit)
btn_cancel.pack(side=tk.LEFT, padx=5)

adjust_window_size()

main.mainloop()
