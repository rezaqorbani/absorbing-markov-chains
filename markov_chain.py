import numpy 
import math
import fractions


def solution(input_matrix, initial_state):
 
    mtrx = numpy.array(input_matrix).transpose()

    ordered_matrix, number_of_absorb, init_vec= absorb_stndrd_form(mtrx,initial_state) #transition matrix in canonical form, the numer of absorbing states
    
    S = []
    R = []

    for column in ordered_matrix[number_of_absorb:]:    #assign the specific sub-matrices from the main matrix
        S.append(list(column[:number_of_absorb]))
        R.append(list(column[number_of_absorb:]))

    S = numpy.array(S).transpose()  #convert matrices to numpy arrays
    R = numpy.array(R).transpose()
    
    ordered_matrix = numpy.array(ordered_matrix)

    I_minus_R_inverted= numpy.linalg.inv(numpy.identity(R.shape[0]) - R) #Fundamental Matrix
    S_times_R = numpy.dot(S,I_minus_R_inverted).transpose()
    


    column_index = 0
    for column in ordered_matrix[number_of_absorb:]: #change the transition matrix again to make the final standard form
        column[:number_of_absorb] = S_times_R[column_index]
        column[number_of_absorb:] = [0 for _ in range(len(ordered_matrix) - number_of_absorb)]
        column_index+=1
    
    ordered_matrix = ordered_matrix.transpose() # transpose the matrix for matrix multiplication
    
    
    stable_distribution_matrix = numpy.dot(ordered_matrix, numpy.array(init_vec))
    return stable_distribution_matrix.astype(float)

    

def absorb_stndrd_form(mtrx,init_vec): 
    output_matrix = []
    output_init_vec = []

    absorbing_state_indices = []
    non_absorbing_state_indices = []
    current_index = 0
    for row in mtrx:
        if(list(row).count(1)): #if all elements in the row are zero, thein it is a absorbing state
            absorbing_state_indices.append(current_index)
        else:
            non_absorbing_state_indices.append(current_index)
        current_index += 1


    ordered_indices = list(absorbing_state_indices + non_absorbing_state_indices) #the indices for the ordered matrix relative to original input matrix

    
    for aborbing_index in absorbing_state_indices: #put 1 at the correspoding index of each absorbing state
        temp_row = mtrx[aborbing_index]
        output_matrix.append(list(temp_row))
        output_init_vec.append(init_vec[aborbing_index])
       

    for non_absorbing_index in non_absorbing_state_indices: #relocate probabilities in the non_absorbing states so that they represent the same transition as in original matrix. The required change is given in ordered indices.
        current_row = mtrx[non_absorbing_index]
        temp_row = []
        for ordered_index in ordered_indices:
            temp_row.append(current_row[ordered_index]) #use the elements in ordered_indices as index
        output_init_vec.append(init_vec[non_absorbing_index])
        output_matrix.append(temp_row)

    return output_matrix, len(absorbing_state_indices),output_init_vec


def lcm(x, y):
    return x * y // math.gcd(x, y)

def lcm_list(denominators): 
    least_common_multiplicand = 0

    if(len(denominators) == 1):
        least_common_multiplicand=denominators[0] 
    else:
        for i in range(len(denominators)-1): #Take the lcm of two adjacent denominators, then take this lcm-value and calculate lcm with the next denominator and so on. Save the biggest lcm value. 
            if(lcm(denominators[i],denominators[i+1]) > least_common_multiplicand):
                least_common_multiplicand = lcm(denominators[i],denominators[i+1])
    return least_common_multiplicand

