import tkinter as tk
from tkinter import ttk, messagebox
from api_client import APIClient
from views.user_form import UserForm


class MainView(tk.Frame):
  REFRESH_INTERVAL = 300000  # 5 minutos en milisegundos

  def __init__(self, master):
    super().__init__(master)
    self.pack(fill="both", expand=True)

    self.create_widgets()
    self.load_users()
    self.auto_refresh()

  # Crea la tabla para mostrar los usuarios y los botones para las acciones, configurando las columnas de la tabla y sus encabezados, y organizando los botones en un marco separado para una mejor disposición visual. 
  def create_widgets(self):
    columns = ("id", "name", "email")

    self.tree = ttk.Treeview(self, columns=columns, show="headings")

    for col in columns:
      self.tree.heading(col, text=col.capitalize())
      self.tree.column(col, width=150)

    self.tree.pack(fill="both", expand=True, pady=10)

    btn_frame = tk.Frame(self)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Crear", command=self.create_user).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Modificar", command=self.edit_user).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Eliminar", command=self.delete_user).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Refrescar", command=self.load_users).pack(side="left", padx=5)
  
  # Limpia la tabla y carga los usuarios desde la API, manejando errores con un mensaje emergente
  def load_users(self):
    for row in self.tree.get_children():
      self.tree.delete(row)

    try:
      users = APIClient.get_users()
      for user in users:
        self.tree.insert("", "end", values=(user["id"], user["name"], user["email"]))
    except Exception as e:
      messagebox.showerror("Error", str(e))

  # Obtiene la fila seleccionada y extrae los valores reales de la misma, los convierte a un diccionario con claves id, name y email, y maneja el caso donde no se ha seleccionado ningún usuario mostrando una advertencia
  def get_selected_user(self):
    selected = self.tree.selection()
    if not selected:
      messagebox.showwarning("Atención", "Selecciona un usuario")
      return None

    values = self.tree.item(selected[0])["values"]
    return {"id": values[0], "name": values[1], "email": values[2]} #cambiar a retornar usuario en lugar de json hardcodeado

  # Abre el formulario de usuario para crear un nuevo usuario, pasando la función de recarga de usuarios como callback para actualizar la lista después de crear el usuario
  def create_user(self):
    UserForm(self, self.load_users)

  # Obtiene el usuario seleccionado y abre el formulario de usuario para editarlo, pasando el usuario como argumento
  def edit_user(self):
    user = self.get_selected_user()
    if user:
      UserForm(self, self.load_users, user)

  # Obtiene el usuario seleccionado, solicita confirmación para eliminarlo, y si se confirma, llama a la API para eliminar el usuario y recarga la lista de usuarios
  def delete_user(self):
    user = self.get_selected_user()
    if user:
      confirm = messagebox.askyesno("Confirmar", "¿Eliminar usuario?")
      if confirm:
        APIClient.delete_user(user["id"])
        self.load_users()

  def auto_refresh(self):
    self.load_users()
    self.after(self.REFRESH_INTERVAL, self.auto_refresh)
