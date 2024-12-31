# A combination of pack and grid used to set out the user interface
#22/2/24 add query function to populate listbox
#Add Messagebox if no round number and set focus to g_round
#26/2/24 add select function to allow score entry
#Add insert score function and enabling of buttons etc using stringvar and
#Trace. 
# add update function to calculate total and update five_scores. Now test rounds 2 to 5 !! Done
# 27/2/24 Add golfer frame forget and grid, namevar and scorevar to control score entry and submit button
#Add cancel button functionality
#Add  insert_golfer (new golfer functionality) data entered correctly and enabling and disabling of buttons etc.
# Change round number check to include entry <1 and >5
#START OF VERSION CONTROL

from tkinter import *

from ttkbootstrap.constants import *
import ttkbootstrap as tb 
from ttkbootstrap.scrolled import ScrolledText, ScrolledFrame
import sqlite3
from sqlite3 import Error
from ttkbootstrap.dialogs import Messagebox

#root = tk.Tk()
root=tb.Window(themename="terry")

root.title("Stableford League")
root.geometry("1000x1000")

conn = sqlite3.connect("summer_cup2.db", detect_types=sqlite3.PARSE_DECLTYPES)


#top_frame3.pack_forget()
def goforit():
	pass
def query():

	if len(g_round.get()) == 0 or int(g_round.get()) < 1 or int(g_round.get()) >5:
		
		mb = Messagebox.show_error('You Must enter a round number between 1 and 5','Error')
		g_round.focus()
	else:
    
	    my_listbox.delete(0,'end')
	    c = conn.cursor()
	    c.execute("SELECT	*	FROM golfer ORDER BY name" )
	    records = c.fetchall()
	    # Loop through results
	    print_records = " "
	    for record in records:
	        my_listbox.insert(END, record)


	    conn.commit()
    #conn.close()

def update_total(conn, ident):
	c = conn.cursor()
	c.execute(""" SELECT score1,score2,score3,score4,score5 FROM five_scores
		WHERE golfer_id = :id """,
		{'id': ident})
	result = c.fetchall()
	print(result)
	total =  0
	scorelist = []
	for s in result:
		scorelist.append(s[0])
		scorelist.append(s[1])
		scorelist.append(s[2])
		scorelist.append(s[3])
		scorelist.append(s[4])
	


	  # find largest
	largest = max(scorelist)
	print(largest)
	# remove from list
	scorelist.remove(largest)
	# second largest
	largest2 = max(scorelist)
	# remove from list
	scorelist.remove(largest2)
	# third largest
	largest3 = max(scorelist)
	print(largest+largest2+largest3)
	total = (largest+largest2+largest3)
	c.execute("""UPDATE five_scores SET total_score = :tot
	WHERE golfer_id = :id""",
	{'tot': total, 'id': ident})

	conn.commit()





def select():
    #called from the Select button enters id into the id entry box

    x= my_listbox.get(ANCHOR)

    g_id.configure(state="normal")
    g_id.insert(END,x[0])
    g_newScore.configure(state="normal")
    g_newScore.focus()   

#------------------------------------------------------------------------------------------------------ 
def insert_golfer():   

    if g_name.get() is None:
        messagebox
   
    c = conn.cursor()
    try:
        c.execute("""INSERT INTO golfer (name)
						VALUES(:a) """,
              {
                  'a': g_name.get()
              }
              )
        gid = c.lastrowid

        c.execute("""INSERT INTO five_scores (score1, score2, score3, score4, score5, golfer_id)
                        VALUES(0, 0, 0, 0, 0, :a) """,
              {
                  'a': gid
              }
              )
        gid = c.lastrowid

       

        if int(g_round.get()) == 1:
            print('yahoo')
            

            c.execute("""UPDATE five_scores SET score1 = :sc1 WHERE golfer_id = :a """,
               
                 {
                      'a': gid,
                      'sc1': g_score.get()
                  })

            update_total(conn,gid)

        if int(g_round.get()) == 2:
            print('yahoo2')
            

            c.execute("""UPDATE five_scores SET score2 = :sc1 WHERE golfer_id = :a """,
               
                 {
                      'a': gid,
                      'sc1': g_score.get()
                  })
            update_total(conn,gid)
        if int(g_round.get()) == 3:
            print('yahoo2')
            

            c.execute("""UPDATE five_scores SET score3 = :sc1 WHERE golfer_id = :a """,
               
                 {
                      'a': gid,
                      'sc1': g_score.get()
                  })
            update_total(conn,gid)
        if int(g_round.get()) == 4:
            print('yahoo2')
            

            c.execute("""UPDATE five_scores SET score4 = :sc1 WHERE golfer_id = :a """,
               
                 {
                      'a': gid,
                      'sc1': g_score.get()
                  })
            update_total(conn,gid)
        if int(g_round.get()) == 5:
            print('yahoo2')
            

            c.execute("""UPDATE five_scores SET score5 = :sc1 WHERE golfer_id = :a """,
               
                 {
                      'a': gid,
                      'sc1': g_score.get()
                  })
            update_total(conn,gid)


        Ts.insert(END, g_name.get() + "  " + g_score.get())

        g_name.delete(0, END)
        g_score.delete(0, END)
        g_name.focus()
        g_score.configure(state='disabled')
        submit_button.configure(state= 'disabled')
        conn.commit()
        #conn.close()

       

    # Capture any errors in the process of entering new golfer e.g. Not Unique
    except Error as e:
        
        messagebox.showerror("Error", e)
        
        g_name.delete(0, END)
        g_score.delete(0, END)
        g_score.configure(state= "disabled")
        submit_btn.configure(state= "disabled")
        g_name.focus()


    conn.commit()    
        #conn.close()



#--------------------------------------------------------------------------------------------------------

def insert_score():
	c = conn.cursor()
	try:
		if int(g_round.get()) == 1:
			c.execute("""UPDATE five_scores SET score1 = :sc1 WHERE golfer_id = :a """,
                {                     
                      'sc1': g_newScore.get(),
                      'a': g_id.get()
                  })
			print('one')
			update_total(conn,g_id.get())
			print('update')

		if int(g_round.get()) == 2:
			c.execute("""UPDATE five_scores SET score2 = :sc1 WHERE golfer_id = :a """,
               {
                      'a': g_id.get(),
                      'sc1': g_newScore.get()
                  })
			update_total(conn,g_id.get())
		if int(g_round.get()) == 3:
			c.execute("""UPDATE five_scores SET score3 = :sc1 WHERE golfer_id = :a """,
                 {
                      'a': g_id.get(),
                      'sc1': g_newScore.get()
                  })
			update_total(conn,g_id.get())
		if int(g_round.get()) == 4:
			c.execute("""UPDATE five_scores SET score4 = :sc1 WHERE golfer_id = :a """,
                 {
                      'a': g_id.get(),
                      'sc1': g_newScore.get()
                  })
			update_total(conn,g_id.get())
		if int(g_round.get()) == 5:
			c.execute("""UPDATE five_scores SET score5 = :sc1 WHERE golfer_id = :a """,
                 {
                      'a': g_id.get(),
                      'sc1': g_newScore.get()
                  })
			update_total(conn,g_id.get())
		conn.commit()

        # show in current entry list
		for i in my_listbox.curselection():
			Ts.insert(END, str(my_listbox.get(i)[1])  + "   " + g_newScore.get())

        #clear data entry boxes
		g_newScore.delete(0, END)
		g_id.delete(0, END)
		conn.commit()

        #Disable enter sNew Score button and score entry box
		new_score_btn.configure(state="disabled")
		print('btn')
		g_newScore.configure(state='disabled')
		print('g_newscore')
		g_id.configure(state="disabled")

	except Error as e:

		messagebox.showerror("Error", e)

		g_newScore.delete(0, END)
		g_id.delete(0, END)
         #Disable enter sNew Score button and score entry box
		new_score_btn.configure(state="disabled")
		g_newScore.configure(state='disabled')
		g_id.configure(state="disabled")

#-----------------------------------------------------------------------------------------

def frame_command():
	if len(g_round.get()) == 0 or int(g_round.get()) < 1 or int(g_round.get()) >5:

		mb = Messagebox.show_error('You Must enter a round number between 1 and 5','Error')
		g_round.focus()

	else:	

	    golfer_frame.grid(row=23,column=0,padx=25,pady=5, columnspan=8,sticky='s')
	    g_name.focus()

# ----------------------------------------------------------------------------------------

def newtrace(a,b,c):
	new_score_btn.configure(state='active')	
def nametrace(a,b,c):
    g_score.configure(state='normal')

def scoretrace(a,b,c):
    submit_button.configure(state="active")

def idtrace(a,b,c):
    g_newScore.configure(state='normal')
#------------------------------------------------------------------------------------------------------

def cancel_new():
    # set conditions for a new instance of New golfer

    g_name.delete(0, END)
    g_score.delete(0, END)
    g_score.configure(state= "disabled")
    submit_button.configure(state= "disabled")
    g_name.focus()

    golfer_frame.grid_forget()




#_______________________________________________________________________________________________________

# Declarations

top_frame = tb.Frame(root,width=900, height=200, bootstyle ='light')
top_frame.pack(padx=10, pady=5, fill=BOTH)
#top_frame3= tb.Frame(root,width=900, height=100)
#top_frame3.pack(side='bottom',padx=10,  fill='x',expand=True)

left_frame = tb.Frame(root,width=400, height=600, bootstyle ='light')
left_frame.pack(side='left',padx=10, pady=5, fill=BOTH, expand= True)

right_frame = ScrolledFrame(root,width=400, height=600, bootstyle ='light')
right_frame.pack(side= 'right',padx=10, pady=5, fill=BOTH, expand=True)

golfer_frame = tb.Frame(left_frame,width=450, height=100,bootstyle='primary')
golfer_frame.grid_forget()

my_list_btn=tb.Button(left_frame,text='list',bootstyle='success', command=query)
my_list_btn.grid(row=0, column=0,padx=5,pady=5)

list_frame = tb.Frame(left_frame,width=200, height=800,bootstyle='primary')
list_frame.grid(row=1, column=0,padx=5,pady=5, rowspan=18)


my_listbox=Listbox(list_frame)
my_listbox.pack(padx=0,pady=15, side = LEFT,fill='both')

my_scrollbar = Scrollbar(list_frame)
my_scrollbar.pack(side = RIGHT, fill = BOTH)

my_listbox.config(yscrollcommand = my_scrollbar.set)
my_scrollbar.config(command = my_listbox.yview)


select_btn = tb.Button(left_frame, text="Select", command=select, bootstyle = SUCCESS)#state="disabled")
select_btn.grid(row=4, column=1, pady=5, padx=5)

id_label=tb.Label(left_frame,text = 'id')
id_label.grid(row=2,column=2,padx=10)

g_id = tb.Entry(left_frame,width=3, font=("Courier",10), state='disabled')
g_id.grid(row = 2, column=3,padx=5,pady=5)


newvar = StringVar()
newvar.set('')
g_newScore = tb.Entry(left_frame,textvariable=newvar,width=3, font=("Courier",10))
g_newScore.grid(row = 3, column=3,padx=5,pady=5)
newvar.trace('w',newtrace)


score_label=tb.Label(left_frame,text = 'score')
score_label.grid(row=3,column=2,padx=10)

g_round = tb.Entry(top_frame,width=3, font=("Courier",10))
g_round.grid(row = 0, column=1,padx=10,pady=10)

new_score_btn= tb.Button(left_frame, text='Submit',bootstyle ='success',state='disabled', command = insert_score)
new_score_btn.grid(row=4, column=3,padx=10,pady=10)

round_label = tb.Label(top_frame, text = "You must enter the round number before proceeding -->  ", font=('Courier', 10))
round_label.grid(row=0,column=0,padx=10,pady=10)

my_label = tb.Label(right_frame, text = "Batch Scores", font=('Courier', 10))
my_label.grid(row=0,column=0,padx=10,pady=10)

golfer_button= tb.Button(left_frame, text='New Golfer',bootstyle ='success', command = frame_command)
golfer_button.grid(row=21, column=0,padx=10,pady=10)


report_button= tb.Button(left_frame, text='Generate Report',bootstyle ='success', command = goforit)
report_button.grid(row=22, column=0,padx=10,pady=10)

#                  ----------------------------------------------------
#                     golfer frame

golfer_label = tb.Label(golfer_frame, text = "name", font=('Courier', 10))
golfer_label.grid(row=0,column=0,padx=10,pady=10)

namevar = StringVar()
namevar.set('')
g_name =tb.Entry(golfer_frame,textvariable=namevar,width=30)
g_name.grid(row=0, column=1,padx=10,pady=10)
namevar.trace('w',nametrace)

g_score_lbl=tb.Label(golfer_frame, text='score', font=('Courier', 10))
g_score_lbl.grid(row=0, column=2,padx=5,pady=10)

scorevar = StringVar()
scorevar.set('')
g_score =tb.Entry(golfer_frame,textvariable=scorevar,width=3, state='disabled')
g_score.grid(row=0, column=3,padx=10,pady=10)
scorevar.trace('w',scoretrace)


submit_button= tb.Button(golfer_frame, text='Submit',bootstyle ='success',state='disabled', command = insert_golfer)
submit_button.grid(row=0, column=4,padx=10,pady=10)



cancel_button= tb.Button(golfer_frame, text='Cancel',bootstyle ='success', command = cancel_new)
cancel_button.grid(row=0, column=5,padx=10,pady=10)

#                       ------------------------------------------------------

Ts = Listbox(right_frame, height = 30, width = 30)
Ts.grid(row= 2, column= 0, sticky= N, columnspan = 5, padx= 10, pady= 15)


root.mainloop()