import numpy 
import math
import fractions
#import discreteMarkovChain
matrix = numpy.array([[ 0,  7,  0, 17,  0,  1,  0,  5,  0,  2], [ 0,  0, 29,  0, 28,  0,  3,  0, 16,  0], [ 0,  3,  0,  0,  0,  1,  0,  0,  0,  0], [48,  0,  3,  0,  0,  0, 17,  0,  0,  0], [ 0,  6,  0,  0,  0,  1,  0,  0,  0,  0], [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0], [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0], [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0], [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0], [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0]])


def solution(m):
    # Your code here
    m_to_floats = []
    for row in m: #make every non-zero element in the matrix a float
        temp_row = []
        for element in row: 
            if(element != 0): 
                  temp_row.append(float(element) / float(sum(row)))
            else:
                temp_row.append(0)
        m_to_floats.append(temp_row)


    ordered_matrix, number_of_absorb = absorb_stndrd_form(m_to_floats) #transition matrix in canonical form, the numer of absorbing states
    
    matrix_dimension = len(ordered_matrix) #we assume a square matrix
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
    
    starting_vector = []    #vector reperesenting the initial state of the fuel particle

    if(matrix_dimension == 1):              #We assume that the particle always has a initial state and that this staet is S0
        starting_vector = [1]               #If there is only one possible state, then that must also be the initial state
    else:
        for i in range(matrix_dimension):   #Else the arrangement in the standard matrix makes the initial state immidiately after the last absorbing state
            if(i == (number_of_absorb)):
                starting_vector.append(1)
            else:
                starting_vector.append(0)
    
    
    stable_distribution_matrix = list(numpy.dot(ordered_matrix, numpy.array(starting_vector))) 

    numerators = []
    denominators = []

    for i in range(number_of_absorb):
        probability = stable_distribution_matrix[i]
        numerators.append(fractions.Fraction(probability).limit_denominator().numerator)
        denominators.append(fractions.Fraction(probability).limit_denominator().denominator)
   
    least_common_multiplicand = lcm_list(denominators)
    
    for i in range(len(numerators)): #multiply the numerator with the corresponding factor that denominator will be multiplied with to get the lcm
        numerators[i] *= (least_common_multiplicand/denominators[i])

    
    output = []
    for numerator in numerators:
        output.append(numerator)
    
    output.append(least_common_multiplicand)

    return list(map(int,output))
    

def absorb_stndrd_form(mtrx): 
    output_matrix = []

    absorbing_state_indices = []
    non_absorbing_state_indices = []
    current_index = 0
    for row in mtrx:
        if(len(set(row)) == 1 and list(set(row))[0] == 0): #if all elements in the row are zero, thein it is a absorbing state
            absorbing_state_indices.append(current_index)
        else:
            non_absorbing_state_indices.append(current_index)
        current_index += 1


    ordered_indices = list(absorbing_state_indices + non_absorbing_state_indices) #the indices for the ordered matrix relative to original input matrix

    current_index = 0
    for aborbing_index in absorbing_state_indices: #put 1 at the correspoding index of each absorbing state
        temp_row = mtrx[aborbing_index]
        temp_row[current_index] = 1
        output_matrix.append(list(temp_row))
        current_index += 1

    for non_absorbing_index in non_absorbing_state_indices: #relocate probabilities in the non_absorbing states so that they represent the same transition as in original matrix. The required change is given in ordered indices.
        current_row = mtrx[non_absorbing_index]
        temp_row = []
        for ordered_index in ordered_indices:
            temp_row.append(current_row[ordered_index]) #use the elements in ordered_indices as index
        output_matrix.append(temp_row)
    return output_matrix, len(absorbing_state_indices)


def lcm(x, y):
    return x * y // fractions.gcd(x, y)

def lcm_list(denominators): 
    least_common_multiplicand = 0

    if(len(denominators) == 1):
        least_common_multiplicand=denominators[0] 
    else:
        for i in range(len(denominators)-1): #Take the lcm of two adjacent denominators, then take this lcm-value and calculate lcm with the next denominator and so on. Save the biggest lcm value. 
            if(lcm(denominators[i],denominators[i+1]) > least_common_multiplicand):
                least_common_multiplicand = lcm(denominators[i],denominators[i+1])
    return least_common_multiplicand

print(solution(matrix))
