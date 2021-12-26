import tkMessageBox
from Tkinter import *
import csv
import networkx as nx
import matplotlib.pyplot as plt

min_start = {}
min_end = {}
max_start = {}
duration = {}
max_end = {}
slack = {}
high ={}
class Window:

 def __init__(self, master):
    self.filename=""
    bar=Entry(master).grid(row=1, column=1)
    #Buttons
    y=7
    self.cbutton= Button(root, text="OK")
    y+=1
    self.cbutton.grid(row=10, column=3, sticky = W + E)
    self.bbutton= Button(root, text="Browse", command=self.browsecsv)
    self.bbutton.grid(row=1, column=3)

 def browsecsv(self):
    from tkFileDialog import askopenfilename
    self.filename = askopenfilename()
    print(self.filename)
    index = self.filename.find('.csv')
    print (index)
    if index != -1:
        self.fobj = open(self.filename, "rt")
        self.calc_info()
        self.fobj = open(self.filename, "rt")
        self.rev_tst()
        self.fobj = open(self.filename, "rt")
        self.csv_reader()
        self.CreateGanttChart()
    else :
        tkMessageBox.showerror("Error", "Wrong File Format")


    Tk().withdraw()
 def csv_reader(self):
     G = nx.DiGraph()
     reader = csv.reader(self.fobj)
     for row in reader:
         for col in reader:
             if slack[col[0]] == 0:
                G.add_node(col[0], color='yellow')
             else:
                G.add_node(col[0], color='red')
             if col[2] != '+':
                 for i in col[2]:
                     if i != ';':
                         G.add_edge(i, col[0])
     color_map= []
     for node in G:
         if slack[node] == 0:
             color_map.append('yellow')
         else:
             color_map.append('red')
     nx.draw_spectral(G, node_color=color_map, with_labels=True)
 #    plt.show()
     plt.savefig("graph.png",Format="PNG")

 def CreateGanttChart(self):
     # def CreateGanttChart(min_start, min_end, duration):
     fig, ax = plt.subplots()
     y_values = sorted(list(min_start.keys()), key=lambda x: min_start[x])
     y_start = 40
     y_height = 5
     for value in y_values:
         ax.broken_barh([(min_start[value], int(duration[value]))], (y_start, y_height), linestyle='-',
                        facecolors='orange', edgecolor='black')
         ax.broken_barh([(min_end[value], slack[value])], (y_start, y_height), linestyle='-', facecolors='white',
                        edgecolor='black')
         ax.text(min_end[value] + slack[value] + 0.5, y_start + y_height / 2, value)
         # ax.text(min_end[value] + 0.5, y_start + y_height/2, value)
         y_start += 10
     p = list(min_end.values())
     ax.set_xlim(0, max(p)+5)
     ax.set_ylim(len(duration) * 20)
     ax.set_xlabel('Duration')
     ax.set_ylabel('Tasks')
     ax.grid(color='k', linestyle=':')
     i = 5
     y_ticks = []
     while i < len(duration) * 20:
         y_ticks.append(i)
         i += 10
     ax.set_yticks(y_ticks)
     plt.tick_params(
         axis='y',
         which='both',
         left='off',
         labelleft='off')
     plt.savefig('ganttc.png')
     plt.show()

 def calc_info(self):
     reader = csv.reader(self.fobj)
     for row in reader:
         for col in reader:
             duration[col[0]] = col[1]
             if col[2] == '+':
                 min_start[col[0]] = 0
                 min_end[col[0]] = min_start[col[0]] + int(col[1])
             else:
                 max = 0
                 for i in col[2]:
                     if i != ';':
                         if int(min_end[i]) > max:
                             max = int(min_end[i])
                 min_start[col[0]] = max
                 min_end[col[0]] = min_start[col[0]] + int(col[1])

     print("Early start")
     print(min_start)
     print("Early end")
     print(min_end)

 def rev_tst(self):
     reader = csv.reader(self.fobj)
     next(reader)
     max = 0
     max_node = ''
     for i in min_end:
         if min_end[i] > max:
             max = int(min_end[i])
             max_node = i
         max_end[i] = 0
         max_start[i] = 0
         slack[i] = 0

     max_start[max_node] = min_start[max_node]
     for col in reversed(list(reader)):
         for i in col[2]:
             if i != ';':
                 if i != '+':
                     if max_start[col[0]] < max_end[i]:
                         max_end[i] = max_start[col[0]]
                         max_start[i] = max_end[i] - int(duration[i])
                     if max_end[i] == 0:
                         max_end[i] = max_start[col[0]]
                         max_start[i] = max_end[i] - int(duration[i])
     for i in max_end:
         if max_end[i] == 0:
             max_end[i] = max
             max_start[i] = max_end[i] - int(duration[i])
     for i in slack:
         slack[i] = max_end[i] - min_end[i]
     print("Late start")
     print(max_start)
     print("Late end")
     print(max_end)
     print("Slack")
     print(slack)
     print("Critical Path Nodes")
     for i in slack:
         if slack[i] == 0:
             print(i)
             high[i]=i

root = Tk()
root.title("PERT CHART")
window=Window(root)
root.mainloop()
