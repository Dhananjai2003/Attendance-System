from time import strftime
from tkinter import *
from PIL import Image,ImageTk
from cv2 import waitKey
from tkinter import filedialog
import os 
from datetime import datetime
from numpy import diag, save
import cv2
import numpy as np
import face_recognition
import os

####################################################################################################################################################################################

def fEncode(pic):
    encodedList = []
    for i in pic:
        i = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(i)[0]
        encodedList.append(encode)
    return encodedList
#print('Encoding Complete')

def clear():
    with open('Attendance.csv','w') as f:
        f.close()

def register(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')


####################################################################################################################################################################################


def home3():#to return to the home screen after taking attendence

    global home_button_2
    global attendence_list_label
    global button_to_save_std_data

    global attendence_button
    global display_button
    global entry_button

    home_button_2.grid_forget()
    attendence_list_label.grid_forget()
    button_to_save_std_data.grid_forget()

    attendence_button=Button(root,text='Attendence',command=to_take_attendence)#this for attendence
    entry_button=Button(root,text='enter new',command=enter_new_page)#this for new entry
    display_button=Button(root,text='Get Attndence',command=get_attendence_page)#this is for delete any rec

    attendence_button.grid(row=0,column=0)
    entry_button.grid(row=1,column=0)
    display_button.grid(row=2,column=0)

def diaplay_attendence(date_by_user):#to disply attendence asked from the user
    global date_entry_by_user

    attendence_display_window=Toplevel()
    attendence_log_file=open('log.txt','r')
    r=attendence_log_file.readline()
    file_data_list=r.split('  ||  ')
    for i in range(len(file_data_list)):
        l=file_data_list[i].split(',')
        if l[0]==date_by_user:
            for j in range(len(l)):
                Label(attendence_display_window,text=l[j]).pack()

def home2():#to return home after attendence sheet
    global home_button
    global date_entry_by_user
    global button_to_get_attendence

    global attendence_button
    global display_button
    global entry_button

    home_button.grid_forget()
    date_entry_by_user.grid_forget()
    button_to_get_attendence.grid_forget()

    attendence_button=Button(root,text='Attendence',command=to_take_attendence)#this for attendence
    entry_button=Button(root,text='enter new',command=enter_new_page)#this for new entry
    display_button=Button(root,text='Get Attndence',command=get_attendence_page)#this is for delete any rec

    attendence_button.grid(row=0,column=0)
    entry_button.grid(row=1,column=0)
    display_button.grid(row=2,column=0)




def get_attendence_page():#to save date of attendence
    global attendence_button
    global entry_button
    global display_button

    global home_button
    global date_entry_by_user
    global button_to_get_attendence
    global date_entry_var

    date_entry_var=StringVar()

    attendence_button.grid_forget()
    display_button.grid_forget()
    entry_button.grid_forget()

    home_button=Button(root,text='back',command=home2)
    home_button.grid(row=0,column=0)

    date_entry_by_user=Entry(root,width='50')
    date_entry_by_user.grid(row=1,column=1)

    button_to_get_attendence=Button(root,text='Get attendence',command=lambda: diaplay_attendence(date_entry_by_user.get()))
    button_to_get_attendence.grid(row=1,column=2)

    date_entry_var=date_entry_by_user.get()



def to_log_attendence(names_to_save):#saves the attendence in the logtxt file
    file_to_open_log=open('log.txt','a+')
    d1=strftime("%d/%m/%y")
    file_to_open_log.write(d1+',')
    for i in range(len(names_to_save)-1):
        file_to_open_log.write(names_to_save[i+1]+',')
    file_to_open_log.write('  ||  ')

    home3()


def to_take_attendence():#take as attendence


    global attendence_button
    global display_button
    global entry_button
    
    global home_button_2
    global attendence_list_label
    global button_to_save_std_data

    entry_button.grid_forget()
    attendence_button.grid_forget()
    display_button.grid_forget()


 #########################################################################################################################################################################

    pic = []
    names = []
    List = os.listdir("ImagesAttendence")
    #print(List)
    for i in List:
        temp = cv2.imread(f'{"ImagesAttendence"}/{i}')
        pic.append(temp)
        names.append(os.path.splitext(i)[0])
    #print(names)

    encodedList = fEncode(pic)

    clear()

    vid = cv2.VideoCapture(0)

    while True:
        check, frame = vid.read()
        img = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        curpic = face_recognition.face_locations(img)
        cdcurpic = face_recognition.face_encodings(img, curpic)

        for encode, fl in zip(cdcurpic, curpic):
            same = face_recognition.compare_faces(encodedList, encode)
            fd = face_recognition.face_distance(encodedList, encode)
            pos = np.argmin(fd)

            if same[pos]:
                n = names[pos].upper()
                y1, x2, y2, x1 = fl
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (255, 0, 0), cv2.FILLED)
                cv2.putText(frame, n, (x1 + 4, y2 - 4), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
                register(n)
        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break

    vid.release()
    cv2.destroyAllWindows()

    #################################################################################################################################################################################


    names_string=''
    names_to_add_in_csv_file=[]
    with open('Attendance.csv','r+') as f:
        p=f.readlines()
        for i in p:
            c=i.split(',')
            names_string+=c[0]+'\n'
            names_to_add_in_csv_file.append(c[0])

    home_button_2=Button(root,text='home',command=home3)
    home_button_2.grid(row=0,column=0)

    attendence_list_label=Label(root,text=names_string)
    attendence_list_label.grid(row=1,column=1)

    button_to_save_std_data=Button(root,text='SAVE',command=lambda: to_log_attendence(names_to_add_in_csv_file))
    button_to_save_std_data.grid(row=2,column=1)



def store_info():#used to save the details to info.txt file

    global roll_number_entry
    global name_entry
    global gender_var
    global date_var
    global month_var
    global year_var

    roll=roll_number_entry.get()
    name=name_entry.get()
    gender=gender_var.get()
    dob=str(date_var)+'/'+str(month_var)+'/'+str(year_var)

    f=open('info.txt','a+')

    rite=roll+','+name+','+dob+','+gender+' || '

    f.write(rite)
    f.close()

    home1()#this is to go back to home page


def to_save_image_in_file():#used to save the image in the file

    global image_path
    global roll_number_entry
    global image_var

    os.rename(image_path,'ImagesAttendence/'+roll_number_entry.get()+'.jpg')

    store_info()#this is to save other data


def open_dialoge_box_to_select_picture():
    global picture_label
    global image_path
    global image_var

    picture_label.grid_forget()

    image_path=filedialog.askopenfilename(title='Select Picture Of Student')
    image_var=ImageTk.PhotoImage(Image.open(image_path))
    picture_label=Label(image=image_var)

    picture_label.grid(row=6,column=1,columnspan=3)

def home1():#to return from entry window
    global name_label
    global roll_label
    global DOB_label
    global gender_label
    global home_button

    global attendence_button
    global display_button
    global entry_button

    global name_entry
    global roll_number_entry

    global gender_var

    global gender_female_button
    global gender_male_button

    global date_menu
    global month_menu
    global year_menu

    global select_picture_button
    global picture_label

    global submit_button

    select_picture_button.grid_forget()
    picture_label.grid_forget()

    year_menu.grid_forget()
    month_menu.grid_forget()
    date_menu.grid_forget()

    name_label.grid_forget()
    roll_label.grid_forget()
    DOB_label.grid_forget()
    gender_label.grid_forget()
    home_button.grid_forget()

    name_entry.grid_forget()
    roll_number_entry.grid_forget()

    gender_male_button.grid_forget()
    gender_female_button.grid_forget()

    submit_button.grid_forget()

    attendence_button=Button(root,text='Attendence',command=to_take_attendence)#this for attendence
    entry_button=Button(root,text='enter new',command=enter_new_page)#this for new entry
    display_button=Button(root,text='Get Attendence',command=get_attendence_page)#this is for delete any rec

    attendence_button.grid(row=0,column=0)
    entry_button.grid(row=1,column=0)
    display_button.grid(row=2,column=0)


def enter_new_page():#to entry new window
    global name_label
    global roll_label
    global DOB_label
    global gender_label
    global home_button

    global attendence_button
    global display_button
    global entry_button

    global name_entry
    global roll_number_entry

    global gender_var

    global gender_female_button
    global gender_male_button

    global date_var
    global month_var
    global year_var
    global date_menu
    global month_menu
    global year_menu

    global select_picture_button
    global picture_label
    global image_path
    global image_var

    global submit_button

    gender_var.set('empty')

    date_var=IntVar()
    month_var=IntVar()
    year_var=IntVar()

    attendence_button.grid_forget()
    entry_button.grid_forget()
    display_button.grid_forget()

    year_list=[]
    for i in range(2000,2023):
        year_list.append(i)
    month_list=[1,2,3,4,5,6,7,8,9,10,11,12]
    date_list=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]

    name_label=Label(root,text='Name: ')
    roll_label=Label(root,text='Roll: ')
    DOB_label=Label(root,text='DOB: ')
    gender_label=Label(root,text='Gender')
    home_button=Button(root,text='Home',command=home1)

    name_entry=Entry(root)
    roll_number_entry=Entry(root)

    gender_male_button=Radiobutton(root,text='Male',variable=gender_var,value='male')
    gender_female_button=Radiobutton(root,text='Female',variable=gender_var,value='female')
    gender_empty_button=Radiobutton(root,text='',variable=gender_var,value='empty')

    date_menu=OptionMenu(root,date_var,*date_list)
    month_menu=OptionMenu(root,month_var,*month_list)
    year_menu=OptionMenu(root,year_var,*year_list)

    image_path=ImageTk.PhotoImage(Image.open('photo/any.jpg'))
    picture_label=Label(root,image=image_path)
    select_picture_button=Button(root,text='Select a Picture',command=open_dialoge_box_to_select_picture)
    
    submit_button=Button(root,text='Submit',command=to_save_image_in_file)

    date_menu.grid(row=4,column=2)
    month_menu.grid(row=4,column=3)
    year_menu.grid(row=4,column=4)

    name_label.grid(row=1,column=1)
    roll_label.grid(row=2,column=1)
    DOB_label.grid(row=4,column=1)
    gender_label.grid(row=3,column=1)
    home_button.grid(row=0,column=0)

    name_entry.grid(row=1,column=2,columnspan=3)
    roll_number_entry.grid(row=2,column=2,columnspan=3)

    gender_female_button.grid(row=3,column=3)
    gender_male_button.grid(row=3,column=2)

    select_picture_button.grid(row=5,column=1,columnspan=3)
    picture_label.grid(row=6,column=1,columnspan=3)

    submit_button.grid(row=7,column=1,columnspan=3)

root = Tk()
root.title('Attendence System')
icon_photo=PhotoImage(file = "icon.png")
root.iconphoto(False, icon_photo)

#home page code.
gender_var=StringVar()#this for gender
attendence_button=Button(root,text='Attendence',command=to_take_attendence)#this for attendence
entry_button=Button(root,text='enter new',command=enter_new_page)#this for new entry
display_button=Button(root,text='Get Attendence',command=get_attendence_page)#this is for delete any rec


attendence_button.grid(row=0,column=0)
entry_button.grid(row=1,column=0)
display_button.grid(row=2,column=0)



root.mainloop()#mainloop