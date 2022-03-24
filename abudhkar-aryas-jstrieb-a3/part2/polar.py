#!/usr/local/bin/python3
#
# Authors: Aishwarya Budhkar (abudhkar)
#          Jacob Striebel (jstrieb),
#          Shubhavi Arya (aryas)
#
# Ice layer finder
# Based on skeleton code by D. Crandall, November 2021
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
import copy
import numpy

# calculate "Edge strength map" of an image
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_boundary(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

def draw_asterisk(image, pt, color, thickness):
    for (x, y) in [ (pt[0]+dx, pt[1]+dy) for dx in range(-3, 4) for dy in range(-2, 3) if dx == 0 or dy == 0 or abs(dx) == abs(dy) ]:
        if 0 <= x < image.size[0] and 0 <= y < image.size[1]:
            image.putpixel((x, y), color)
    return image


# Save an image that superimposes three lines (simple, hmm, feedback) in three different colors
# (yellow, blue, red) to the filename
def write_output_image(filename, image, simple, hmm, feedback, feedback_pt):
    new_image = draw_boundary(image, simple, (255, 255, 0), 2)
    new_image = draw_boundary(new_image, hmm, (0, 0, 255), 2)
    new_image = draw_boundary(new_image, feedback, (255, 0, 0), 2)
    new_image = draw_asterisk(new_image, (feedback_pt[1],feedback_pt[0]), (255, 0, 0), 2)
    imageio.imwrite(filename, new_image)

# Code for simple Bayes net Fig (b)
# Only using emission probability that is edge mask
def simple_air(edge_strength):

    # To store the boundary
    air_boundary = []

    # For each column return the max edge strength mask/probability row, conditioned to having a smooth boundary.
    for j in range(edge_strength.shape[1]):

        # Store max probability/edge strength mask
        max1 = -1

        # Row having max probability
        best_row = 0

        # Iterate through all rows of the columns
        for i in range(edge_strength.shape[0]):

            # Dividing by 100 to avoid overflow in double_scalars
            prob = edge_strength[i][j] / 100

            # Get the best row
            if(j > 0):
                # If prev column present, go for a smooth boundary
                if(prob > max1 and abs(i-air_boundary[j-1]) < 20):
                    max1 = prob
                    best_row = i
            # Get the max probability for the column
            else:
                if(prob > max1):
                    max1 = prob
                    best_row = i
        air_boundary.append(best_row)
    return air_boundary


def simple_ice(edge_strength,air_boundary):

    # To store the boundary
    ice_boundary = []

    # Iterate through all columns to get the best row where chance of boundary being present is highest
    for j in range(edge_strength.shape[1]):
        temp = []
        max1 = -1
        best_row = 0

        # For each row in the column
        for i in range(air_boundary[j] + 11, edge_strength.shape[0]):

            # Divide by 100 to avoid overflow
            prob  = edge_strength[i][j] / 100

            # When prev column value is present go for maximum probability conditioned with a smoother boundary
            if j>0:
                if prob >max1 and (i - air_boundary[j] > 10) and abs(i - ice_boundary[j-1]) < 20:
                    max1 = prob
                    best_row = i

            # Find the maximum probability row in the column
            else:
                if prob > max1 and (i-air_boundary[j] > 10):
                    max1 = prob
                    best_row = i
        ice_boundary.append(best_row)
    return ice_boundary

# Viterbi algorithm for Fig (a)
def viterbi(edge_strength):

    # Array to store initial probability for column 0
    initial_probability = []

    # Matrix to store emission probability
    emission_probability = numpy.zeros((edge_strength.shape[0],edge_strength.shape[1]))

    # Count of same edge_strength mask values
    emission_count = {}
    for i in range(0, edge_strength.shape[0]):
        for j in range(0, 1):
            if edge_strength[i][j] not in  emission_count:
                emission_count[edge_strength[i][j]] = 1
            else:
                emission_count[edge_strength[i][j]] = emission_count[edge_strength[i][j]] + 1

    # Calculate Initial probability that is count of same strength mask values for that cell divided by the sum of column 0 cell values
    for i in range(edge_strength.shape[0]):
        initial_probability.append( emission_count[edge_strength[i][0]] / edge_strength.shape[0])

    # Calculate emission probability for each cell
    for i in range(edge_strength.shape[0]):
        for j in range(edge_strength.shape[1]):
             emission_probability[i][j] = edge_strength[i][j] / 100

    # Vtable and backtrackTable for viterbi algorithm
    VTable = numpy.zeros((edge_strength.shape[0],edge_strength.shape[1]))
    backtrackTable = numpy.zeros((edge_strength.shape[0],edge_strength.shape[1]))

    # For first column, store initial probability * emission probability for each row
    for i in range(0, edge_strength.shape[0]):
        VTable[i][0] = initial_probability[i] * emission_probability[i][0]
        backtrackTable[i][0] = -1

    # For next columns
    for j in range(1, edge_strength.shape[1]):

        # Get all previous probabilities
        prev_prob_entry = []
        for entry in VTable:
            prev_prob_entry.append(entry[j-1])

        # From all rows in column get the max of transition probability * previous probability
        for i in range(0, edge_strength.shape[0]):
            max1 = -1
            parent = 0

            # Here only considering neighboring cells till distance 4 otherwise 0 chance of transition from the cell
            # The values are found by trial and error
            for ind in range(0, edge_strength.shape[0]):
                if abs(ind - i) == 0:
                    transition_prob = 3.7
                elif abs(ind - i) == 2:
                    transition_prob = 3.6
                elif abs(ind - i) == 3:
                    transition_prob = 3.55
                elif abs(ind - i) == 4:
                    transition_prob = 3.5
                else:
                    transition_prob = 0

                prob = transition_prob * prev_prob_entry[ind]

                if max1 < prob:
                    max1 = prob
                    parent = ind

            # Store maximum value * emission probability in viterbi table
            VTable[i][j] = max1 * emission_probability[i][j]

            # Store parent that is row of max probability in backtrack table
            backtrackTable[i][j] = int(parent)

    return VTable,backtrackTable

def viterbiFeedback(edge_strength,row_coord, col_coord):

    # Stores emission probability
    emission_probability = numpy.zeros((edge_strength.shape[0],edge_strength.shape[1]))

    # Calculate emission_probability
    for i in range(edge_strength.shape[0]):
        for j in range(edge_strength.shape[1]):
             emission_probability[i][j] = edge_strength[i][j] / 100

    VTable = numpy.zeros((edge_strength.shape[0],edge_strength.shape[1]))
    backtrackTable = numpy.zeros((edge_strength.shape[0],edge_strength.shape[1]))

    # For given column probability is 0 for all columns except given column whose probability is 1
    for prob in range(0, edge_strength.shape[0]):
       VTable[i][row_coord] = 0
       backtrackTable[i][row_coord] = -1

    # Store 1 as probability in given row,column
    VTable[row_coord][col_coord] = 1

    # Store the given row coordinate in the backtrack table
    backtrackTable[row_coord][col_coord] = row_coord


    if col_coord < (edge_strength.shape[1] - 1):
        # Starting from given column to last
        for j in range(col_coord + 1, edge_strength.shape[1]):

            # Get all previous row probabilities
            prev_prob_entry = []
            for entry in VTable:
                prev_prob_entry.append(entry[j-1])

            # Calculate the max of transition * previous probability from all rows
            for i in range(0, len(VTable)):
                max1 = -1
                parent = 0

                # For transition only neighbors till distance 4 are considered, for remaining transition probability is 0
                # The values are found by trial and error
                for ind in range(0, len(prev_prob_entry)):
                    if abs(ind - i) == 0:
                        transition_prob = 3.7
                    elif abs(ind - i) == 1:
                        transition_prob = 3.6
                    elif abs(ind - i) == 2:
                        transition_prob = 3.55
                    elif abs(ind - i) == 3:
                        transition_prob = 3.5
                    else:
                        transition_prob = 0

                    prob = transition_prob * prev_prob_entry[ind]
                    if max1 < prob:
                        max1 = prob
                        parent = ind

                # Store maximum value * emission probability in viterbi table
                VTable[i][j] = max1 * emission_probability[i][j]

                # Store parent i.e row of max probability in backtrack table
                backtrackTable[i][j] = int(parent)

    if col_coord > 0:

        # From 0 till given column
        for j in range(col_coord-1, -1, -1):

           # Get all previous probabilities
           prev_prob_entry = [i[j +1] for i in VTable]

           # From all rows calculate max transition * previous probability
           for i in range(0, len(VTable)):
                max1 = -1
                parent = 0

                # For transition only neighbors till distance 3 are considered, for remaining transition probability is 0
                # The values are found by trial and error
                for ind in range(0, len(prev_prob_entry)):
                    if abs(ind - i) == 0:
                        transition_prob = 3.7
                    elif abs(ind - i) == 1:
                        transition_prob = 3.6
                    elif abs(ind - i) == 2:
                        transition_prob = 3.55
                    elif abs(ind - i) == 3:
                        transition_prob = 3.5
                    else:
                        transition_prob = 0

                    prob = transition_prob * prev_prob_entry[ind]
                    if max1 < prob:
                        max1 = prob
                        parent = ind

                # Store maximum value * emission probability in viterbi table
                VTable[i][j] = max1 * emission_probability[i][j]

                # Store parent i.r row of max probability in backtrack table
                backtrackTable[i][j] = int(parent)

    return VTable,backtrackTable


def backTrackWithFeedbackAir(VTable, backtrackTable,col_coord):

    # Get max probability from last column of Vtable
    prob = [prob[len(VTable[0]) - 1] for prob in VTable]
    max1 = -1
    parent = 0
    for ind in range(0, len(prob)):
        if max1< prob[ind]:
            max1 = prob[ind]
            parent = ind

    # Get the parent of last column row where the probability is max
    N = edge_strength.shape[1]
    viterbi_seq = [0] * edge_strength.shape[1]
    viterbi_seq[N-1] = int(backtrackTable[parent][len(VTable[0]) - 2])

    # Backtrack
    if col_coord < (len(VTable[0]) - 1):
        for i in range(N - 2, col_coord + 1, -1):
            viterbi_seq[i] = int(backtrackTable[viterbi_seq[i+1]][i])

    if col_coord > 0:

        # Get max column for row 0
        prob = [prob[0] for prob in VTable]
        max1 = -1
        parent = 0
        for ind in range(0, len(prob)):
            if max1 < prob[ind]:
                max1 = prob[ind]
                parent = ind

        # Starting from second column max probability row, trace the parents till the given column
        viterbi_seq[0] = int(backtrackTable[parent][0])
        for i in range(1, col_coord):
            viterbi_seq[i] = int(backtrackTable[viterbi_seq[i-1]][i])

    return viterbi_seq

def backTrackWithFeedbackIce(VTable, backtrackTable,col_coord,airice_feedback):
    # Get the maximum probability row in given column
    temp_boundary = []
    prob = [prob[len(VTable[0]) - 1] for prob in VTable]

    max1 = -1
    parent = 0

    if len(temp_boundary) > 0:
        max1 = VTable[temp_boundary[-1]][len(VTable[0])]
        parent = temp_boundary[-1]

    for ind in range(0, len(prob)):
        # If we have previous column max probability row value, Get the max probability cell conditioned to it being atleast 10 rows below air and trying to value smoother boundary
        if len(temp_boundary)>0:
            if max1 <= prob[ind] and ind-airice_feedback[ind] > 10 and abs(temp_boundary[-1] - ind) < 5:
                max1 = prob[ind]
                parent = ind
        # If we don't have a previous column max probability row value, just make sure that the ice boundary is atleast 10 cells lower than the air boundary
        else:
            if max1 <= prob[ind] and ind-airice_feedback[ind] > 10:
                max1 = prob[ind]
                parent = ind

    # Backtrack to get complete sequence
    N = edge_strength.shape[1]
    viterbi_seq = [0] * edge_strength.shape[1]
    viterbi_seq[N-1] = int(backtrackTable[parent][len(VTable[0]) - 2])

    if col_coord < len(VTable[0]) - 1:

        # Starting from second last column till given column backtrack
        for i in range(N - 2, col_coord, -1):
             viterbi_seq[i] = int(backtrackTable[viterbi_seq[i+1]][i])

    if (col_coord > 0):
        # Get max probability row for column 0
        prob = [prob[0] for prob in VTable]
        temp_boundary = []

        max1 = -1
        parent = 0
        if len(temp_boundary) > 0:
            max1 = VTable[temp_boundary[-1]][1]
            parent = temp_boundary[-1]

        for ind in range(0, len(prob)):
            # If we have previous column max probability row value, Get the max probability cell conditioned to it being atleast 10 rows below air and trying to value smoother boundary
            if len(temp_boundary) > 0:
                if max1 <= prob[ind] and ind-airice_feedback[ind] > 10 and abs(temp_boundary[-1] - ind) < 25:
                    max1 = prob[ind]
                    parent = ind
            # If we don't have a previous column max probability row value, just make sure that the ice boundary is atleast 10 cells lower than the air boundary
            else:
                if max1 <= prob[ind] and ind - airice_feedback[ind] > 10:
                    max1 = prob[ind]
                    parent = ind

        viterbi_seq[0] = int(backtrackTable[parent][0])

        # Starting from second column max probability row till the given column backtrack
        for i in range(1, col_coord):
             viterbi_seq[i] = int(backtrackTable[viterbi_seq[i-1]][i])
        return viterbi_seq
# main program
#
if __name__ == "__main__":

    if len(sys.argv) != 6:
        raise Exception("Program needs 5 parameters: input_file airice_row_coord airice_col_coord icerock_row_coord icerock_col_coord")

    input_filename = sys.argv[1]
    gt_airice = [ int(i) for i in sys.argv[2:4] ]
    gt_icerock = [ int(i) for i in sys.argv[4:6] ]

    # load in image
    input_image = Image.open(input_filename).convert('RGB')
    input_image1 = Image.open(input_filename).convert('RGB')
    image_array = array(input_image.convert('L'))

    # compute edge strength mask -- in case it's helpful. Feel free to use this.
    edge_strength = edge_strength(input_image)
    imageio.imwrite('edges.png', uint8(255 * edge_strength / (amax(edge_strength))))

    # You'll need to add code here to figure out the results! For now,
    # just create some random lines.

    # Calculate airice boundary using simple algorithm
    airice_simple = simple_air(edge_strength)

    # Calculate airice boundary using viterbi algorithm
    VTable_icerock_simple,backtrackTable_icerock_simple = viterbi(edge_strength)

    # Get max probability row in last column and backtrack
    temp_boundary = []
    prob = [prob[len(VTable_icerock_simple[0])-1] for prob in VTable_icerock_simple]
    max1 = -1
    parent = 0
    for ind in range(0, len(prob)):
        if max1 < prob[ind]:
            max1 = prob[ind]
            parent = ind

    N = edge_strength.shape[1]
    viterbi_seq = [0] * edge_strength.shape[1]

    # Store index of max probability row in the viterbi table
    viterbi_seq[N-1] = int(backtrackTable_icerock_simple[parent][len(VTable_icerock_simple[0]) - 1])
    # From last column to 0 column backtrack to get the sequence
    for i in range(N-2, -1, -1):
        viterbi_seq[i] = int(backtrackTable_icerock_simple[viterbi_seq[i+1]][i])

    airice_hmm = viterbi_seq

    # Calculate airice boundary using hmm with human feedback
    VTable_airice_feedback,backtrackTable_airice_feedback = viterbiFeedback(edge_strength,int(gt_airice[0]), int(gt_airice[1]) )
    airice_feedback = backTrackWithFeedbackAir(VTable_airice_feedback,backtrackTable_airice_feedback, int(gt_airice[1]))

    # Edge strength with airice boundary values marked as 0 to be used to aid finding icerock boundary
    edge_strength1 = copy.deepcopy(edge_strength)
    for i in range(len(airice_hmm)):
        prob = airice_hmm[i]
        j = 0
        while(j < prob + 11):
            j += 1
            edge_strength1[j][i] = 0

    # Find icerock boundary using simple algorithm
    icerock_simple = simple_ice(edge_strength1,airice_simple)

    # Viterbi for icerock
    VTable_icerockhmm,backtrackTable_icerockhmm = viterbi(edge_strength1)
    temp_boundary = []

    # Get max row probability from last column
    prob = [prob[len(VTable_icerockhmm[0])-1] for prob in VTable_icerockhmm]

    max1 = -1
    parent = 0
    if len(temp_boundary)>0:
        max1 = VTable_icerockhmm[temp_boundary[-1]][len(VTable_icerockhmm[0]) + 1]
        parent = temp_boundary[-1]

    # For each row find the ice boundary conditioned to it is atleast 10 values below the ice and also that the boundary is smooth
    for index in range(0, len(prob)):

        if len(temp_boundary) > 0:
            if max1 <= prob[index] and index-airice_hmm[index] > 10 and abs(temp_boundary[-1] - index) < 5:
                max1 = prob[index]
                parent = index
        else:
            if max1 <= prob[index] and index-airice_hmm[index] > 10:
                max1 = prob[index]
                parent = index

    N = edge_strength.shape[1]
    viterbi_seq = [0] * edge_strength.shape[1]

    # Store index of max probability row in the viterbi table
    viterbi_seq[N-1] = int(backtrackTable_icerockhmm[parent][len(VTable_icerock_simple[0]) - 2])

    for i in range(N-2, -1, -1):
        viterbi_seq[i] = int(backtrackTable_icerockhmm[viterbi_seq[i+1]][i])

    icerock_hmm =  viterbi_seq

    # Calculate icerock boundary with feed back
    VTable_icerock_feedback,backtrackTable_icerock_feedback = viterbiFeedback(edge_strength1,int(gt_icerock[0]), int(gt_icerock[1]) )
    icerock_feedback = backTrackWithFeedbackIce(VTable_icerock_feedback,backtrackTable_icerock_feedback, int(gt_icerock[1]),airice_feedback)

    # Now write out the results as images and a text file
    write_output_image("air_ice_output.png", input_image, airice_simple, airice_hmm, airice_feedback, gt_airice)
    write_output_image("ice_rock_output.png", input_image1, icerock_simple, icerock_hmm, icerock_feedback, gt_icerock)
    with open("layers_output.txt", "w") as fp:
        for i in (airice_simple, airice_hmm, airice_feedback, icerock_simple, icerock_hmm, icerock_feedback):
            fp.write(str(i) + "\n")