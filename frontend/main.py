import tkinter as tk
from views.main_view import MainView

def main():
  root = tk.Tk()
  root.title("SGI - Gestión de Usuarios")
  root.geometry("900x600")

  MainView(root)

  root.mainloop()


if __name__ == "__main__":
  main()
