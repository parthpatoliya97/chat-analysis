from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
extractor=URLExtract()

def fetch_stats(selected_user,df):
    if selected_user!="Overall":
        
        new_df=df[df["user"]==selected_user]
        
    else:
        new_df=df
    #num of message
    num_message= new_df.shape[0]
    # no of words:
    words=[]
    for message in new_df["message"]:
        words.extend(message.split())
        num_words=len(words)
        
    #fetch no of media message:
    
    no_of_media_message=new_df[df["message"]=="<Media omitted>"].shape[0]
    
    #fetch no of links:
    
    links=[]
    for message in new_df["message"]:
        links.extend(extractor.find_urls(message))
        no_of_links=len(links)
    return num_message,num_words,no_of_media_message,no_of_links,


def dataframe(selected_user,df):
    if selected_user!="Overall":
            
        new_df=df[df["user"]==selected_user]
        
    else:
        new_df=df
    return new_df

def fetch_most_busy_user(df):
    x=df["user"].value_counts().head()
    df=round((df["user"].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={"user":"name","count":"percent"})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user!="Overall":
        
        new_df=df[df["user"]==selected_user]
        
    else:
        new_df=df
    f=open("stop_hinglish.txt",'r')
    stop_words=f.read()
    
    temp=new_df[new_df["user"]!='Group Notification']
    temp=temp[temp["message"]!="<Media omitted>"]
    
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
        
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color="white")
    temp["message"].apply(remove_stop_words)
    
    df_wc=wc.generate(temp["message"].str.cat(sep=" "))
    return df_wc

def most_comman_words(selected_user,df):
    
    f=open("stop_hinglish.txt",'r')
    stop_words=f.read()
    if selected_user!="Overall":
        
        new_df=df[df["user"]==selected_user]
        
    else:
        new_df=df
        
        #remove Group Notification and Media Ommitted
    temp=new_df[new_df["user"]!='Group Notification']
    temp=temp[temp["message"]!="<Media omitted>"]
        
    words=[]
    for message in temp["message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
                    
        
    df= pd.DataFrame(Counter(words).most_common(20))
    return df



def Emogi_helper(selected_user,df):
    if selected_user!="Overall":
        
        new_df=df[df["user"]==selected_user]
        
    else:
        new_df=df
        
    def extract_emojis(text):
        return [char for char in text if char in emoji.EMOJI_DATA]
    all_emojis = df['message'].apply(extract_emojis)
    flattened_emojis = [item for sublist in all_emojis for item in sublist]
    emoji_counter = Counter(flattened_emojis).most_common(len(Counter(flattened_emojis)))
    emogi_df=pd.DataFrame(emoji_counter)
    
    return emogi_df

def monthly_timeline(selected_user,df):
    if selected_user!="Overall":
        
        new_df=df[df["user"]==selected_user]
        
    else:
        new_df=df
    
    df["month_num"]=df["date"].dt.month    
    timeline=df.groupby(["year","month_num","month"]).count()["message"].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline["month"][i] + "-" +str(timeline["year"][i]))
    timeline["time"]=time
    
    return timeline
        
def daily_timeline(selected_user,df):
    if selected_user!="Overall":
        
        new_df=df[df["user"]==selected_user]
        
    else:
        new_df=df
    
    df["only-date"]=df["date"].dt.date    
    daily_timeline=df.groupby(["only-date"]).count().reset_index()
   
    
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user!="Overall":
        
        new_df=df[df["user"]==selected_user]
        
    else:
        new_df=df
        
    new_df["day_name"]=new_df["date"].dt.day_name()
    
    return new_df["day_name"].value_counts()

def month_activity_map(selected_user,df):
    if selected_user!="Overall":
            
        new_df=df[df["user"]==selected_user]
        
    else:
        new_df=df
        
    return new_df["month"].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user!="Overall":
            
        new_df=df[df["user"]==selected_user]
        
    else:
        new_df=df
    new_df["day_name"]=new_df["date"].dt.day_name()
        
    period=[]
    for hour in new_df[["day_name","hour"]]["hour"]:
        if hour==23:
            period.append(str(hour) + "-" +str("00"))
        elif hour==0:
            period.append(str(hour) + "-" +str(hour+1))
        else:
            period.append(str(hour)+ "-"+ str(hour+1))
    new_df["period"]=period
    return new_df.pivot_table(index="day_name",columns="period",values="message",aggfunc="count").fillna(0)

        
        
    
        
    
    
    
    
    

    