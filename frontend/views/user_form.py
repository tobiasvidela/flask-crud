import tkinter as tk
from tkinter import messagebox
from api_client import APIClient


class UserForm(tk.Toplevel):

  def __init__(self, master, refresh_callback, user=None):
    super().__init__(master)

    self.refresh_callback = refresh_callback
    self.user = user

    self.title("Usuario")
    self.geometry("350x200")

    tk.Label(self, text="Nombre").pack()
    self.name_entry = tk.Entry(self)
    self.name_entry.pack()

    tk.Label(self, text="Email").pack()
    self.email_entry = tk.Entry(self)
    self.email_entry.pack()

    if user:
      self.name_entry.insert(0, user["name"])
      self.email_entry.insert(0, user["email"])

    tk.Button(self, text="Guardar", command=self.save_user).pack(pady=10)

  def save_user(self):
    data = {
      "name": self.name_entry.get(),
      "email": self.email_entry.get()
    }

    try:
      if self.user:
        APIClient.update_user(self.user["id"], data)
      else:
        APIClient.create_user(data)

      self.refresh_callback()
      self.destroy()

    except Exception as e:
      messagebox.showerror("Error", str(e))
