import Tkinter as tk

root = tk.Tk()
#TODO LOGGER
print(root.winfo_screenwidth())
print(root.winfo_screenheight())
#root.destroy()
root.config(height=root.winfo_screenheight()-80,width=root.winfo_screenwidth())
root.mainloop()