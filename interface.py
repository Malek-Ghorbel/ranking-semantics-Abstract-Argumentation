import tkinter
import time 
from tkinter import filedialog
from tkinter import font
import tkinter.scrolledtext
import networkx as nx
from Alpha_Burden_based_semantic import alpha_burden_based
from Burden_based_semantic import burden_based
from catergriser_based import categoriser_based_ranking
from discussion_based import discussion_based
from matt_and_toni import mt_ranking
from scoring_aggregation.biased_scoring_aggregation import biased_scoring_aggregation
from scoring_aggregation.borda_count_aggregation import borda_count_aggregation
from scoring_aggregation.consensus import closest_ranking, kendall_closest_ranking
from scoring_aggregation.plurality_aggregation import plurality_aggregation
from scoring_aggregation.top_k_aggregation import topk_aggregation
from scoring_aggregation.veto_aggregation import  minimax_method, veto_aggregation , aggregate_rankings
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
win.configure(bg="#badfe7")

#graph area
bold_font = font.Font(weight='bold')

graph_label = tkinter.Label(win, text="Type a Graph: Or", bg="#badfe7")
graph_label.config( font=("Arial", 12, "bold"), fg="#388087" )
graph_label.pack(padx= 20, pady= 5)

text_area = tkinter.scrolledtext.ScrolledText(win, bg="#f6f6f2" , border=0)
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

open_button = tkinter.Button(win, padx=5, pady=5, text="Open from file", command=open_file, bg="#6fb3b8", border=0.3)
open_button.config(font=("Arial", 10, "bold"), fg="#08535a")
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
    semantics.clear()
reset_button = tkinter.Button(win, padx=5, pady=5, text="Reset", command=reset, bg="#6fb3b8", border=0.3)
reset_button.config(font=("Arial", 10, "bold"), fg="#08535a")
reset_button.place(x=740, y=4)


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

convert_button = tkinter.Button(win, padx=5, pady=5, text="Convert old format file", command=convert_file, bg="#6fb3b8", border=0.3)
convert_button.config(font=("Arial", 10, "bold"), fg="#08535a")
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

save_button = tkinter.Button(win, padx=5, pady=5, text="Save", command=save_graph, bg="#6fb3b8", border=0.3)
save_button.config(font=("Arial", 10, "bold"), fg="#08535a")
save_button.place(x=650, y=360)

#show graph button
def show_graph():
    new_window = tkinter.Toplevel(win,bg='#badfe7')
    label = tkinter.Label(new_window, text="Visual representation of the graph" ,bg='#badfe7')
    label.config(font=("Arial", 12, "bold"), fg='#08535a' )
    label.pack()
    fig = plt.figure(figsize =(7, 7))
    nx.draw_networkx(G, with_labels = True, node_color ='#6fb3b8')
    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack()
show_button = tkinter.Button(win, padx=5, pady=5, text="Show", command=show_graph, bg="#6fb3b8", border=0.3)
show_button.config(font=("Arial", 10, "bold"), fg="#08535a")
show_button.place(x=720, y=360)


# semantics area
semantics_frame = tkinter.Frame(win)
semantics_frame.configure(bg="#badfe7")
semantics_frame.pack(side="left")


number_entry = tkinter.Entry(win ,  width=7, bg="#f6f6f2" , border=0)
number_entry.insert(0, ' alpha')
number_entry.place(x=153, y=375)

def on_entry_click(event):
    if number_entry.get() == 'alpha':
        number_entry.delete(0, tkinter.END)

number_entry.bind('<FocusIn>', on_entry_click)

semantics_listbox = tkinter.Listbox(semantics_frame, height=8, bg="#f6f6f2" , border=0)
semantics_listbox.pack(padx= 20, pady= 5)
semantics_listbox.insert(tkinter.END, " RANKING")
semantics_listbox.insert(tkinter.END, " 1-categoriser")
semantics_listbox.insert(tkinter.END, " 2-discussion")
semantics_listbox.insert(tkinter.END, " 3-burden")
semantics_listbox.insert(tkinter.END, " 4-alpha burden")
semantics_listbox.insert(tkinter.END, " 5-tuple")
semantics_listbox.insert(tkinter.END, " 6-Matt & Toni")
def on_select(event):
    try : 
        message = semantics_listbox.get(semantics_listbox.curselection() )
        semantic = message[1]
        message = message[3:] + ' based : ' 
        start_time = time.time()
        if semantic == '1':
            rank= categoriser_based_ranking(G)
            if (rank):
                rankings.append(rank)
                semantics.append("Categoriser")
            message += str(rank)
        if semantic == '2':
            rank = discussion_based(G ,1)
            if (rank):
                rankings.append(rank)
                semantics.append("Discussion")
            message += str(rank)
        elif semantic == '3':
            rank = burden_based(G ,10)
            if (rank):
                rankings.append(rank)
                semantics.append("Burden")
            message += str(rank)
        elif semantic == '4':
            alpha = int(number_entry.get())
            rank = alpha_burden_based(G ,alpha)
            if (rank):
                rankings.append(rank)
                semantics.append("alpha-Burden")
            message += str(rank)
        elif semantic == '5':
            rank = tuple_based(G)
            if (isinstance(rank, list) and (rank)):
                rankings.append(rank)
                semantics.append("Tuple")
            message += str(rank)
        elif semantic == '6':
            rank = mt_ranking(G)
            message = message.replace('based ','')
            if (rank):
                rankings.append(rank)
                semantics.append("M&T")
            message += str(rank)
        end_time = time.time()
        print(end_time - start_time)
        output_area.config(state='normal')
        output_area.insert('end', message+'\n')
        output_area.yview('end')
        output_area.config(state='disabled')
    except Exception as e :
        print(e)

semantics_listbox.bind("<<ListboxSelect>>", on_select)


#solver output
output_label = tkinter.Label(win, text="Ranking Output :", bg="#badfe7")
output_label.config(font=("Arial", 12, "bold"), fg='#006770')
output_label.pack(padx= 20, pady= 5)

output_area = tkinter.scrolledtext.ScrolledText(win,  bg="#f6f6f2" , border=0)
output_area.pack(padx= 10, pady= 10)
output_area.config(font=("Arial", 10)   )
output_area.config(state="disabled", height=5)



#aggregation list
k_entry = tkinter.Entry(win ,  width=7, bg="#f6f6f2" , border=0)
k_entry.insert(0, ' K')
k_entry.place(x=153, y=515)

def on_entry_click(event):
    if k_entry.get() == 'K':
        k_entry.delete(0, tkinter.END)

k_entry.bind('<FocusIn>', on_entry_click)

aggregation_listbox = tkinter.Listbox(semantics_frame,  height=8, bg="#f6f6f2" , border=0)
aggregation_listbox.pack(padx= 20, pady= 5)
aggregation_listbox.insert(tkinter.END, " AGGREGATION")
aggregation_listbox.insert(tkinter.END, " 1-borda count")
aggregation_listbox.insert(tkinter.END, " 2-plurality")
aggregation_listbox.insert(tkinter.END, " 3-top k")
aggregation_listbox.insert(tkinter.END, " 4-veto")
def print_aggregation_rank(distances) :
    # Combine the lists and sort based on time
    combined_list = sorted(zip(semantics, distances), key=lambda x: x[1])
    # Determine the ranks
    ranks = {}
    rank = 1
    prev_time = None
    for i, (name, time) in enumerate(combined_list):
        if time != prev_time:
            rank = i + 1
        ranks[name] = rank
        prev_time = time
    # Print the results
    for name, rank in ranks.items():
        print(f"{name} -> {rank}")

def aggregate(event):
    
    message = aggregation_listbox.get(aggregation_listbox.curselection() )
    index = message[1]
    message = message[3:] + ' : '
    rank = []
    if (index == '1'):
        rank = borda_count_aggregation(rankings)
    elif (index == '2'):
        rank = plurality_aggregation(rankings)
    elif (index == '3') :
        k = int(k_entry.get())
        rank= topk_aggregation(ranking_list=rankings , k=k)
    elif (index == '4') :
        rank= minimax_method(rankings)
    elif (index == '5') :
        rank= biased_scoring_aggregation(rankings)
    outputs_area.config(state='normal')
    message += str(rank)
    distances = kendall_closest_ranking(rank, rankings)
    consensus = semantics[distances.index(min(distances))]
    print("simple distance")
    print_aggregation_rank(distances)

    kendall_distances = kendall_closest_ranking(rank, rankings)
    print("Kendall distance")
    print_aggregation_rank(kendall_distances)

    outputs_area.insert('end', message+ ' --> ' + consensus+'\n')
    outputs_area.yview('end')
    outputs_area.config(state='disabled')
    
aggregation_listbox.bind("<<ListboxSelect>>", aggregate)

#aggregation output
outputs_label = tkinter.Label(win, text="Aggregation Output :", bg="#badfe7")
outputs_label.config(font=("Arial", 12, "bold"), fg='#006770')
outputs_label.pack(padx= 20, pady= 5)

outputs_area = tkinter.scrolledtext.ScrolledText(win, bg="#f6f6f2" , border=0)
outputs_area.pack(padx= 10, pady= 10)
outputs_area.config(font=("Arial", 10)  )
outputs_area.config(state="disabled", height=5)


gui_done = True
win.mainloop()
win.protocol("wM_DELETE_WINDOW", stop)