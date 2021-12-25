from tkinter import *
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont


WHITE = "#fff"
FILE = ""
COLOR=()
T_VALUE = 0
POSITION = "Top-Left"
WM_IMG = Image.Image()
WM_TEXT = ""
FONT = "Arial"
SIZE = 10
is_color_selected = False


def browse_file():
    global FILE
    FILE = filedialog.askopenfilename(initialdir="/")
    filename.delete(0, 'end')
    filename.insert(0, FILE)


def add_wm():
    global FILE, COLOR, POSITION, T_VALUE, WM_IMG, WM_TEXT, FONT, SIZE
    if FILE == "":
        messagebox.showwarning(title="Warning", message="Please don't leave the field empty.")
    else:
        try:
            with Image.open(FILE).convert("RGBA") as img:

                width, height = img.size
                # make a blank image for the text, initialized to transparent text color
                text = Image.new("RGBA", img.size, (255, 255, 255, 0))
                font = ImageFont.truetype(f"fonts/{FONT}.ttf", int(SIZE))
                draw = ImageDraw.Draw(text)

                if is_color_selected:
                    fill = (COLOR[0], COLOR[1], COLOR[2], T_VALUE)
                else:
                    fill = (0, 0, 0, T_VALUE)

                if POSITION == "Top-Left":
                    x=30
                    y=30
                    draw.text((50,50), WM_TEXT, font=font, fill=fill)
                elif POSITION == "Top-Right":
                    x=width-130
                    y=30
                    draw.text((x,y), WM_TEXT, font=font, fill=fill)
                elif POSITION == "Bottom-Left":
                    x=30
                    y=height-30
                    draw.text((x,y), WM_TEXT, font=font, fill=fill)
                elif POSITION == "Bottom-Right":
                    x=width-130
                    y=height-40
                    draw.text((x,y), WM_TEXT, font=font, fill=fill)
                # Position is center
                else: 
                    x=int(width/2)
                    y=int(height/2)
                    draw.text((x,y), WM_TEXT, font=font, fill=fill)    

                WM_IMG = Image.alpha_composite(img, text)

        except AttributeError:
            messagebox.showerror(title="Error", message="Enter correct file path.")


def preview():
    global WM_IMG
    WM_IMG.show()


def save():
    global WM_IMG, FILE
    wm_filename = FILE.split("/")[-1].split(".")[0]
    ext = FILE.split("/")[-1].split(".")[1].lower()     
    if WM_IMG.mode in ("RGBA", "p"):
        WM_IMG = WM_IMG.convert("RGB")
    WM_IMG.save(f'images/watermark-{wm_filename}.{ext}')


def add_text():
    global WM_TEXT
    WM_TEXT= watermark_text.get()
    if WM_TEXT == "":
        messagebox.showerror(title="Watermark Text", message="Watermark text field cannot be empty.")
        


def color_chooser():
    global COLOR, is_color_selected
    try:
        color = colorchooser.askcolor() #returns tuple with rgb value tuple and hex value string
    except TypeError:
        messagebox.showwarning(title="Color Chooser", message="Color not selected.")
        color_tuple = (0, 0, 0)
        is_color_selected = False
    else:
        color_tuple = color[0]
        is_color_selected = True
    finally:
        COLOR = (int(color_tuple[0]), int(color_tuple[1]), int(color_tuple[2]))
        color_label.config(background=color[1])
        

def font_name_select(*args):
    global FONT
    FONT = font_var.get()


def font_size_select(*args):
    global SIZE
    SIZE = size_var.get()


def transparent(*args):
    global T_VALUE
    T_VALUE = t_var.get()


def position_select(*args):
    global POSITION
    POSITION = pos_var.get()


def reset():
    global FILE, COLOR, POSITION, T_VALUE, WM_IMG, WM_TEXT, FONT, SIZE, is_color_selected
    FILE = ""
    COLOR=()
    T_VALUE = 0
    POSITION = "Top-Left"
    WM_IMG = Image.Image()
    WM_TEXT = ""
    FONT = "Arial"
    SIZE = 10
    is_color_selected = False

    filename.delete(0, END)
    watermark_text.delete(0, END)
    color_label.config(background="Black")
    transparency_scale.set(127)
    pos_var.set(position_tuple[0])
    font_var.set(font_tuple[0])
    size_var.set(size_list[0])



####### UI ########

window = Tk()
window.title("Watermarker")
window.config(padx=50, pady=50, bg=WHITE)


# Browsing image UI
filename = Entry(width=50)
filename.insert(0, "filename")
filename.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=W)
browse = Button(text="Browse", width=10, justify="left", command=browse_file)
browse.grid(row=0, column=2, padx=10, pady=10, sticky=W)


# Watermark text UI
watermark_text_label = Label(text="Text", background=WHITE)
watermark_text_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
watermark_text = Entry(width=30) 
watermark_text.grid(row=1, column=1, padx=10, pady=10, sticky=W)
add_text_button = Button(text="Add Text", width=10, command=add_text)
add_text_button.grid(row=1, column=2, padx=10, pady=10, sticky=W)


# Color chooser UI
choose_color_label = Label(text="Color", background=WHITE)
choose_color_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
color_label = Label(width=10, height=1, background="Black")
color_label.grid(row=2, column=1, padx=10, pady=10, sticky=W)
color_button = Button(text="Choose Color", command=color_chooser)
color_button.grid(row=2, column=2, padx=10, pady=10, sticky=W)


# Transpareny setting UI
transparency_label = Label(text="Transparency", background=WHITE, justify="left")
transparency_label.grid(row=3, column=0, sticky=W, padx=10, pady=10)
t_var = IntVar()
transparency_scale = Scale(from_=0, to=255, orient=HORIZONTAL, command=transparent)
## set alpha value to half opacity
transparency_scale.set(127)
transparency_scale.grid(row=3, column=1, sticky=W, padx=10, pady=10)


# Watermark Position Selection UI
position_label = Label(text="Position", background=WHITE, justify="left")
position_label.grid(row=4, column=0, sticky=W, padx=10, pady=10)

position_tuple = ("Top-Left", "Top-Right", "Center", "Bottom-Left", "Bottom-Right")
pos_var = StringVar(window)
pos_var.set(position_tuple[0])
position_menu = OptionMenu(window, pos_var, *position_tuple)
pos_var.trace("w", position_select)
position_menu.config(width=20)
position_menu.grid(row=4, column=1, sticky=W, padx=10, pady=10)


# Font Chooser UI
font_label = Label(text="Font", background=WHITE, justify="left")
font_label.grid(row=5, column=0, sticky=W, padx=10, pady=10)

font_tuple = ("Arial", "Courier", "DejaVuSans", "FreeMono", "Gidole-Regular", "Helvetica", "Lucida-Calligraphy", "Montserrat-Black", "Times New Roman")
font_var = StringVar(window)
font_var.set(font_tuple[0])
font_menu = OptionMenu(window, font_var, *font_tuple)
font_var.trace("w", font_name_select)
font_menu.config(width=20)
font_menu.grid(row=5, column=1, sticky=W, padx=10, pady=10)

size_list = [size for size in range(10, 41)]
size_var = StringVar(window)
size_var.set(size_list[0])
size_menu = OptionMenu(window, size_var, *size_list)
size_var.trace("w", font_size_select)
size_menu.config(width=10)
size_menu.grid(row=5, column=2, sticky=W, padx=10, pady=10)


# Watermark Buttons
add_wm_button = Button(text="Add Watermark", command=add_wm)
add_wm_button.grid(row=6, column=0, padx=10, pady=10, sticky=W)

preview_button = Button(text="Preview", width=10, command=preview)
preview_button.grid(row=6, column=1, padx=10, pady=10, sticky=EW)

save_button = Button(text="Save", width=10, command=save)
save_button.grid(row=6, column=2, padx=10, pady=10, sticky=W)

reset_button = Button(text="Reset", width=10, command=reset)
reset_button.grid(row=7, column=0, padx=10, pady=10, sticky=W)


window.mainloop()


