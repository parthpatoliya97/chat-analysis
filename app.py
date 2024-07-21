import streamlit as st
import re
import pandas as pd
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    
    # st.dataframe(df)
    
    
    # fetch unique user
    
    user_list=df["user"].unique().tolist()
    user_list.remove("Group Notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    
    selected_user=st.sidebar.selectbox("Show analysis wrt ",user_list)
    df=helper.dataframe(selected_user,df)
    # st.dataframe(df)
    
    if st.sidebar.button("Show Analysis"):
        num_message,words,no_of_media_message,no_of_links=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2,col3,col4=st.columns(4)
        
        with col1:
            st.header("Total Message")
            st.title(num_message)
        with col2:
            st.header("Total Words")
            st.title(words)
            with col3:
                st.header("Media Shared")
                st.title(no_of_media_message)
            with col4:
                st.header("Link shared")
                st.title(no_of_links)
                
        # Montly timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline["time"],timeline["message"],color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        
        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline["only-date"],daily_timeline["message"],color="black")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        
        #Activity Map
        
        st.title("Activity Map")
        
        col1,col2=st.columns(2)
        
        with col1:
            st.header("Most Busy Day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
            
            
        with col2:
            st.header("Most Busy Month")
            busy_month=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color="orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
            
        
        st.title("Weekly Activation Function")
        heatmap=helper.activity_heatmap(selected_user,df)
        fig ,ax=plt.subplots()
        ax=sns.heatmap(heatmap)
        st.pyplot(fig)
            
            
        
        
        
        
        
        
        
        
        
        #finding the busiest user in the group
        if selected_user=="Overall":
            st.title("Most Busy User")
            x,df1=helper.fetch_most_busy_user(df)
            fig, ax = plt.subplots()
            
            col1,col2=st.columns(2)
            
            with col1:
                ax.bar(x.index,x.values,color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(df1)
        #Word Cloud
        st.title("WordCloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        #Most Comman Words
        st.title("Most Comman Words")
        most_comman_df=helper.most_comman_words(selected_user,df)
        
        fig,ax=plt.subplots()
        ax.barh(most_comman_df[0],most_comman_df[1])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        # st.dataframe(most_comman_df)
        
        #Emojies Analysis
        emoji_df=helper.Emogi_helper(selected_user,df)
        st.title("Emogi Analysis")
        col1,col2=st.columns(2)
        
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
    