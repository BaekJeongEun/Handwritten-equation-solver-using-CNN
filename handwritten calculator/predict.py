
# ~~~~~~~~draw~~~~~
import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from tensorflow import keras
import seaborn as sns
from tkinter import *
from tkinter.colorchooser import *
from PIL import ImageGrab
def NewFile() :
  print("New File!")
def OpenFile() :
  print("Open File!")
def About() :
  print("This is a simple example of a menu")
root = Tk()
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=NewFile)
filemenu.add_command(label="Open...", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)
canvas = Canvas(root, width=1550, height=150, bg='white')
color = "red"
result = '#000000'

save = False

def callback() :
  global result
  result = askcolor(title = "Colour Chooser")
  result = result[1]

def savefile():
    global save
    x = root.winfo_rootx() +3
    y = root.winfo_rooty() +3
    w = 1533 + x +3
    h = 140 + y +3
    
    box = (x, y, w, h)
    img=ImageGrab.grab(box) #창의 크기만큼만 이미지저장
    saveas='capture.png'
    img.save(saveas)
    save = True

button = Button(root, text='Choose Color', fg="darkgreen", command=callback)
button.pack(side=RIGHT, padx=10)

button = Button(root, text='save', fg="red", command=savefile)
button.pack(side=RIGHT, padx=10)

lastx, lasty = 0, 0

def xy(event) :
  global lastx, lasty
  lastx, lasty = event.x, event.y
def addLine(event) :
  global lastx, lasty
  canvas.create_line((lastx, lasty, event.x, event.y), width = 5, fill=result, capstyle=ROUND, smooth=True)
  lastx, lasty = event.x, event.y

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
canvas.pack()
canvas.bind("<Button-1>", xy)
canvas.bind("<B1-Motion>", addLine)
root.mainloop()

while not save:
    hi = 1
    if save:
        break

#~~~3. Prediction~~~

from PIL import Image
from itertools import groupby

print('Prediction !!!!!!!!!!!!!!')

'loading image'
#image = Image.open("...//testing.png").convert("L")
image = Image.open("capture.png").convert("L")

'resizing to 28 height pixels'
w = image.size[0]
h = image.size[1]
r = w / h # aspect ratio
new_w = int(r * 28)
new_h = 28
new_image = image.resize((new_w, new_h))

'converting to a numpy array'
new_image_arr = np.array(new_image)

'inverting the image to make background = 0'
new_inv_image_arr = 255 - new_image_arr

'rescaling the image'
final_image_arr = new_inv_image_arr / 255.0

'splitting image array into individual digit arrays using non zero columns'
m = final_image_arr.any(0)
out = [final_image_arr[:,[*g]] for k, g in groupby(np.arange(len(m)), lambda x: m[x] != 0) if k]


'''
iterating through the digit arrays to resize them to match input 
criteria of the model = [mini_batch_size, height, width, channels]
'''
num_of_elements = len(out)
elements_list = []

for x in range(0, num_of_elements):

    img = out[x]
    
    #adding 0 value columns as fillers
    width = img.shape[1]
    filler = (final_image_arr.shape[0] - width) / 2
    
    if filler.is_integer() == False:    #odd number of filler columns
        filler_l = int(filler)
        filler_r = int(filler) + 1
    else:                               #even number of filler columns
        filler_l = int(filler)
        filler_r = int(filler)
    
    arr_l = np.zeros((final_image_arr.shape[0], filler_l)) #left fillers
    arr_r = np.zeros((final_image_arr.shape[0], filler_r)) #right fillers
    
    #concatinating the left and right fillers
    help_ = np.concatenate((arr_l, img), axis= 1)
    element_arr = np.concatenate((help_, arr_r), axis= 1)
    
    element_arr.resize(28, 28, 1) #resize array 2d to 3d

    #storing all elements in a list
    elements_list.append(element_arr)


elements_array = np.array(elements_list)

'reshaping to fit model input criteria'
elements_array = elements_array.reshape(-1, 28, 28, 1)

'predicting using the model'
#model = keras.models.load_model("...//model.h5")
model = keras.models.load_model("model.h5")
elements_pred =  model.predict(elements_array)
elements_pred = np.argmax(elements_pred, axis = 1)

#~~~4. Mathematical Operation~~~

def math_expression_generator(arr):
    
    op = {
              10,   # = "/"
              11,   # = "+"
              12,   # = "-"
              13    # = "*"
                  }   
    
    m_exp = []
    temp = []
        
    'creating a list separating all elements'
    for item in arr:
        if item not in op:
            temp.append(item)
        else:
            m_exp.append(temp)
            m_exp.append(item)
            temp = []
    if temp:
        m_exp.append(temp)
        
    'converting the elements to numbers and operators'
    i = 0
    num = 0
    for item in m_exp:
        if type(item) == list:
            if not item:
                m_exp[i] = ""
                i = i + 1
            else:
                num_len = len(item)
                for digit in item:
                    num_len = num_len - 1
                    num = num + ((10 ** num_len) * digit)
                m_exp[i] = str(num)
                num = 0
                i = i + 1
        else:
            m_exp[i] = str(item)
            m_exp[i] = m_exp[i].replace("10","/")
            m_exp[i] = m_exp[i].replace("11","+")
            m_exp[i] = m_exp[i].replace("12","-")
            m_exp[i] = m_exp[i].replace("13","*")
            
            i = i + 1
    
    
    'joining the list of strings to create the mathematical expression'
    separator = ' '
    m_exp_str = separator.join(m_exp)
    
    return (m_exp_str)

'creating the mathematical expression'
m_exp_str = math_expression_generator(elements_pred)

'calculating the mathematical expression using eval()'
while True:
    try:
        answer = eval(m_exp_str)    #evaluating the answer
        answer = round(answer, 2)
        equation  = m_exp_str + " = " + str(answer)
        print(equation)   #printing the equation
        break

    except SyntaxError:
        print("Invalid predicted expression!!")
        print("Following is the predicted expression:")
        print(m_exp_str)
        break

#-------------------------------
