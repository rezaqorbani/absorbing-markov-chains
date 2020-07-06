from tkinter import *
from tkinter import messagebox
import markov_chain
import re

def validate_elements_row(output_matrix,entry,name_of_matrix):
       
    content = entry.get()
    pattern = re.compile(r"[0]{1}[.]{1}[0-9]+|^[01]{1}$|\d+[/]\d+")
    found = pattern.match(content)
    if(not(found)):
        messagebox.showerror(title=name_of_matrix + "Error", message="The input in "+name_of_matrix+" is incorrect!" )

    else:
        if(len(found.group().split("/"))==2):
            division_string_split = found.group().split("/")
            user_input = float(int(division_string_split[0])/int(division_string_split[1]))
            if(user_input > 1): 
                messagebox.showerror(title="Value Error", message="All elements in the "+ name_of_matrix +" must <= 1" )
            else:
                output_matrix.append(user_input)
        else:
            user_input = float(found.group(0))
            if(user_input > 1):
                messagebox.showerror(title="Value Error", message="All elements in the "+ name_of_matrix +" must <= 1" )
            else:
                output_matrix.append(user_input)



def calculate_stable_state_vector(): 
    matrix=[]
    for row in matrix_entries:
        temp_row = []
        for entry in row:
            validate_elements_row(temp_row,entry,"matrix")
        matrix.append(temp_row)


    init_vector = []
    for entry in initial_state_vector_entries:
        validate_elements_row(init_vector,entry,"vector")
    
    
    calculated_vector = markov_chain.solution(matrix,init_vector)

    result = list(map(float,calculated_vector))
    
    index = 0
    for entry in result_entries:
        entry.delete(0,'end')
        entry.insert(0, result[index])
        index += 1
    
    
def create_matrix_elements():

    N = int(dimension_entry.get())
    if(N!=0):
        matrix_entries.clear()
        initial_state_vector_entries.clear()
        result_entries.clear()
        button_0 = Button(master=frame_0, text = "Re-enter", command = regenerate_matrix)
        button_0.grid(row=3)

        ask_for_matrix = Label(master=frame_1, text="Please enter the matrix")
        ask_for_matrix.grid(row=0)
        frame_1.pack()

        for i in range(N):
            temp_row = []
            for j in range(N):
                entry = Entry(master=frame_2,width=10 )
                entry.insert(0,"0")
                temp_row.append(entry)
                entry.grid(row=i,column=j,sticky="W",padx=5,pady=5)

            matrix_entries.append(temp_row)

        frame_2.pack() 
    
        ask_for_init = Label(master=frame_3, text="Please Enter the initial state vector")
        ask_for_init.grid(row=0)

        for n in range(N):
            entry_init = Entry(frame_3, width = 10)
            entry_init.insert(0,"0")
            entry_init.grid(row=n+1)
            initial_state_vector_entries.append(entry_init)

        calculate_button = Button(master = frame_3, text="Calculate!", command = calculate_stable_state_vector)
        calculate_button.grid(row=N+1)
        frame_3.pack()


        result = Label(master=frame_4, text="Result")
        result.grid(row=0)
        
        for n in range(N):
            result_entry = Entry(frame_4, width = 20)
            result_entry.insert(0,"0")
            result_entries.append(result_entry)
            result_entry.grid(row=n+1)
        frame_4.pack()

def regenerate_matrix():
    for slave in frame_1.grid_slaves():
        slave.destroy()
    for slave in frame_2.grid_slaves():
        slave.destroy()
    for slave in frame_3.grid_slaves():
        slave.destroy()
    for slave in frame_4.grid_slaves():
        slave.destroy()


    create_matrix_elements()

window = Tk()
window.title("Absorbing Markov Chain")
frame_0 = Frame(window)
frame_1 = Frame(window)
frame_2 = Frame(window)
frame_3 = Frame(window)
frame_4 = Frame(window)

initial_state_vector_entries = []
matrix_entries = []
result_entries = []


prompt_dimension = Label( master=frame_0, text = "Please enter the dimension (N) of the N x N stochastic matrix!")
prompt_dimension.grid(row=0)

dimension_entry = Entry( master=frame_0, text="Enter N",width=10)
dimension_entry.insert(0,"0")
dimension_entry.grid(row=2)


button_0 = Button(master=frame_0, text = "Enter", command = create_matrix_elements)
button_0.grid(row=3)

frame_0.pack()

window.mainloop()
            
