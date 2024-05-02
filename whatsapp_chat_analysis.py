import streamlit as st
import preprocessor, Helper
import matplotlib.pyplot as plt
import seaborn as sns
def main():
    st.sidebar.title("PYTHONJN")

    uploaded_file = st.sidebar.file_uploader("choose a file")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)


    #fetch unique users
        user_list = df['user'].unique().tolist()
        user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0,"Overall")

        selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

        if st.sidebar.button("Show Analysis"):

           #stats area
            num_messages, words, num_media_messages, num_links = Helper.fetch_stats(selected_user,df)

            st.title("Top Statistics")

            col1,col2,col3,col4 = st.columns(4)
            
            with col1:
                st.header("Total Messages")
                st.title(num_messages)
                
            with col2:
                st.header("Total Words")
                st.title(words)
            with col3:
                st.header("Media Shared")
                st.title(num_media_messages)
            with col4:
                st.header("Links Shared")
                st.title(num_links)

            # monthly timeline
            st.title("Monthly Timeline")
            timeline = Helper.monthly_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.plot(timeline['time'],timeline['message'], color = 'red')
            plt.xticks(rotation= 'vertical')
            st.pyplot(fig)

            #daily timeline
            st.title("Daily Timeline")
            daily_timeline = Helper.daily_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.plot(daily_timeline['only_date'],daily_timeline['message'], color = 'black')
            plt.xticks(rotation= 'vertical')
            st.pyplot(fig)

            #activity map
            st.title('Activity Map')
            col1,col2 = st.columns(2)

            with col1:
                st.header("Most busy day")
                busy_day = Helper.week_activity_map(selected_user,df)
                fig,ax = plt.subplots()
                ax.bar(busy_day.index,busy_day.values)
                st.pyplot(fig)

            with col2:
                st.header("Most busy month")
                busy_month = Helper.month_activity_map(selected_user,df)
                fig,ax = plt.subplots()
                ax.bar(busy_month.index,busy_month.values,color = 'pink')
                plt.xticks(rotation= 'vertical')
                st.pyplot(fig)

            
            st.title("Weekly Activity Map")
            # user_heatmap = Helper.activity_heatmap(selected_user,df)
            # fig,ax = plt.subplots()
            # ax = sns.heatmap(user_heatmap)
            # st.pyplot(fig)
            # st.pyplot(sns.heatmap(user_heatmap))

            user_heatmap = Helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots()
            # Plot the heatmap
            sns.heatmap(user_heatmap, ax=ax)
            # Display the figure using Streamlit
            st.pyplot(fig)

       
            #finding the busiest users in the group(group level)
            if selected_user == 'Overall':
                st.title('Most Busy Users')
                x, new_df = Helper.most_busy_users(df)
                fig, ax = plt.subplots()
                
                col1,col2 = st.columns(2)

                with col1:
                    ax.bar(x.index,x.values,color= 'purple')
                    plt.xticks(rotation= 'vertical')
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)
            #WordCloud
            st.title("Wordcloud")
            df_wc = Helper.create_wordcloud(selected_user,df)
            fig,ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            #most common words
            most_common_df = Helper.most_common_word(selected_user, df)
            
            fig,ax = plt.subplots()

            ax.barh(most_common_df[0],most_common_df[1])
            plt.xticks(rotation= 'vertical')

            st.title('Most common words')
            st.pyplot(fig)

            #emoji analysis
            emoji_df = Helper.emoji_Helper(selected_user,df)
            st.title("Emoji Analysis")

            col1,col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig,ax = plt.subplots()
                ax.pie(emoji_df[1],labels=emoji_df[0],autopct= "%0.2f")
                st.pyplot(fig)

if __name__=="__main__":
    main()

