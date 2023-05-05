import tkinter
from tkinter import filedialog
import tkinter.scrolledtext
import networkx as nx
from Alpha_Burden_based_semantic import alpha_burden_based
from Burden_based_semantic import burden_based
from catergriser_based import categoriser_based_ranking
from discussion_based import discussion_based
from matt_and_toni import mt_ranking
from scoring_aggregation.biased_scoring_aggregation import biased_scoring_aggregation
from scoring_aggregation.borda_count_aggregation import borda_count_aggregation
from scoring_aggregation.consensus import closest_ranking
from scoring_aggregation.plurality_aggregation import plurality_aggregation
from scoring_aggregation.top_k_aggregation import topk_aggregation
from scoring_aggregation.veto_aggregation import veto_aggregation
from tuple_based import tuple_based
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
G = nx.DiGraph() 
rankings = []
semantics = []

def stop():
    exit(0)

def on_closing(event=None):
    win.quit()

win = tkinter.Tk()
win.title("Argmentation frameworks solver")
win.protocol("WM_DELETE_WINDOW", on_closing)
win.configure(bg="light blue")

#graph area
graph_label = tkinter.Label(win, text="Type a Graph: Or", bg="light blue")
graph_label.config(font=("Arial", 12), fg='black' )
graph_label.pack(padx= 20, pady= 5)

text_area = tkinter.scrolledtext.ScrolledText(win)
text_area.pack(padx=30, pady=15)
text_area.config(font=("Cascadia Code", 11) , height=15 )


#open from file button
def open_file():
    file_path = filedialog.askopenfilename()
    text_area.delete('1.0', 'end')
    with open(file_path, 'r') as file:
        for line in file:
            text_area.insert('end', line)
    text_area.yview('end')

open_button = tkinter.Button(win, text="Open from file", command=open_file)
open_button.config(font=("Arial", 12))
open_button.place(x=470, y=4)


def reset():
    text_area.delete('1.0', 'end')
    output_area.config(state='normal')
    output_area.delete('1.0', 'end')
    output_area.config(state='disabled')
    outputs_area.config(state='normal')
    outputs_area.delete('1.0', 'end')
    outputs_area.config(state='disabled')
    rankings.clear()
reset_button = tkinter.Button(win, text="reset", command=reset)
reset_button.config(font=("Arial", 12))
reset_button.place(x=750, y=4)


#convert file button
def convert_file():
    file_path = filedialog.askopenfilename()
    p= True
    counter = 0
    with open(file_path, 'r') as file , open("newformat.txt" , 'w') as destination:
        for line in file:
                line = line.strip()
                if line.startswith('arg(') and line.endswith(').'):
                    counter += 1

                elif line.startswith('att(') and line.endswith(').'):
                    if (p) :
                        destination.write("p af " + str(counter) + '\n')
                        destination.write("# comment \n")
                        p =False
                    content = line[5:-2].split(',')
                    arg1_value = content[0].strip()
                    destination.write(arg1_value + ' ')
                    arg2_value = content[1].strip()
                    arg2_value = arg2_value[1:]
                    destination.write(arg2_value + '\n')

convert_button = tkinter.Button(win, text="Convert old format file", command=convert_file)
convert_button.config(font=("Arial", 12))
convert_button.place(x=10, y=5)


# save button
def save_graph():
    graph = text_area.get('1.0', 'end').split('\n')
    graph = graph[1:]
    for line in graph:
        if line : 
            if (line[0] == '#' ):
                continue          
            else :
                content = line.split()
                G.add_edge(int(content[0]) , int(content[1]))

save_button = tkinter.Button(win, text="save", command=save_graph)
save_button.config(font=("Arial", 12))
save_button.place(x=650, y=360)

#show graph button
def show_graph():
    new_window = tkinter.Toplevel(win,bg='light blue')
    label = tkinter.Label(new_window, text="Visual representation of the graph" ,bg='light blue')
    label.config(font=("Arial", 12), fg='black' )
    label.pack()
    fig = plt.figure(figsize =(7, 7))
    nx.draw_networkx(G, with_labels = True, node_color ='green')
    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack()
show_button = tkinter.Button(win, text="show", command=show_graph)
show_button.config(font=("Arial", 12))
show_button.place(x=720, y=360)


# semantics area
semantics_frame = tkinter.Frame(win)
semantics_frame.configure(bg="light blue")
semantics_frame.pack(side="left")


number_entry = tkinter.Entry(win ,  width=7)
number_entry.insert(0, 'alpha')
number_entry.place(x=153, y=375)

def on_entry_click(event):
    if number_entry.get() == 'alpha':
        number_entry.delete(0, tkinter.END)

number_entry.bind('<FocusIn>', on_entry_click)

semantics_listbox = tkinter.Listbox(semantics_frame, height=8)
semantics_listbox.pack(padx= 20, pady= 5)
semantics_listbox.insert(tkinter.END, "RANKING")
semantics_listbox.insert(tkinter.END, "1-categoriser")
semantics_listbox.insert(tkinter.END, "2-discussion")
semantics_listbox.insert(tkinter.END, "3-burden")
semantics_listbox.insert(tkinter.END, "4-alpha burden")
semantics_listbox.insert(tkinter.END, "5-tuple")
semantics_listbox.insert(tkinter.END, "6-Matt & Toni")
def on_select(event):
    message = semantics_listbox.get(semantics_listbox.curselection() )
    semantic = message[0]
    message = message[2:] + ' based : ' 
    if semantic == '1':
        rank= categoriser_based_ranking(G)
        if (rank):
            rankings.append(rank)
            semantics.append(semantic)
        message += str(rank)
    if semantic == '2':
        rank = discussion_based(G ,1)
        if (rank):
            rankings.append(rank)
            semantics.append(semantic)
        message += str(rank)
    elif semantic == '3':
        rank = burden_based(G ,10)
        if (rank):
            rankings.append(rank)
            semantics.append(semantic)
        message += str(rank)
    elif semantic == '4':
        alpha = int(number_entry.get())
        rank = alpha_burden_based(G ,alpha)
        if (rank):
            rankings.append(rank)
            semantics.append(semantic)
        message += str(rank)
    elif semantic == '5':
        rank = tuple_based(G)
        if (isinstance(rank, list) and (rank)):
            rankings.append(rank)
            semantics.append(semantic)
        message += str(rank)
    elif semantic == '6':
        rank = mt_ranking(G)
        message = message.replace('based ','')
        if (rank):
            rankings.append(rank)
            semantics.append(semantic)
        message += str(rank)
    output_area.config(state='normal')
    output_area.insert('end', message+'\n')
    output_area.yview('end')
    output_area.config(state='disabled')

semantics_listbox.bind("<<ListboxSelect>>", on_select)


#solver output
output_label = tkinter.Label(win, text="Ranking Output :", bg="light blue")
output_label.config(font=("Arial", 12), fg='black')
output_label.pack(padx= 20, pady= 5)

output_area = tkinter.scrolledtext.ScrolledText(win)
output_area.pack(padx= 10, pady= 10)
output_area.config(font=("Arial", 10)   )
output_area.config(state="disabled", height=5)



#aggregation list
k_entry = tkinter.Entry(win ,  width=7)
k_entry.insert(0, 'K')
k_entry.place(x=153, y=515)

def on_entry_click(event):
    if k_entry.get() == 'K':
        k_entry.delete(0, tkinter.END)

k_entry.bind('<FocusIn>', on_entry_click)

aggregation_listbox = tkinter.Listbox(semantics_frame, height=8)
aggregation_listbox.pack(padx= 20, pady= 5)
aggregation_listbox.insert(tkinter.END, "AGGREGATION")
aggregation_listbox.insert(tkinter.END, "1-borda count")
aggregation_listbox.insert(tkinter.END, "2-plurality")
aggregation_listbox.insert(tkinter.END, "3-top k")
aggregation_listbox.insert(tkinter.END, "4-veto")
aggregation_listbox.insert(tkinter.END, "5-biased scoring")
aggregation_listbox.insert(tkinter.END, "6-Kemeny")
def aggregate(event):
    message = aggregation_listbox.get(aggregation_listbox.curselection() )
    index = message[0]
    message = message[2:] + ' : '
    rank = []
    if (index == '1'):
        rank = borda_count_aggregation(rankings)
    elif (index == '2'):
        rank = plurality_aggregation(rankings)
    elif (index == '3') :
        k = int(k_entry.get())
        rank= topk_aggregation(ranking_list=rankings , k=k)
    elif (index == '4') :
        rank= veto_aggregation(rankings)
    elif (index == '5') :
        rank= biased_scoring_aggregation(rankings)
    elif (index == '6') :
        message += str("kemeny_aggregation(rankings)")
    outputs_area.config(state='normal')
    message += str(rank)
    consensus = closest_ranking(rank, rankings)
    outputs_area.insert('end', message+ ' --> ' + str(consensus)+'\n')
    outputs_area.yview('end')
    outputs_area.config(state='disabled')
aggregation_listbox.bind("<<ListboxSelect>>", aggregate)

#aggregation output
outputs_label = tkinter.Label(win, text="Aggregation Output :", bg="light blue")
outputs_label.config(font=("Arial", 12), fg='black')
outputs_label.pack(padx= 20, pady= 5)

outputs_area = tkinter.scrolledtext.ScrolledText(win)
outputs_area.pack(padx= 10, pady= 10)
outputs_area.config(font=("Arial", 10)  )
outputs_area.config(state="disabled", height=5)


gui_done = True
win.mainloop()
win.protocol("wM_DELETE_WINDOW", stop)