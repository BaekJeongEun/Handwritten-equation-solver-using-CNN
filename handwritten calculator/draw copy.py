#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *


# In[2]:


from PIL import ImageGrab


# In[3]:


window = None


# In[4]:


canvas = None


# In[5]:


x1, y1 = None, None


# In[6]:


wp = 5


# In[7]:


def mouseMove(event):
    global x1, y1
    x1 = event.x
    y1 = event.y
    canvas.create_line(x1, y1, x1+1, y1+1, width=wp, fill="black")


# In[8]:


def mouseScroll(event):
    global wp
    if event.delta==120:
        wp+=1
    if event.delta==-120:
        wp-=1
        if wp<1:
            wp = 1
    textSize.config(text=str(wp))


# In[9]:


def clearCanvas():
    canvas.delete("all")


# In[10]:


def save():
    x = window.winfo_rootx()
    y = window.winfo_rooty()
    w = window.winfo_width() + x
    h = window.winfo_height() + y
    
    box = (x, y, w, h)
    img=ImageGrab.grab(box) #창의 크기만큼만 이미지저장
    saveas='capture.png'
    img.save(saveas)


# In[11]:


window=Tk()


# In[12]:


frame = Frame(window)


# In[13]:


frame.pack()


# In[14]:


canvas=Canvas(window, height=500,width=400)


# In[15]:


canvas.bind('<B1-Motion>', mouseMove)


# In[16]:


canvas.bind('<MouseWheel>', mouseScroll)


# In[17]:


canvas.pack(side=BOTTOM)


# In[18]:


window.title("Paint")


# In[19]:


button = Button(frame, text="Exit", fg = "red",
               command=window.destroy)


# In[20]:


button.grid(row=1, column = 1)


# In[21]:


savebutton = Button(frame, text="Save", fg = "red",
               command=save)


# In[22]:


savebutton.grid(row=1, column = 3)


# In[23]:


clear = Button(frame, text="Clear", fg = "red",
              command=clearCanvas)


# In[24]:


clear.grid(row=1, column = 2)


# In[25]:


textSize = Label(frame, text = str(wp))


# In[26]:


textSize.grid(row=1, column = 4)


# In[ ]:


window.mainloop()
