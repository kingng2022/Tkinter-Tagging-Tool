import tkinter as tk
from PIL import ImageTk, Image, ImageDraw
import glob
import shutil
import re
import os
import copy


#counter for image labelled 
class counter:
    def __init__(self, count):
        self.count = count

n = counter(0)


#params for grids spliting 
min_y, max_y, min_x, max_x = 350, 650, 150, 1650
color = (0,255,0)
thickness = 2
grid_w, grid_h = 100, 100


#calculate the grid positions 
grid_position = [] 
for w in range(min_x, max_x, grid_w):
    for h in range(min_y, max_y, grid_h):
        grid_position.append([(w,h),(w+grid_w,h+grid_h)])

        
#sort images in the folder 
image_path = glob.glob('*.jpg')
image_path.sort(key=lambda x:(int(re.search('(\d+)-(\d+)_(\d+)_(\d+).jpg', x).group(1)),int(re.search('(\d+)-(\d+)_(\d+)_(\d+).jpg', x).group(2)),int(re.search('(\d+)-(\d+)_(\d+)_(\d+).jpg', x).group(3)),int(re.search('(\d+)-(\d+)_(\d+)_(\d+).jpg', x).group(4)) ))


#name and create target  folders 
target_dir = ['clean_wet', 'clean-half', 'clean_dry', 'little-dirty', 'sparse-dirty', 'dense-dirty', 'blockage', 'broader']

for d in target_dir:
    try:
        os.mkdir(d)
    except:
        pass
    
    
#create the history list recording the files movement
history = []


#display functions
def display_full():
    img_path = re.search('(.+)_\d+.jpg',image_path[n.count]).group(1)
    img = Image.open(f'../cropped_image/org_{img_path}.jpg')
    grid_pos = grid_position[int(re.search('(\d+)\.', image_path[n.count]).group(1))-1]
    draw = ImageDraw.Draw(img)
    draw.rectangle(grid_pos, outline=(0,255,0), width=2)
    img = img.resize((int(1920*0.8) ,int( 1080*0.8)))
    img = ImageTk.PhotoImage(img)
    panel.configure(image = img)
    panel.image = img

def display_crop():
    img_crop = ImageTk.PhotoImage(Image.open(image_path[n.count])) 
    panel_crop.configure(image = img_crop)
    panel_crop.image = img_crop

    
#button functions
def move2file(target_path):
    shutil.move(image_path[n.count],target_path+ '/'+ image_path[n.count]) 
    print(f'moved {image_path[n.count]} to {target_path}')
    history.append([image_path[n.count],target_path])

    n.count += 1 
    display_full()
    display_crop()
 
def undo():
    try:
        shutil.move(history[-1][1]+'/'+history[-1][0], history[-1][0])
        print(f'moved {history[-1][0]} back from {history[-1][1]}')    
        history.pop()
        n.count -=1
        display_full()
        display_crop()
    except:
        print('nothing to undo!')

        
#create the tool window
win =  tk.Tk()
win.geometry("1600x900")

#buttons params
btn_w = 15
btn_h = 5
btn_list = [tk.Button(win)]*len(target_dir)
relx = [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85]
rely = [0.2]*len(target_dir)
hkey = ['a','s','d','f','h','j','k','l']

#create class buttons
for i in range(len(btn_list)):
    btn_list[i]  = tk.Button(win, text=target_dir[i]+f'({hkey[i].upper()})', width=btn_w, height=btn_h, command= lambda m=target_dir[i]: move2file(m))
    btn_list[i].place(relx=relx[i] ,rely= rely[i], anchor='center')
    win.bind(hkey[i], lambda event, d = target_dir[i]: move2file(d))

#create undo button 
btn_undo  = tk.Button(win, text='Undo(U)', width=btn_w, height=btn_h, command= lambda: undo())
btn_undo.place(relx=0.95 ,rely= 0.05, anchor='center')
win.bind('u', lambda event: undo()) 

#images display
#original images with grids
img_path = re.search('(.+)_\d+.jpg',image_path[n.count]).group(1)
img = Image.open(f'../cropped_image/org_{img_path}.jpg')
img = ImageTk.PhotoImage(img)
panel = tk.Label(win, image = img)
panel.place(relx= 0.5, rely=0.8, anchor='center')
display_full()

#cropped images
img_crop = ImageTk.PhotoImage(Image.open(image_path[n.count]))
panel_crop = tk.Label(win, image = img_crop)
panel_crop.place(relx= 0.5, rely=0.06, anchor='center')

win.mainloop()

print(f'{n.count} images tagged')
