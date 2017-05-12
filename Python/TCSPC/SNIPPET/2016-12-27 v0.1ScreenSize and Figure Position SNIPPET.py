import Tkinter as tk
class CustomError(Exception):
	pass
root=tk.Tk()
DefaultFigSize=[640,480]
screenwidth=root.winfo_screenwidth()
screenheight=root.winfo_screenheight() 
dim_screen=[screenwidth, screenheight]  ###Put it into a list###
DefaultFigPosition=[dim_screen[0]-DefaultFigSize[0],dim_screen[1]-DefaultFigSize[1]]
if min(DefaultFigPosition)<=0:
	raise CustomError('Current display resolution too small to display standard figure')
