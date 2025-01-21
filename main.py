# Module
import os
import csv
import pandas as pd
import numpy as np

# ตัวแปรทั่วไป
LECTURE = ['IT301', 'IT302', 'IT303', 'IT304']
LAB = ['LAB103', 'LAB104', 'LAB105', 'LAB106']
month_names = {1: "January", 2: "February", 3: "March", 4: "April",
               5: "May", 6: "June", 7: "July", 8: "August",
               9: "September", 10: "October", 11: "November", 12: "December"} 

# ตรวจสอบไฟล์ booking ไม่พบให้สร่้างใหม่
def check_file_exist():
    global booking_df
    header = ['id', 'fname', 'lname', 'roomtype', 'room', 'bookingdate','sorted_date']
    if not os.path.exists('studentbooking.csv'): 
        with open("studentbooking.csv", "w", newline="") as file:
            newfile = csv.writer(file)
            newfile.writerow(header)
    else:
        booking_df = pd.read_csv("studentbooking.csv")
      
#ฟังก์ชันตรวจสอบรหัสนักศึกษา '''
def checkvalid_IDstudent(ID_student):
    if ID_student in student_df["id"].values:
        return True
      
# ฟังก์ชันตรวจสอบวันที่ '''
def checkvalid_date(Bookingdate, month_names):
    check = Bookingdate.split("-")
    if len(check) == 3:
        for items in check:
            if not items.isdigit():
                print("Incorrect date format, should be DD-MM-YYYY")
                return True
        else:
            days, month, years = map(int, check)
            if month < 1 or month > 12:
                print("Please enter a month between 1-12 (January-December)")
                return True
            elif years > 9999 :
                print("Incorrect date format, should be DD-MM-YYYY")
                return True
            elif month in [1, 3, 5, 7, 8, 10, 12] and days > 31:
                print(f"On {month_names[month]} there are only 31 days")
                return True
            elif month in [4, 6, 9, 11] and days > 30:
                print(f"On {month_names[month]} there are only 30 days")
                return True
            elif month == 2:
                if (years % 400 == 0 or years % 4 == 0 and years % 100 != 0):
                    if days > 29:
                        print(f"Leap years have only 29 days")
                        return True
                elif days > 28:
                    print(f"{month_names[month]} in this year has only 28 days")
                    return True
    else:
        print("Incorrect date format, should be DD-MM-YYYY")
        return True
      
# สร้าง format dd-mm-yyyy 
def make_ddmmyyyy_format(Bookingdate):
    day,month,year = Bookingdate.split("-")
    if len(day) == 1:
        day = f"0{day}"
    if len(month) == 1:
        month = f"0{month}"
    Bookingdate = f"{day}-{month}-{year}"
    Sorted_date = f"{year}-{month}-{day}"
    return Bookingdate,Sorted_date
  
# ฟังก์ชันแสดงหน้าจอโปรแกรม '''
def UI():
    global student_df
    student_df = pd.read_csv("students.csv")
    check_file_exist()
    print("======================================================")
    print("             Student Room Booking System ")
    print("======================================================")
    print("  1  Print a list of students")
    print("  2  Submit a booking request")
    print("  3  Check the current booking via room number")
    print("  4  Check the available rooms via date")
    print("  5  Check booking with student ID")
    print("  6  Check booking with student first name")
    print("  7  Print booking summary")
    print("  0  Exit")
    print("======================================================")
  
# ฟังก์ชันแสดงรายชื่อนักศึกษา 
def func1_liststudentname():
    print(student_df)

# ฟังก์ชันการจองห้อง 
def func2_booking(LAB, LECTURE):
    ID_student = int(input("ID: "))
    if checkvalid_IDstudent(ID_student): 
        Roomtype = input("Roomtype (Lecture / Lab): ").upper()
        #รับประเภทของห้องจนกว่าจะถูก
        while True: 
            if Roomtype != 'LECTURE' and Roomtype != 'LAB': 
                print("Please enter Roomtype Lecture or Lab")
                Roomtype = input("Roomtype (Lecture / Lab): ").upper()
            else:
                break
        if  Roomtype == 'LECTURE':
            print(f"Room: {LECTURE}")
        elif Roomtype == 'LAB':
            print(f"Room: {LAB}")
        Room = input("Please select one room above: ").upper()
        #รับห้องจนกว่าจะถูก
        while True: 
            if (Roomtype == 'LECTURE') and Room not in LECTURE: 
                Room = input("Please enter a room according to the Lecture Room: ").upper()
            elif (Roomtype == 'LAB') and Room not in LAB:
                Room = input("Please enter a room according to the Lab Room: ").upper()
            else:
                break
        Bookingdate = input("Booking Date (DD-MM-YYYY): ")
        #รับวันที่จนกว่าจะถูก
        while True:
            if checkvalid_date(Bookingdate, month_names): 
                print("Please try again!!!")
                Bookingdate = input("Booking Date (DD-MM-YYYY): ")
            else:
                break
        #แปลง format ของวันที่
        if make_ddmmyyyy_format(Bookingdate): 
            Bookingdate, Sorted_date = make_ddmmyyyy_format(Bookingdate)
        for _,items in booking_df.iterrows():
            # ตรวจว่าห้องในวันที่รับเข้ามาถูกจองไปหรือยัง 
            if Room == items['room'] and Bookingdate == items['bookingdate']: 
                print(f'''
==========================================
   {Room} is not available on {Bookingdate}
==========================================
                    ''')
                return
        else:
            #บันทึกข้อมูลลง studentbooking.csv
            for _, value in student_df.iterrows(): 
                if ID_student == value['id']: 
                    fname = value['fname']
                    lname = value['lname']
                    newdata = {
                        'id': ID_student,
                        'fname': fname,
                        'lname': lname,
                        'roomtype': Roomtype,
                        'room': Room,
                        'bookingdate': Bookingdate,
                        'sortingdate': Sorted_date
                    }
                    booking_data = pd.DataFrame(newdata, index=[0])
                    booking_data.to_csv("studentbooking.csv", mode="a", header=False, index=False)
            print(f'''
========================
  Booking Successfully
========================
  ID:{ID_student}
  Firstname: {fname} 
  Lastname: {lname}
  Roomtype: {Roomtype}
  Room: {Room}
  Booking Date: {Bookingdate}
=========================
                  ''')
    else:
        print("You can't booking")
#ฟังก์ชันตรวจสอบห้องที่ถูกจอง
def func3_checkwithroom(LECTURE,LAB):
    booking_file = booking_df.sort_values(by='id')
    Room = input("Room: ").upper()
    #รับห้องจนกว่าจะถูก
    while Room not in LECTURE and Room not in LAB:
        print(f"Room {Room} does not exist in the system.")
        print(f"Lecture Rooms: {LECTURE}")
        print(f"Lab Rooms: {LAB}")
        print("Please select one room above.")
        Room = input("Room: ").upper()
    print("Current Booking: ")
    for _,value in booking_file.iterrows():
      if Room == value['room']:
         print(f"    Date: {value['bookingdate']} Student ID: {value['id']}")
    if Room not in booking_file['room'].values :
        print("    No booking")
      
#ฟังก์ชันตรวจสอบห้องที่ว่างด้วยวันที่
def func4_checkwithdate():
    lefLECTURE = np.array(['IT301', 'IT302', 'IT303', 'IT304'])
    lefLAB = np.array(['LAB103', 'LAB104', 'LAB105', 'LAB106'])
    #รับวันที่จนกว่าจะถูกต้อง
    Bookingdate = input("Booking Date (DD-MM-YYYY): ")
    while True:
        if checkvalid_date(Bookingdate, month_names):
            print("Please try again")
            Bookingdate = input("Booking Date (DD-MM-YYYY): ")
        else:
            break
    #แปลง format ของวันที่
    if make_ddmmyyyy_format(Bookingdate):
        Bookingdate, Sorted_date = make_ddmmyyyy_format(Bookingdate)
    #ดึงข้อมูลห้องที่ถูกจองของ LECTURE ตามในวันที่รับค่าเข้ามา
    booked_lecture_rooms = booking_df.loc[(booking_df['bookingdate'] == Bookingdate) & (booking_df['roomtype'] == 'LECTURE'), 'room'].values
    #ดึงข้อมูลห้องที่ถูกจองของ LAB ตามในวันที่รับค่าเข้ามา
    booked_lab_rooms = booking_df.loc[(booking_df['bookingdate'] == Bookingdate) & (booking_df['roomtype'] == 'LAB'), 'room'].values
    #ตรวจสอบถ้าในวันที่นั้นมีห้องที่ถูกจองจะนำข้อมูลที่มีไปลบใน lefLECTURE
    if len(booked_lecture_rooms) > 0:
        lefLECTURE = np.setdiff1d(lefLECTURE, booked_lecture_rooms, assume_unique=True)
    #ตรวจสอบถ้าในวันที่นั้นมีห้องที่ถูกจองจะนำข้อมูลที่มีไปลบใน lefLAB
    if len(booked_lab_rooms) > 0:
        lefLAB = np.setdiff1d(lefLAB, booked_lab_rooms, assume_unique=True)
    print("Available Room : ")
    print(f"     Lecture: {lefLECTURE}")
    print(f"     Lab:  {lefLAB}")

#ตรวจสอบการจองด้วยรหัสนักศึกษา
def func5_checkwithID():
    booking_file = booking_df.sort_values(by='sorted_date')
    ID_student = int(input("Student ID: "))
    if checkvalid_IDstudent(ID_student): 
        print("Current Booking: ")
        for _,values in booking_file.iterrows():
            if ID_student == values['id']:
                print(f"    Room: {values['room']} Date: {values['bookingdate']}")
            elif ID_student not in booking_file['id'].values:
                print("    No Booking")
                return
    else:
        print("ID student not match on students.csv file")
      
#ตรวจสอบการจองด้วยชื่อจริง
def func6_checkwithFname():
    data = []
    Nostudent = True
    booking_file = booking_df.sort_values(by='id')
    student_file = student_df.sort_values(by='id')
    firstname = input("Firstname: ").lower()
    #เก็บข้อมูลของคนที่มีประวัติการจอง
    for _,values in booking_file.iterrows() : 
        name = values['fname'].lower()
        if firstname in name : 
            data.append(values)
    #เก็บข้อมูลของคนที่ไม่มีประวัติการจอง
    for _,values in student_file.iterrows(): 
        name = values['fname'].lower()
        if values['id'] not in booking_file['id'].values and firstname in name :
            data.append(values)
    #แสดงผล
    for item in data:
        if item['id'] in booking_file.values:
            print(f"{item['id']} {item['fname']} {item['lname']}")
            print("    Current Booking: ")
            print(f"      Room:{item['room']} Date: {item['bookingdate']}") 
            print()
        else :
            print(f"{item['id']} {item['fname']} {item['lname']}")
            print("    Current Booking: ")
            print("      No bookings")
            print()
        Nostudent = False

    if Nostudent : 
        print("There is no student founds.")
#สรุปการจองของห้องทั้งหมด
def func7_summary(LECTURE, LAB):
    booking_file = booking_df.sort_values(by='sorted_date', ascending=True)
    print("Roomtype: LECTURE")
    for room in LECTURE:
        no_booking = True
        print(f"    {room}")
        for _, values in booking_file.iterrows():
            if values['roomtype'] == 'LECTURE' and values['room'] == room:
                print(f"        StudentID: {values['id']}  Date: {values['bookingdate']}")
                no_booking = False
        if no_booking:
            print("        No booking")
    print()
    print("Roomtype: LAB")
    for room in LAB:
        no_booking = True
        print(f"    {room}")
        for _, values in booking_file.iterrows():
            if values['roomtype'] == 'LAB' and values['room'] == room:
                print(f"        StudentID: {values['id']}  Date: {values['bookingdate']}")
                no_booking = False
        if no_booking:
            print("        No booking")

UI()
select = input("Option: ")
while True:
   if select == '1':
        func1_liststudentname()
   elif select == '2':
        func2_booking(LAB, LECTURE)
   elif select == '3':
        func3_checkwithroom(LECTURE,LAB)
   elif select == '4':
        func4_checkwithdate()
   elif select == '5':
        func5_checkwithID()
   elif select == '6':
        func6_checkwithFname()
   elif select == '7':
        func7_summary(LECTURE,LAB)
   elif select == '0':
        print("Thank you and goodbye")
        break
   else:
        print("Please enter function 1-7")
   UI()
   select = input("Option: ")