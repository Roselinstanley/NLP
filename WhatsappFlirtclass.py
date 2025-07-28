import pandas as pd
import emoji
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
class WhatsappFlirt:
    def __init__(self):
        pass

    def get_emoji_free_text(self, text):
        return emoji.replace_emoji(text, replace='')

    def deemojify(self, text):
        return text.encode('ascii', 'ignore').decode('ascii')

    def assign_emoji(self, text, dataset):
        dataset = dataset.copy()
        dataset.loc[[i for i, x in enumerate(text) if x == 0], 'Chat'] = 'Emoji'
        return dataset

    def TalkerChecking(self, Unique_Frequency_Talker, flirt_words):
        return Unique_Frequency_Talker.loc[Unique_Frequency_Talker.index.str.lower().isin([w.lower() for w in flirt_words])]

    def LesserChecking(self, Unique_Frequency_Lesser, flirt_words):
        return Unique_Frequency_Lesser.loc[Unique_Frequency_Lesser.index.str.lower().isin([w.lower() for w in flirt_words])]

    def whole_process(self, dataset):
        # Clean and process chat dataset
        dataset = dataset.dropna(subset=['Date', 'Time', 'Name', 'Chat'])
        dataset['Chat'] = dataset['Chat'].apply(lambda x: self.get_emoji_free_text(str(x)))
        dataset['TW'] = dataset['Chat'].str.split().str.len()
        dataset.index = range(dataset.shape[0])
        dataset = self.assign_emoji(dataset.TW, dataset)

        # Identify most and least talkative persons
        Talker = dataset['Name'].value_counts().idxmax()
        Less_Talker = dataset['Name'].value_counts().idxmin()

        print("Most Talkative Person :", Talker.upper())
        print("Less Talkative Person :", Less_Talker.upper())

        # Extract messages of talker and lesser talker
        Talker_chat = dataset[dataset['Name'] == Talker]
        Less_chat = dataset[dataset['Name'] == Less_Talker]

        # Get word frequencies
        Unique_Frequency_Talker = pd.DataFrame(Talker_chat['Chat'].str.split(expand=True).stack().value_counts())
        Unique_Frequency_Talker.columns = ['count']
        Unique_Frequency_Lesser = pd.DataFrame(Less_chat['Chat'].str.split(expand=True).stack().value_counts())
        Unique_Frequency_Lesser.columns = ['count']

        flirt_words = [
            'kiss', 'hug', 'date', 'cute', 'beautiful', 'sexy', 'hot', 'adorable', 'uma', 'darling',
            'fuck', 'porn', 'x', 'sex', 'matter', 'nipple', 'virgin', 'sperm', 'seduce', 'condom', 'kk'
        ]

        # Initialize outputs
        Talker_out = 0
        Less_out = 0
        Talker_Filter_list = pd.DataFrame()
        Less_Filter_list = pd.DataFrame()

        # Process Talker
        try:
            Talker_Filter_list = self.TalkerChecking(Unique_Frequency_Talker, flirt_words)
            if not Talker_Filter_list.empty:
                Talker_Filter_list = Talker_Filter_list.copy()
                Talker_Filter_list.columns = ['Repeated_count']
                Talker_Filter_list['Flirt_Frequency'] = (Talker_Filter_list['Repeated_count'] / Talker_chat['TW'].sum()) * 100
                Talker_out = round(Talker_Filter_list['Flirt_Frequency'].mean(), 2)
                print(f"Flirting Percentage of {Talker.upper()}: {Talker_out} %")
            else:
                print(f"Wonderful, no flirting by {Talker.upper()}")
        except Exception as e:
            print(f"Error processing flirting for {Talker.upper()}: {e}")

        # Process Lesser Talker
        try:
            Less_Filter_list = self.LesserChecking(Unique_Frequency_Lesser, flirt_words)
            if not Less_Filter_list.empty:
                Less_Filter_list = Less_Filter_list.copy()
                Less_Filter_list.columns = ['Repeated_count']
                Less_Filter_list['Flirt_Frequency'] = (Less_Filter_list['Repeated_count'] / Less_chat['TW'].sum()) * 100
                Less_out = round(Less_Filter_list['Flirt_Frequency'].mean(), 2)
                print(f"Flirting Percentage of {Less_Talker.upper()}: {Less_out} %")
            else:
                print(f"Wonderful, no flirting by {Less_Talker.upper()}")
        except Exception as e:
            print(f"Error processing flirting for {Less_Talker.upper()}: {e}")

        # Return clean structured result
        return {
            'Talker': {
                'Name': Talker.upper(),
                'Flirting_Score': Talker_out,
                'Filtered_Words': Talker_Filter_list
            },
            'Lesser_Talker': {
                'Name': Less_Talker.upper(),
                'Flirting_Score': Less_out,
                'Filtered_Words': Less_Filter_list
            }
        }
    def statsWhatsApp(self, dataset):
        stats = []   # Basic statistics
        stats1 = []  # "Freaks" (most media sender, message deleter etc.)
    
        # 1. 📅 Most Active Date
        date_chart = pd.DataFrame(dataset["Date"].value_counts())
        most_active_date = dataset["Date"].value_counts().idxmax()
        stats.append(most_active_date)
    
        # 🗓️ Day of the Week (for the most active date)
        l = list(map(int, most_active_date.split('/')))
        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday = datetime.date(l[2], l[0], l[1]).weekday()
        stats.append(week_days[weekday])
    
        # ⏰ Most Active Time of Day
        most_active_time = dataset["Time"].value_counts().idxmax()
        stats.append(most_active_time)
    
        # 📊 Average Messages Per Day
        avg_msgs_per_day = round(dataset["Date"].count() / dataset["Date"].nunique())
        stats.append(avg_msgs_per_day)
    
        # 📈 Plot: Messages per date by name
        plt.clf()
        ax1 = sns.countplot(x='Date', hue='Name', data=dataset)
        ax1.tick_params(axis='x', rotation=40)  # ✅ Use this instead of set_xticklabels
        plt.tight_layout()
        plt.show()
    
        # 2. 📷 Media Sharing Freak
        media = dataset[dataset["Chat"] == "<media omitted>"]
        if not media.empty:
            media_count = media["Name"].value_counts().to_frame(name="Media Shared")
            media_freak = media["Name"].value_counts().idxmax()
        else:
            media_count = pd.DataFrame()
            media_freak = "No Media Shared"
            stats1.append(media_freak)
    
        # 3. ❌ Message Deletion Freak
        deleted = dataset[dataset["Chat"] == "this message was deleted"]
        if not deleted.empty:
            deleted_count = deleted["Name"].value_counts().to_frame(name="Messages Deleted")
            delete_freak = deleted["Name"].value_counts().idxmax()
        else:
            deleted_count = pd.DataFrame()
            delete_freak = "No Message Deleted"
            stats1.append(delete_freak)
    
        # 4. 📞 Missed Voice Call Freak
        voice_calls = dataset[dataset["Chat"] == "missed voice call"]
        if not voice_calls.empty:
            voice_call_count = voice_calls["Name"].value_counts().to_frame(name="Missed Voice Calls")
            voice_call_freak = voice_calls["Name"].value_counts().idxmax()
        else:
            voice_call_count = pd.DataFrame()
            voice_call_freak = "No Missed Voice Call"
            stats1.append(voice_call_freak)
    
        # 5. 📹 Missed Video Call Freak
        video_calls = dataset[dataset["Chat"] == "missed video call"]
        if not video_calls.empty:
            video_call_count = video_calls["Name"].value_counts().to_frame(name="Missed Video Calls")
            video_call_freak = video_calls["Name"].value_counts().idxmax()
        else:
            video_call_count = pd.DataFrame()
            video_call_freak = "No Missed Video Call"
            stats1.append(video_call_freak)
    
        # ✅ Return all statistics
        return {
            "date_chart": date_chart,
            "media_count": media_count,
            "deleted_count": deleted_count,
            "voice_call_count": voice_call_count,
            "video_call_count": video_call_count,
            "summary_stats": {
                "Most Active Date": most_active_date,
                "Active Weekday": week_days[weekday],
                "Most Active Time": most_active_time,
                "Avg Messages Per Day": avg_msgs_per_day
                },
            "freaks": {
                "Media Share Freak": media_freak,
                "Message Deletion Freak": delete_freak,
                "Voice Call Freak": voice_call_freak,
                "Video Call Freak": video_call_freak
                }
             }
        