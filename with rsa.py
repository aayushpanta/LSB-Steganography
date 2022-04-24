import random
import sqlite3
import sys
from tkinter.constants import END,CENTER
from tkinter import ttk
from PIL import Image

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

DB_FILE = 'mydb.db'

def connect1():
    try:
        conn = sqlite3.connect(DB_FILE)
        print(sqlite3.version)
        print("Connect database successfully")
    except:
        print("Error : ", sys.exc_info()[0])
    finally:
        conn.close()

def create_table1():
    sql="""
        CREATE TABLE IF NOT EXISTS tbl_key(
            id INTEGER PRIMARY KEY,
            filepath TEXT NOT NULL,
            stegokey TEXT NOT NULL
        );
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        print("Create table successfully")
    except:
        print("Error : ", sys.exc_info()[0])
    finally:
        cursor.close()

def insert_record1(values):
    sql="""INSERT INTO tbl_key(filepath, stegokey) values(?, ?)"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        print("Insert record successfully")
    except:
        print("Error : ", sys.exc_info()[0])
    finally:
        cursor.close()
        conn.close()        

def records_btn():
    win_rec = tk.Tk()
    win_rec.title("Records")

        # Table
    tree = ttk.Treeview(master=win_rec, height = 14, columns = 2,)
    tree.grid(row = 0, column = 0, columnspan = 2)
    tree.heading('#0', text = 'Image Path', anchor = CENTER)
    tree.heading('#1', text = 'Key', anchor = CENTER)

    # cleaning Table 
    records = tree.get_children()
    for element in records:
        tree.delete(element)
    # getting data
    query = 'SELECT * FROM tbl_key ORDER BY id'
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        db_rows = cursor.execute(query)
        conn.commit()
    # filling data
    for row in db_rows:
        tree.insert('', 0, text = row[1], values = row[2])

    win_rec.mainloop()    
  
def help_btn():
    win_help = tk.Tk()
    win_help.title("Help")

    text_box = tk.Text(master=win_help, width= 62, font=15)
    text_box.pack()
    f= open("help.txt", "r")
    text = f.read()
    text_box.insert(tk.END, text)

    win_help.mainloop()

def openImg_btn():
    filepath = askopenfilename(
        filetypes=[("Image Files", "*.png)"), ("Image Files", "*.jpg)"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    #read the image
    im = Image.open(filepath)

    #show image
    im.show()

def clear_btn():
    ent_img_name.delete(0, tk.END)
    ent_msg.delete(0, tk.END)
    ent_new_name.delete(0, tk.END)
    ent_key.delete(0, tk.END)

    ent_dec_name.delete(0,tk.END)
    ent_keyin.delete(0,tk.END)
    ent_dec_msg.delete(0,tk.END)

def browse():
    """Open a img for editing."""
    filepath = askopenfilename(
        filetypes=[("Image Files", "*.png"), ("Image Files", "*.jpg"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    else: 
        return filepath

def browse1():
    filepath = browse()
    ent_img_name.delete(0, tk.END)
    ent_img_name.insert(tk.END, filepath)

def browse2():
    filepath = browse()
    ent_dec_name.delete(0, tk.END)
    ent_dec_name.insert(tk.END, filepath)

def saveas():
    """Save the current img as a new img."""
    filepath = asksaveasfilename(
        defaultextension="png",
        filetypes=[("Image Files", "*.png"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    ent_new_name.delete(0, tk.END)
    ent_new_name.insert(tk.END, filepath)

def encode_btn():
    ent_dec_name.delete(0,tk.END)
    ent_keyin.delete(0,tk.END)
    ent_dec_msg.delete(0,tk.END)
    img = ent_img_name.get()
    image = Image.open(img, 'r')

    data = ent_msg.get()
    if (len(data) == 0): 
	    raise ValueError('Data is empty')

    newdata, n, d = encrypt(data)
    newimg = image.copy()
    k = pattern(newimg, newdata)
    r1 = random.randint(65, 90)
    r2 = random.randint(65, 90)
    key = str(k) + chr(r1) + str(n) + chr(r2) + str(d)

    outname = ent_new_name.get()
    newimg.save(outname, str(outname.split(".")[1].upper()))
    print("The key is: ",key)
    ent_key.insert(tk.END,key)
    values = (outname , key)
    print(values)
    insert_record1(values)

def getPrimes():
    
    check = 0
    p = random.randint(10, 100)
    if (p <= 50):
        con = 1
    else:
        con = -1
    
    while(check == 0):
        check = 1
        for i in range(2, int(p/5) + 1):
            if (p % i == 0):
                check = 0
                p += con
                break
    
    check = 0
    q = random.randint(10, 100)
    if (q <= 50):
        con = 1
    else:
        con = -1
    
    while(check == 0):
        if (q == p):
            q += con
            continue
        check = 1
        for i in range(2, int(q/5) + 1):
            if (q % i == 0):
                check = 0
                q += con
                break
    return p, q

def encrypt(data):
    p, q = getPrimes()
    n = p * q
    o = (p -1) * (q - 1)

    for i in range(2, o):
        check = 0
        for j in range(2, i + 1):
            if ((i % j == 0) and (o % j == 0)):
                check = 1
                break
        if (check == 0):
            e = i
            break
    
    check = 0
    i == 2
    while(check == 0):
        if((i * e) % o == 1):
            d = i
            check = 1
        else:
            i += 1
    
    newdata = ''
    datalen = len(data)
    for i in range(datalen):
        m = ord(data[i])
        c = (m ** e) % n
        if (c < 1000):
            newdata += '0'
        elif (c < 100):
            newdata += '00'
        elif(c < 10):
            newdata += '000'
        newdata += str(c)
    
    return newdata, n, d

def pattern(img, data):
    length = img.size[0]
    (x, y) = (0, 0)
    key = random.randint(1, 9)

    for pixel in modPix(img.getdata(), data, key):
        img.putpixel((x, y), pixel)

        if (x == length - 1):
            x = 0
            y += 1
        else:
            x += 1
    
    return key

def modPix(pix, data, key):
    datalist = genData(data)
    datalen = len(datalist)
    imgdata = iter(pix)
    i = 0

    for  k in range(datalen * key):
        pixlist = [value for value in imgdata.__next__()[:3] + 
                                      imgdata.__next__()[:3] + 
                                      imgdata.__next__()[:3] ]
        
        if (k % key == 0):
            for j in range(0, 8):
                if (datalist[i][j] == '0' and pixlist[j] % 2 != 0):
                    pixlist[j] -= 1
                
                elif (datalist[i][j] != '0' and pixlist[j] % 2 == 0):
                    if (pixlist[j] == 0):
                        pixlist[j] += 1
                    else:
                        pixlist[j] -= 1
            
            if (i == datalen - 1):
                if (pixlist[-1] % 2 == 0):
                    if (pixlist[-1] == 0):
                        pixlist[-1] += 1
                    else:
                        pixlist[-1] -= 1
            else:
                if(pixlist[-1] % 2 != 0):
                    pixlist[-1] -= 1        
            i += 1

        pixlist = tuple(pixlist)
        yield pixlist[0:3]
        yield pixlist[3:6]
        yield pixlist[6:9]

def genData(data):
    newdata = []

    for i in data:
        newdata.append(format(ord(i), '08b'))
    
    return newdata

def decod_btn():
    ent_img_name.delete(0, tk.END)
    ent_msg.delete(0, tk.END)
    ent_new_name.delete(0, tk.END)
    ent_key.delete(0, tk.END)
    msg=decrypt()
    ent_dec_msg.insert(tk.END,msg)

def decode(key):
    img = ent_dec_name.get()
    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())
    i = 0

    while(True):
        pixlist = [value for value in imgdata.__next__()[:3] + 
                                      imgdata.__next__()[:3] + 
                                      imgdata.__next__()[:3] ]
        binstr = ''
        
        if (i % key == 0):
            for j in pixlist[:8]:
                if (j % 2 == 0):
                    binstr += '0'
                else:
                    binstr += '1'            
            data += chr(int(binstr, 2))
            
            if (pixlist[-1] % 2 != 0):
                return data
        i += 1

def decrypt():
    key = ent_keyin.get()
    k = int(key[0])
    n, d = getKey(key)
    data = decode(k)
    datalen = len(data)
    newdata = ""

    for i in range(int(datalen/4)):
        j = i * 4
        c = int(data[j:(j+4)])
        m = (c ** d) % n
        newdata += chr(m)
    
    return newdata

def getKey(key):
    keylen = len(key)
    keys = ["",""]
    case = 0
    
    for i in range(2, keylen):
        c = ord(key[i])
        if (c >= 65 and c <= 90):
            case += 1
        else:
            keys[case] += key[i]
    
    n = int(keys[0])
    d = int(keys[1])
    return n, d
 
#connect1()
#create_table1()

window = tk.Tk()
window.title("Image Steganography")

window.rowconfigure(0, minsize=300, weight=2)
window.columnconfigure(1, minsize=300, weight=3)

    
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=3)
fr_buttons.grid(row=0, column=0, sticky="n")

btn_encode = tk.Button(fr_buttons, text="Encode",command=encode_btn)
btn_decode = tk.Button(fr_buttons, text="Decode",command=decod_btn)
btn_clear = tk.Button(fr_buttons, text="Clear",command=clear_btn)
btn_openimg = tk.Button(fr_buttons, text="Open Img",command=openImg_btn)
btn_help = tk.Button(fr_buttons, text="Help",command=help_btn)
btn_records = tk.Button(fr_buttons, text="Records",command=records_btn)

btn_encode.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_decode.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
btn_openimg.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
btn_records.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
btn_help.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
btn_clear.grid(row=6, column=0, sticky="ew", padx=5, pady=5)

frm_input1 = tk.Frame(window, relief=tk.SUNKEN)
frm_input1.grid(row=0, column=1, sticky="nsew" )


frm_input2=tk.Frame(window)
frm_input2.grid(row=2, column=1, sticky="nsew")

lbl_img_name = tk.Label(master=frm_input1, text="Enter image name for encode:")
ent_img_name = tk.Entry(master=frm_input1, width=50)
btn_img1 = tk.Button(
    master=frm_input1,
    text="Browse",
    command=browse1
)
btn_img1.grid(row=0,column=3)
lbl_img_name.grid(row=0, column=1, sticky="e")
ent_img_name.grid(row=0, column=2)


lbl_msg = tk.Label(master=frm_input1, text="Enter data/message for encode")
ent_msg = tk.Entry(master=frm_input1, width=50)
lbl_msg.grid(row=1, column=1, sticky="e")
ent_msg.grid(row=1, column=2)

lbl_new_name = tk.Label(master=frm_input1, text="Enter new image name:")
ent_new_name = tk.Entry(master=frm_input1, width=50)
btn_img2 = tk.Button(
    master=frm_input1,
    text="Save As",
    command=saveas
)
btn_img2.grid(row=3,column=3)
lbl_new_name.grid(row=3, column=1, sticky="e")
ent_new_name.grid(row=3, column=2)

lbl_key = tk.Label(master=frm_input1, text="The key is:")
ent_key = tk.Entry(master=frm_input1, width=50)
lbl_key.grid(row=4, column=1, sticky="e")
ent_key.grid(row=4, column=2)

lbl_dec_name = tk.Label(master=frm_input2, text="Enter image name for decode:")
ent_dec_name = tk.Entry(master=frm_input2, width=50)
btn_img3 = tk.Button(
    master=frm_input2,
    text="Browse",
    command=browse2
)
btn_img3.grid(row=5,column=3)
lbl_dec_name.grid(row=5, column=1, sticky="e")
ent_dec_name.grid(row=5, column=2)

lbl_keyin = tk.Label(master=frm_input2, text="Enter key:")
ent_keyin = tk.Entry(master=frm_input2, width=50)
lbl_keyin.grid(row=6, column=1, sticky="e")
ent_keyin.grid(row=6, column=2)

lbl_dec_msg = tk.Label(master=frm_input2, text="The decoded msg is:")
ent_dec_msg = tk.Entry(master=frm_input2, width=50)
lbl_dec_msg.grid(row=7, column=1, sticky="e")
ent_dec_msg.grid(row=7, column=2)

window.mainloop()