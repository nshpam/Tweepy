from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkcalendar import *
# create widget
root = Tk()
# title name
root.title("Tweet Harvest")
root.config(bg="#2E2D2E")
# widget size wide*tall
root.geometry('900x600')
# letter position
headLabel = Label(text='Twitter API Scraper',font=("Monospace",20,"bold"),bg='#2E2D2E',fg='white').grid(row=0,column=0)
search_title = Label(text='Search Input',font=("Yu Gothic UI",10,"bold"),bg='#2E2D2E',fg='white').grid(row=1,column=0)
# text label
txt = StringVar()
search_txt = Entry(root,textvariable = txt,width=40,bg="#636163").grid(row=2,column=0,padx=10,pady=5,ipady=100)
# progressbar
search_uploading_bar = Progressbar(root,orient='horizontal',mode='determinate',length=245).grid(padx=10)
# button
button_cancel = Button(root,text="Cancel",font=("Yu Gothic UI",10,"bold"),width=29,bg='#4E4C4E',fg='white',border=0).grid(row=4,column=0,pady=5)
# label frame
lf = LabelFrame(root, text='Type Selection',font=("Yu Gothic UI",10,"bold"),bg='#2E2D2E',fg='white')
lf.grid(column=0, row=5, padx=20, pady=20)

alignment_var = StringVar()
alignments = ('Hashtag', 'Word')

# create radio buttons and place them on the label frame
grid_column = 0
for alignment in alignments:
    # create a radio button
    radio = Radiobutton(lf, text=alignment, value=alignment, variable=alignment_var,bg='#2E2D2E',fg='white',font=("Yu Gothic UI",10,"bold"),width=9)
    radio.grid(column=grid_column, row=6, ipadx=10, ipady=10)
    # grid column
    grid_column += 1

# Tabbed Widget
# Creating Tab Control
tabControl = ttk.Notebook(root,width=590,height=550)
tab_color = "#1F1E1F"
ttk.Style().configure("TNotebook", background=tab_color );
# Creating the tabs
tab_scraper_task = Frame(tabControl)
tab_analyze_data = Frame(tabControl)
tab_analyze_overall = Frame(tabControl)
# Adding the tab
tabControl.add(tab_scraper_task,text='Scraper Task')
tabControl.add(tab_analyze_data,text='Analyze Data')
tabControl.add(tab_analyze_overall,text='Analyze Overall Sentiment')
# Packing the tab control to make the tabs visible
tabControl.grid(row=0,column=1,padx=10,pady=10,rowspan=50,columnspan=3)

Label(tab_scraper_task).grid(row=0,column=1)
Label(tab_analyze_data).grid(row=0,column=1)
Label(tab_analyze_overall).grid(row=0,column=1)

# calendar
calendar = Calendar(tab_scraper_task, selectmode="day",year =2023,month=1,day=15,font=("Yu Gothic UI",10,"bold"))
calendar.grid(row=1,column=1)

def grab_date():
    calendar_label.config(text="Scrap Tweets Created At Date "+calendar.get_date(),font=("Yu Gothic UI",10,"bold"))
calendar_button = Button(tab_scraper_task, text="Get Date", command=grab_date,font=("Yu Gothic UI",10,"bold"),width=31,bg='#4E4C4E',fg='white',border=0)
calendar_button.grid(row=2,column=1,pady=10)

calendar_label = Label(tab_scraper_task, text="")
calendar_label.grid(row=3,column=1)

lf_tweet_count_limit = LabelFrame(tab_scraper_task, text='Tweet Count Limit',font=("Yu Gothic UI",15,"bold"))
lf_tweet_count_limit.grid(column=1, row=4,padx=10)
num_tweet = IntVar()
text_tweet_count_limit = Entry(lf_tweet_count_limit,textvariable = num_tweet,font=("Yu Gothic UI",10,"bold"),bg="#636163",fg="white",width=48).grid(row=1,column=4,padx=10,pady=5)

lf_note = LabelFrame(tab_scraper_task,text='Note',font=("Yu Gothic UI",15,"bold"))
lf_note.grid(row=5,column=1,padx=10)

text_note = Label(lf_note,text='You can not scrap tweet that is created more than a week',font=("Yu Gothic UI",10,"bold"),fg="red").grid(row=5,column=1)
button_scrap_tweet = Button(tab_scraper_task,text='Create API Scrap Task',font=("Yu Gothic UI",10,"bold"),width=20,bg='#4E4C4E',fg='white',border=0).grid(row=6,column=2,pady=10)

# run program
root.mainloop()

