from tkcalendar import Calendar
import tkinter as tk

root = tk.Tk()
root.title("Calendario de prueba")

cal = Calendar(root, selectmode='day')
cal.pack(pady=20)

root.mainloop()
