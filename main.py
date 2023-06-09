import json
from tkinter import *
from tkinter import messagebox
from random import choice, shuffle
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """Generate a random password, put it into the password field and copy it to the clipboard"""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(12)]
    password_symbols = [choice(symbols) for _ in range(4)]
    password_numbers = [choice(numbers) for _ in range(4)]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = "".join(password_list)
    password_input.delete(0, END)
    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """Check if all the fields have been filled in. If not, then show a warning.
    If all are populated, save the website name,
    username and password to data.json"""
    website = website_input.get()
    user = user_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "user": user,
            "password": password,
        }
    }

    if website == "" or user == "" or password == "":
        messagebox.showwarning(title="Oops", message="You didn't fill in all the fields.\n"
                                                     "Please complete the form and try again.")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                data.update(new_data)
        except FileNotFoundError:
            data = new_data

        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
            website_input.delete(0, END)
            password_input.delete(0, END)
            website_input.focus()


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    """Check if the website is in data.json. If not, show a warning. If it is, the retrieve the user and password for
    the website, show it in a messagebox and copy the password to the clipboard"""
    search_name = website_input.get().lower()
    search_result = {}

    if search_name == "":
        messagebox.showwarning(title="Oops", message="You didn't fill in the 'Website' field.\n"
                                                     "Please complete the form and try again.")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)

            for entry in data:
                if search_name == entry.lower():
                    search_result = data[entry]
        except FileNotFoundError:
            messagebox.showwarning(title="Error", message="No data file found.")
        else:
            if len(search_result) < 1:
                messagebox.showwarning(title="No Result",
                                       message="There are no saved details for the website you are looking for.")
            else:
                messagebox.showinfo(title="Search Result", message=f"Login details for {search_name.title()}:\n\n"
                                                                   f"Email/Username: {search_result['user']}\n"
                                                                   f"Password: {search_result['password']}\n\n"
                                                                   f"Password has been copied to the clipboard.")
                pyperclip.copy(search_result["password"])


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# create and place the logo on screen
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# text labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0, sticky="W")
user_label = Label(text="Email/Username:")
user_label.grid(row=2, column=0, sticky="W")
password_label = Label(text="Password:")
password_label.grid(row=3, column=0, sticky="W")

# text input fields
website_input = Entry(width=33)
website_input.grid(row=1, column=1, sticky="W")
website_input.focus()
user_input = Entry(width=52)
user_input.insert(0, "example@email.com")
user_input.grid(row=2, column=1, columnspan=2, sticky="W")
password_input = Entry(width=33)
password_input.grid(row=3, column=1, sticky="W")

# buttons
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2, sticky="W", padx=(3, 0))
gen_password_button = Button(text="Generate Password", command=generate_password)
gen_password_button.grid(row=3, column=2, sticky="W")
add_button = Button(text="Add", width=44, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="W")


window.mainloop()
