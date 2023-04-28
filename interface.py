import tkinter
from tkinter import filedialog
import tkinter.scrolledtext
import networkx as nx
from Alpha_Burden_based_semantic import alpha_burden_based
from Burden_based_semantic import burden_based
from discussion_based import discussion_based
from scoring_aggregation.biased_scoring_aggregation import biased_scoring_aggregation
from scoring_aggregation.borda_count_aggregation import borda_count_aggregation
from scoring_aggregation.plurality_aggregation import plurality_aggregation
from scoring_aggregation.top_k_aggregation import topk_aggregation
from scoring_aggregation.veto_aggregation import veto_aggregation
from tuple_based import tuple_based
G = nx.DiGraph() 
rankings = []

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
graph_label.config(font=("Arial", 12), fg='black')
graph_label.pack(padx= 20, pady= 5)

text_area = tkinter.scrolledtext.ScrolledText(win)
text_area.pack(padx=25, pady=5)
text_area.config(font=("Cascadia Code", 11) , height=15)


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
open_button.place(x=480, y=4)


# save button
def save_graph():
    graph = text_area.get('1.0', 'end').split('\n')
    for line in graph:
        if line : 
            if (line[0] == '#' ):
                continue
            elif ( line[0] == 'p'):
                content = line.split()
                nb_nodes = int(content[-1])
                nodes = [i+1 for i in range(nb_nodes)]
                G.add_nodes_from(nodes)
            else :
                content = line.split()
                G.add_edge(int(content[0]) , int(content[1]))

save_button = tkinter.Button(win, text="save graph", command=save_graph)
save_button.config(font=("Arial", 12))
save_button.place(x=673, y=350)


# semantics area
semantics_frame = tkinter.Frame(win)
semantics_frame.configure(bg="light blue")
semantics_frame.pack(side="left")

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
    if semantic == '2':
        rank = discussion_based(G ,10)
        rankings.append(rank)
        message += str(rank)
    elif semantic == '3':
        rank = burden_based(G ,10)
        rankings.append(rank)
        message += str(rank)
    elif semantic == '4':
        rank = alpha_burden_based(G ,1)
        rankings.append(rank)
        message += str(rank)
    elif semantic == '5':
        rank = tuple_based(G)
        if isinstance(rank, list):
            rankings.append(rank)
        message += str(rank)
    elif semantic == '6':
        message = message.replace('based ','')
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
output_area.config(font=("Arial", 10))
output_area.config(state="disabled", height=5)



#aggregation list
aggregation_listbox = tkinter.Listbox(semantics_frame, height=8)
aggregation_listbox.pack(padx= 20, pady= 5)
aggregation_listbox.insert(tkinter.END, "AGGREGATION")
aggregation_listbox.insert(tkinter.END, "1-borda count")
aggregation_listbox.insert(tkinter.END, "2-plurality")
aggregation_listbox.insert(tkinter.END, "3-top k")
aggregation_listbox.insert(tkinter.END, "4-veto")
aggregation_listbox.insert(tkinter.END, "5-biased scoring")
def aggregate(event):
    message = aggregation_listbox.get(aggregation_listbox.curselection() )
    index = message[0]
    message = message[2:] + ' : '
    if (index == '1'):
        message += str(borda_count_aggregation(rankings))
    elif (index == '2'):
        message += str(plurality_aggregation(rankings))
    elif (index == '3') :
        message += str(topk_aggregation(ranking_list=rankings , k=5))
    elif (index == '4') :
        message += str(veto_aggregation(rankings))
    elif (index == '5') :
        message += str(biased_scoring_aggregation(rankings))
    outputs_area.config(state='normal')
    outputs_area.insert('end', message+'\n')
    outputs_area.yview('end')
    outputs_area.config(state='disabled')
aggregation_listbox.bind("<<ListboxSelect>>", aggregate)

#aggregation output
outputs_label = tkinter.Label(win, text="Aggregation Output :", bg="light blue")
outputs_label.config(font=("Arial", 12), fg='black')
outputs_label.pack(padx= 20, pady= 5)

outputs_area = tkinter.scrolledtext.ScrolledText(win)
outputs_area.pack(padx= 10, pady= 10)
outputs_area.config(font=("Arial", 10))
outputs_area.config(state="disabled", height=5)


gui_done = True
win.mainloop()
win.protocol("wM_DELETE_WINDOW", stop)