#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 17:39:28 2022

@author: o
"""

    
import pandas as pd

# July 4th is saturday, so, the holiday is July 5th
# https://elpaso.ttuhsc.edu/the-scope/excellence/2021-2022-holiday-schedule.aspx
HOLIDAY = pd.to_datetime(["2021-07-05","2021-9-6","2021-11-22","2021-11-25","2021-11-26","2021-11-25","2021-12-24","2021-12-27","2021-12-31","2022-1-17","2021-5-30","2021-1-1"])

# From 8 AM to 5 PM
WORK_HOUR = pd.to_datetime(["8:00:00","17:00:00"])
#
NEW_YEAR = pd.to_datetime(["2021-12-30 17:00:00","2022-1-2 08:00:00"])


df = pd.read_csv("~/Downloads/CD_report.csv")


df["start"] = pd.to_datetime(df['Created Date'])
df["end"] = pd.to_datetime(df['Finish Date'])
df["report"] = pd.to_datetime(df['Completion Date'])


################################################

# get the business day range
#pd.bdate_range('2011-01-05', '2011-01-09')

def get_business_mins(start,end): # the same year
    """

    Parameters
    ----------
    start : TYPE datetime
        start time of a work order.
    end : TYPE datetime
        finish time of a work order.

    Returns
    -------
    the period between those two time.

    """
    if start > end:
        return print("start should before end.")
    if start.day == end.day and start.month == end.month:
        return int((end-start).total_seconds()/60)
    else:
        diff_dates_list_1 = pd.bdate_range(str(start),str(end))
        diff_dates_list = []
        for i in range(0, len(diff_dates_list_1)):
            if diff_dates_list_1[i] not in HOLIDAY:
                diff_dates_list.append(diff_dates_list_1[i])
        diff_dates_nums = len(diff_dates_list)
        #### end.hour < start.hour
        diff_min = 0   
        diff_hour = 0
        if end.minute < start.minute: 
            diff_hour -= 1
            diff_min += end.minute
            diff_min += 60 - start.minute
        else:
            diff_min = end.minute - start.minute
        if end.hour < start.hour:
            if start.hour < WORK_HOUR[0].hour: # change the start time before 8 am to 8am
                start_hour = WORK_HOUR[0].hour
            elif start.hour > WORK_HOUR[1].hour: # change the start time after 8am to next day 8am, 
                start_hour = WORK_HOUR[1].hour
            else:
                start_hour = start.hour
            if end.hour < WORK_HOUR[0].hour:
                end_hour = WORK_HOUR[0].hour  # change the finish time before 8 am to 8 am.
            elif end.hour > WORK_HOUR[1].hour:
                end_hour = WORK_HOUR[1].hour
            else: 
                end_hour = end.hour
            #print(end_hour,start_hour,diff_hour)
            diff_dates_nums -= 1 # because end hour before start hour, day-1
            #print(diff_hour)
            diff_hour = diff_hour + end_hour - WORK_HOUR[0].hour # end hour - 8 AM
            diff_hour += WORK_HOUR[1].hour - start_hour # 5 PM - start hour
        else:
            diff_hour = diff_hour + end.hour - start.hour
        ### end minute < start mintue:
        #print(diff_min)
        diff_min = max(diff_dates_nums-1,0) * 9 * 60 + min(diff_hour,9) * 60 + min(diff_min,60)
        if diff_min < 0:
            diff_min += 9 * 60
        #print(diff_dates_nums,diff_hour)
        return int(diff_min)
        


        
################################################


##################
# bug test 

d11 = pd.to_datetime('2021-07-28 14:09:00')
d12 = pd.to_datetime('2021-07-28 14:10:00')      
get_business_mins(d11,d12)


d11 = pd.to_datetime('2021-07-28 14:09:00')
d13 = pd.to_datetime('2021-07-29 10:09:00')  
get_business_mins(d11,d13)

d21 = pd.to_datetime('2021-07-4 14:09:00')
d22 = pd.to_datetime('2021-07-6 14:10:00')  
get_business_mins(d21,d22)


d31 = pd.to_datetime("2021-8-16 10:01:00")
d32 = pd.to_datetime("2021-8-17 9:00:00")
get_business_mins(d31,d32)



d41 = pd.to_datetime("2021-12-30 16:00:00")
d42 = pd.to_datetime("2022-1-2 9:00:00")
get_business_mins(d41,NEW_YEAR[0]) + get_business_mins(NEW_YEAR[1],d42)


##################


dif_min = []

for i in range(0,len(df["start"])):
        start = df["start"][i]
        end = df["end"][i]
        if start.year == 2021 and end.year == 2022:
            dif_min.append(get_business_mins(start,NEW_YEAR[0]) + get_business_mins(NEW_YEAR[1],end))
        else:    
            dif_min.append(get_business_mins(start,end))


df["Fin-Cre Mins"] = dif_min


     

dif_min = []

for i in range(0,len(df["start"])):
        start = df["end"][i]
        end = df["report"][i]
        if start.year == 2021 and end.year == 2022:
            dif_min.append(get_business_mins(start,NEW_YEAR[0]) + get_business_mins(NEW_YEAR[1],end))
        else:    
            dif_min.append(get_business_mins(start,end))


df["Rep-Fin Mins"] = dif_min
    
################################################
### working hour
a = []
for date in df["start"]:
    a.append(date.hour)
        
df["working hour creat"] = a     
        
        
b = []
for date in df["end"]:
    b.append(date.hour) 
    
    
df["working hour finish"] = b


        
c = []
for date in df["report"]:
    c.append(date.hour) 
    
    
df["working hour report"] = c       
        
df1 = pd.DataFrame(df)
df1.to_csv("~/Downloads/Final_Data.csv")



# Conpute non-regular working time percent
size = len(a)
counts = 0
for i in range(0,size):
    if a[i] < 8 or a[i] > 17:
        counts += 1

create_non_hours_rate = counts/size




size = len(b)
counts = 0
for i in range(0,size):
    if b[i] < 8 or b[i] > 17:
        counts += 1

finish_non_hours_rate = counts/size





size = len(c)
counts = 0
for i in range(0,size):
    if c[i] < 8 or c[i] > 17:
        counts += 1

report_non_hours_rate = counts/size



#### counts keywords
df1 = df[df["Building Name"]=="Coleman Hall -HS"]


df_request = df1["Request"]
req_txt = {}
for words in df_request:
    a = words.lower().split("this is a fire marshal work order")[1].replace("\n"," ")
    a = a.replace("."," ")
    a = a.replace(","," ")
    a = a.replace(";"," ")
    a = a.replace(":"," ")
    a = a.replace("'"," ")
    a = a.replace('"'," ")
    a = a.replace("\\"," ")
    a = a.replace("/"," ")
    a = a.replace("?"," ")
    a = a.replace(")"," ")
    a = a.replace("the"," ")
    """
    a = a.replace("following"," ")
    a = a.replace("have"," ")
    a = a.replace("wall"," ")
    a = a.replace("and"," ")
    a = a.replace("locations"," ")
    a = a.replace("that"," ")
    a = a.replace("need"," ")
    a = a.replace("to"," ")
    a = a.replace("to"," ")
    a = a.replace("with"," ")
    a = a.replace("this"," ")
    a = a.replace("area"," ")
    a = a.replace("is"," ")
    a = a.replace("for"," ")
    a = a.replace("fire"," ")
    a = a.replace("are"," ")
    a = a.replace("not"," ")
    a = a.replace("floor"," ")
    a = a.replace("by"," ")
    a = a.replace("photo"," ")
    a = a.replace("location"," ")
    a = a.replace("#"," ")
    a = a.replace("door"," ")
    a = a.replace("or"," ")
    a = a.replace("a"," ")
    a = a.replace("on"," ")
    a = a.replace("of"," ")
    a = a.replace("out"," ")
    a = a.replace("date"," ")
    a = a.replace("it"," ")
    a = a.replace("in"," ")
    a = a.replace("so"," ")
    """
    a = a.replace("&"," ")
    a = a.split(" ")
    for word in a:
        try:
            req_txt["{}".format(word)] += 1
        except KeyError:
            req_txt["{}".format(word)] = 1
            
with open('req_txt.csv', 'w') as f:
    f.write("Key,Counts \n")
    for key in req_txt:
        f.write('{},{}\n'.format(key, req_txt["{}".format(key)]) )

    



    
