import tkinter
from PIL import Image, ImageTk
import numpy
import os
import glob
import argparse

WINDOW_H = 600
WINDOW_W = 500
IMAGE_H  = 500
IMAGE_W  = WINDOW_W
BUTTON_H = 50
FONT_SIZE = 0
FRAME_NOW_WINDOW_H =50
OUTPUT_FILE_NAME = 'rm_file.sh'

#command line
parser = argparse.ArgumentParser()
parser.add_argument('--in_dir', type=str)
parser.add_argument('--img_type', type=str)

args = parser.parse_args()
DIR = args.in_dir 
FILE_TYPE = args.img_type



def main():
    # file info extract
    total_file_num = cnt_file_num(DIR,FILE_TYPE)
    file_array = []
    for pathAndFilename in glob.iglob(os.path.join(DIR, "*."+FILE_TYPE)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        file_array.append(DIR+'/'+title+ext)
    
    # window setting
    window = tkinter.Tk()
    window = custom_window(window)
    window.window_size_set(WINDOW_W,WINDOW_H)
    window.window_name_set("IMAGE rm")
    window.window_background_set("white")

    # first image frame
    frame_info = frame_info_cls(file_array,total_file_num)
    pil_img = Image.open(frame_info.file_array[frame_info.now])
    img = view_image(pil_img)
    img.pil_to_tk()
    img.pil_resize(IMAGE_H)

    # setting canvas for image
    canvas = custom_canvas(window.window,"white",IMAGE_H,IMAGE_W,tag='image')
    canvas.canvas_pack()
    canvas.canvas_place(0,0)
    canvas.canvas_create_image(img.tk_img,0,0,'nw')

    # setting canvas for string
    canvas_frame_num = custom_canvas(window.window,"white",IMAGE_H,IMAGE_W,tag='text')
    canvas_frame_num.canvas_pack()
    canvas_frame_num.canvas_place(0,IMAGE_H)
    canvas_frame_num.canvas_init_create_text(x=IMAGE_W/2,y=FRAME_NOW_WINDOW_H/2,fill='#778899',anchor='center',font_size=FONT_SIZE,frame_info=frame_info)
    
    # segging rm button 
    button_rm = custom_button_rm(window.window,"rm",fg='white',bg='#ee8484',font_size=FONT_SIZE,activeforeground='white',activebackground="#fd0000",canvas=canvas,frame_info=frame_info,canvas_frame_num=canvas_frame_num)
    button_rm.button_place(x=WINDOW_W/2,y=IMAGE_H+FRAME_NOW_WINDOW_H,h=BUTTON_H,w=WINDOW_W/2)

    # setting keep button
    button_keep = custom_button_keep(window.window,"keep",fg='white',bg='#b8c2ff',font_size=FONT_SIZE,activeforeground='white',activebackground="#0023fa",canvas=canvas,frame_info=frame_info,canvas_frame_num=canvas_frame_num)
    button_keep.button_place(x=0,y=IMAGE_H+FRAME_NOW_WINDOW_H,h=BUTTON_H,w=WINDOW_W/2)

    # main loop
    window.window_mainloop()


def write_rm_file(out_file_name, frame_info):
    with open(out_file_name, mode='w') as fw:
        print("generating "+"\""+out_file_name+"\"")
        output_str = ''
        for tmp_file_num in frame_info.rm_file_element_num:
            output_str += "rm -f "+frame_info.file_array[tmp_file_num]+"\n"
        fw.write(output_str)
    
def cnt_file_num(cnt_dir,cnt_file_type):
    file_num = 0;
    for name in os.listdir(cnt_dir):
        if name[-len(cnt_file_type):]==cnt_file_type:
            file_num += 1
    return file_num;

class frame_info_cls:
    def __init__(self,file_array,total_file_num):
        self.now = 0
        self.total_file_num = total_file_num
        file_array.sort()
        self.rm_file_element_num = []
        self.file_array = file_array
    def next(self):
        self.now += 1
    def print(self):
        print(self.now+1,"/",self.total_file_num,end=' ')
        print("\""+self.file_array[self.now]+"\"")
    def add_rm_file_element_num(self):
        self.rm_file_element_num.append(self.now)
        
class custom_window:
    def __init__(self,window):
        self.window = window

    def window_size_set(self,w,h):
        self.window.geometry(str(w)+"x"+str(h))
        
    def window_name_set(self,name):
        self.window.title(name)

    def window_mainloop(self):
        self.window.mainloop()
        
    def window_background_set(self,color):
        self.window.configure(bg=color)
        
class custom_canvas:
    def __init__(self,window,bg,h,w,tag):
        self.canvas = tkinter.Canvas(window, bg=bg, height=h, width=w)
        self.tag=tag
    def canvas_place(self,x,y):
        self.canvas.place(x=x,y=y)
    def canvas_create_image(self,tk_img,x,y,anchor):
        self.image_on_canvas = self.canvas.create_image(0,0,image=tk_img,anchor=anchor)
    def canvas_pack(self):
        self.canvas.pack()
    def canvas_init_create_text(self,x,y,fill,anchor,font_size,frame_info):
        font=("",font_size,"bold","roman","normal","normal")
        self.text_x = x
        self.text_y = y
        self.text_fill =fill
        self.text_anchor = anchor
        self.text_font_size = font_size
        self.text_font = font
        self.frame_info = frame_info
        text =  str(self.frame_info.now+1) + "/" + str(self.frame_info.total_file_num) 
        self.canvas.create_text(x,y,text=text,fill=fill,anchor=anchor,font=font,tag=self.tag)
        
    def canvas_refresh(self):
        tmp_txt = str(self.frame_info.now+1) + "/" + str(self.frame_info.total_file_num) 
        self.canvas.delete(self.tag)
        self.canvas.create_text(self.text_x,self.text_y,text=tmp_txt,fill=self.text_fill,anchor=self.text_anchor,font=self.text_font,tag=self.tag)
    
        
class custom_button_rm:
    def __init__(self,window,txt,fg,bg,font_size,activeforeground,activebackground,canvas,frame_info,canvas_frame_num):
        self.button = tkinter.Button(window,text=txt,command=self.btn_clicked,fg=fg,bg=bg,font=("",font_size,"bold","roman","normal","normal"),relief="sunken",activeforeground=activeforeground,activebackground=activebackground)
        self.canvas=canvas
        self.frame_info = frame_info
        self.canvas_frame_num = canvas_frame_num
    def button_place(self,x,y,w,h):
        self.button.place(x=x,y=y,width=w,height=h)
    def btn_clicked(self):
        print('[ rm ] ' ,end='')
        self.frame_info.print()
        self.frame_info.add_rm_file_element_num()
        self.frame_info.next()
        if self.frame_info.now == self.frame_info.total_file_num:
            write_rm_file(OUTPUT_FILE_NAME,self.frame_info)
            print("finish")
            exit()
        next_pil_img = Image.open(self.frame_info.file_array[self.frame_info.now])
        next_img = view_image(next_pil_img)
        next_img.pil_resize(IMAGE_H)
        self.canvas.canvas.photo = next_img.tk_img
        self.canvas.canvas.itemconfig(self.canvas.image_on_canvas,image=self.canvas.canvas.photo)
        self.canvas_frame_num.canvas_refresh()
class custom_button_keep:
    def __init__(self,window,txt,fg,bg,font_size,activeforeground,activebackground,canvas,frame_info,canvas_frame_num):
        self.button = tkinter.Button(window,text=txt,command=self.btn_clicked,fg=fg,bg=bg,font=("",font_size,"bold","roman","normal","normal"),activeforeground=activeforeground,activebackground=activebackground)
        self.canvas=canvas
        self.frame_info=frame_info
        self.canvas_frame_num = canvas_frame_num
        
    def button_place(self,x,y,w,h):
        self.button.place(x=x,y=y,width=w,height=h)
    def btn_clicked(self):
        print("[keep] ",end='')
        self.frame_info.print()
        self.frame_info.next()
        if self.frame_info.now == self.frame_info.total_file_num:
            write_rm_file(OUTPUT_FILE_NAME,self.frame_info)
            print("finish")
            exit()
        next_pil_img = Image.open(self.frame_info.file_array[self.frame_info.now])
        next_img = view_image(next_pil_img)
        next_img.pil_resize(IMAGE_H)
        self.canvas.canvas.photo = next_img.tk_img
        self.canvas.canvas.itemconfig(self.canvas.image_on_canvas,image=self.canvas.canvas.photo)
        self.canvas_frame_num.canvas_refresh()
        
class view_image:
    def __init__(self,pil_img):
        self.pil_img = pil_img
        self.tk_img = None
        self.pil_to_tk()
    def pil_to_tk(self):
        self.tk_img = ImageTk.PhotoImage(self.pil_img)
    def pil_resize(self,resize_size):
        if(self.pil_img.height <= resize_size and self.pil_img.width <= resize_size):
            pass
        else:
            if(self.pil_img.width>self.pil_img.height):
                scale = resize_size/self.pil_img.width
            else:
                scale = resize_size/self.pil_img.height
            resize_size_w = int(self.pil_img.width*scale)
            resize_size_h = int(self.pil_img.height*scale)
            self.pil_img = self.pil_img.resize((resize_size_w,resize_size_h))
            self.pil_to_tk()
            
main()
