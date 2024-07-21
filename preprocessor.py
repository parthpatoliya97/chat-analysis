import re 
import pandas as pd

def preprocess(data):
    data=data
    # f=open("WhatsApp Chat with SEM-6_DIV-B_COMP.txt",'r',encoding='utf-8')
    # data=f.read()
    pattern = r'(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{2}\s?[APM]{2}) - (.*)'

    # Using re.findall to find all matches
    matches = re.findall(pattern, data)

    # Lists to hold dates and times, and messages
    date_time_list = []
    message_list = []

    # Extract and append each part to respective lists
    for match in matches:
        date_time, time, message = match
        combined_date_time = f"{date_time}, {time}"
        date_time_list.append(combined_date_time)
        message_list.append(message)
        
    df=pd.DataFrame({"user_mesage":message_list,"message_date":date_time_list})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p')
    df.rename(columns={"message_date":"date"},inplace=True)
    
    users = []
    messages = []

    pattern = r'^(.*?):\s*(.*)$'
    for message in df["user_mesage"]:
        entry = re.split(pattern,message )
        if entry[1:]:
        
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("Group Notification")
            messages.append(entry[0])
    df["user"]=users
    df["message"]=messages
    df.drop("user_mesage",axis=1,inplace=True)
    df["year"]=df["date"].dt.year
    df["month"]=df["date"].dt.month_name()
    df["day"]=df["date"].dt.day
    df["hour"]=df["date"].dt.hour
    df["minute"]=df["date"].dt.minute
    
    return df
    
    
