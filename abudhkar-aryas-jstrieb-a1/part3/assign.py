#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by:
#  primary
#   Aishwarya Budhkar (abudhkar)
#  secondary
#   Jacob Striebel    (jstrieb)
#   Shubhavi Arya     (aryas)
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#
# References:
# https://docs.python.org/3/library/itertools.html
# https://docs.python.org/3/library/copy.html

import sys
import itertools
import copy

"""
 This function reads the input file and
 creates data structures to store the students, teams, requested, requested_teammates and not_requested dictionaries
"""
def read_file(input_file):
    input_file = open(input_file, "r")
    lines = input_file.readlines()

    # List of students
    students = []

    # Teams with each student alone
    teams = []

    # Dictionary to store the teammates requested by a student
    # eg {djcran: [vkvats,nthakurd]}
    requested_dict = {}

    # Dictionary to store the number of teammates requested by each student
    # eg {djcran: 3}
    requested_teamsize = {}

    # Dictionary to store the teammates that the student does not wish to work with
    # eg {nthakurd: [fajun, djcran]}
    not_requested_dict = {}

    # Read each line
    for line in lines:

        # Split by ' '
        data = line.rstrip().split(" ")

        # Store all student names in students list
        students.append(data[0])

        # Create teams list with each student working as individual and - indicating open spot in team
        # All teams are of size 3
        teams.append([data[0],'-','-'])

        # Get team size requested by student
        team_size = len(data[1].split("-"))

        # Teammates requested by student
        requested_teammates = data[1].split("-")

        # List of students that the student does not wish to work with
        requested_to_not_work_teammates = data[2].split(",")

        # Code to create the requested dictionary
        requested_list = []
        not_requested_list = []
        for teammate in requested_teammates[1:]:
            if(teammate != "xxx" and teammate != 'zzz'):
                requested_list.append(teammate)
        requested_dict[data[0]] = (requested_list)

        # Code to create not_requested dictionary
        for teammate in requested_to_not_work_teammates:
            if(teammate!='_'):
                not_requested_list.append(teammate)
        not_requested_dict[data[0]] = (not_requested_list)
        requested_teamsize[data[0]] = (team_size)

    return students, teams, requested_dict, not_requested_dict, requested_teamsize

"""
 This function computes the cost associated with formation of groups of size 3 or less
 with each student included in one and only one team
"""
def compute_cost(initial_teams,  requested_dict ,requested_teamsize, not_requested_dict):

    # Get the number of groups in the arrangement
    n = len(initial_teams)

    # Stores the number of students whom a student has not requested but have been assigned in his team for all the students in the arrangement
    count_not_requested = 0

    # Stores the number of students requested but not assigned in his team for all the students in the arrangement
    count_requested_but_not_assigned = 0

    # Stores the number of students who were not assigned the group size they requested
    count_wrong_team_size = 0

    # Following lines of code remove the '-' (no teammate present) from the teams for cost computation
    team2 = []

    for r in initial_teams:
        team1 = []
        for c in r:
            if c != '-':
                team1.append(c)
        team2.append(team1)

    """
    For all the groups compute and add :
    1. the number of teammates requested but not assigned,
    2. number of teammates assigned that were not wanted,
    3. number of students who were not assigned the group size that they requested
    """
    for team in team2:

        if(len(team) == 1):
            first = team[0]
            first_requested = requested_dict[first]
            for teammate in first_requested:
                count_requested_but_not_assigned += 1

            first_requested_team_size = requested_teamsize[first]
            if(len(team) != first_requested_team_size):
                count_wrong_team_size += 1

        if(len(team) == 2):
            first = team[0]
            second = team[1]

            first_not_requested = not_requested_dict[first]
            for teammate in first_not_requested:
               if(teammate == second):
                   count_not_requested += 1

            second_not_requested = not_requested_dict[second]
            for teammate in second_not_requested:
               if(teammate == first):
                   count_not_requested += 1

            first_requested = requested_dict[first]
            for teammate in first_requested:
                if(teammate == second):
                   continue
                count_requested_but_not_assigned+=1

            second_requested = requested_dict[second]
            for teammate in second_requested:
                if(teammate == first):
                   continue
                count_requested_but_not_assigned += 1

            first_requested_team_size = requested_teamsize[first]
            if(len(team) != first_requested_team_size):
                count_wrong_team_size += 1

            second_requested_team_size = requested_teamsize[second]
            if(len(team) != second_requested_team_size):
                count_wrong_team_size += 1

        if(len(team) == 3):
            first = team[0]
            second = team[1]
            third = team[2]

            first_not_requested = not_requested_dict[first]
            for teammate in first_not_requested:
                if(teammate == second):
                    count_not_requested += 1
                if(teammate == third):
                    count_not_requested += 1

            second_not_requested = not_requested_dict[second]
            for teammate in second_not_requested:
               if(teammate == first):
                   count_not_requested += 1
               if(teammate == third):
                   count_not_requested += 1

            third_not_requested = not_requested_dict[third]
            for teammate in third_not_requested:
               if(teammate == second):
                   count_not_requested += 1
               if(teammate == first):
                   count_not_requested += 1

            first_requested = requested_dict[first]
            for teammate in first_requested:
                if(teammate == second or teammate == third):
                   continue
                count_requested_but_not_assigned+=1

            second_requested = requested_dict[second]
            for teammate in second_requested:
               if(teammate == first or teammate == third):
                   continue
               count_requested_but_not_assigned += 1

            third_requested = requested_dict[third]
            for teammate in third_requested:
               if(teammate == first or teammate == second):
                   continue
               count_requested_but_not_assigned += 1

            first_requested_team_size = requested_teamsize[first]
            if(len(team) != first_requested_team_size):
                count_wrong_team_size += 1

            second_requested_team_size = requested_teamsize[second]
            if(len(team) != second_requested_team_size):
                count_wrong_team_size += 1

            third_requested_team_size = requested_teamsize[third]
            if(len(team) != third_requested_team_size):
                count_wrong_team_size += 1

    # Return cost to form the arrangement of teams
    return ((5 * n) + (10 * count_not_requested) + (3 * count_requested_but_not_assigned) + (2 * count_wrong_team_size))

def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
    - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
        much time it will take to find the best solution, you can compute a series of solutions and then
        call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
        our test program will take the last answer you 'yielded' once time expired.
    """

    # Read input file
    students, teams, requested_dict, not_requested_dict, requested_teamsize = read_file(input_file)

    # Start with groups with each student being in his own group alone
    fringe = [teams]

    # Compute the cost
    old_cost = compute_cost(teams,requested_dict ,requested_teamsize, not_requested_dict)

    # Stop when cost is not lowered for 100 iterations
    threshold = 0

    # Variables to store final successor and cost
    final_succ = []
    final_cost = []

    # To avoid duplicate computation
    cost_dict = {}

    while len(fringe) > 0:
        # Get the successor
        for succ in successor(fringe.pop(), students, requested_dict ,requested_teamsize, not_requested_dict, cost_dict):
            # Get cost for the successor
            succ_cost = compute_cost(succ,requested_dict ,requested_teamsize, not_requested_dict)

            # Yield a solution
            teams_formed = get_printable_teams(succ)
            yield({"assigned-groups": ["-".join(i) for i in teams_formed], "total-cost" : succ_cost})

            final_cost = succ_cost
            final_succ = succ

            # Add successor to fringe
            fringe.append(succ)


    # Yield solution
    final_teams_formed = get_printable_teams(final_succ)
    yield({"assigned-groups": ["-".join(i) for i in final_teams_formed], "total-cost" : final_cost})
    return

"""
 This functions takes a team formation as input
 Forms all the successor group arrangements of a group arrangement by creating and combining different permutations of teams
 Returns the successor with least cost
"""
def successor(teams, students, requested_dict ,requested_teamsize, not_requested_dict, cost_dict):

    succ = []
    succ_dict = {}
    min_cost_succ = teams
    min_succ_cost = compute_cost(teams,  requested_dict ,requested_teamsize, not_requested_dict)
    """
    Following lines create combinations of teams to find a potentially low cost successor arrangement of current arrangement
    """
    for k in range(0,len(teams)):
        for l in range(0, len(teams)):
            if(k != l):
                team_combinations = []

                # Create all permutations of team1
                team1_permutation = list(set(itertools.permutations(teams[k])))

                # Create all permutations of team2
                team2_permutation = list(set(itertools.permutations(teams[l])))

                for team1 in team1_permutation:
                    for team2 in team2_permutation:
                        for i in range(0,len(team1)):
                            for j in range(0, len(team2)):
                                # If no student present in one permutation and a student present in another, exchange
                                if(list(team1)[i] == '-' and list(team2)[j] != '-' and team2[j] not in list(team1)):
                                    list1_copy = list(team1)
                                    list2_copy = list(team2)
                                    list1_copy[i] = list(team2)[j]
                                    list2_copy[j] = '-'
                                    # Add the new teams to team_combinations
                                    team_combinations.append([list1_copy,list2_copy])

                # We need to get this copy to replace the old teams with new teams and get a successor
                teams_copy = copy.deepcopy(teams)
                # Delete the kth team
                del teams_copy[k]

                # The index of l changes if k comes before l in the list
                if(k < l):
                    del teams_copy[l-1]
                else:
                    del teams_copy[l]

                # Remove duplicated from the team_combinations
                k1 = list(i for i in team_combinations)
                team_combinations = list(k1 for k1,_ in itertools.groupby(k1))
                for i in team_combinations:
                    # Add the new teams to create a successor
                    teams_copy.append(i[0])
                    teams_copy.append(i[1])

                    # If all students are not present in the successor group formation do not proceed
                    # Check if new group arrangement is valid
                    if(check_if_all_students_assigned(students, teams_copy)):

                        # Check if the new successor cost is less the minimum_successor_cost
                        new_succ = []

                        # Remove from new teams the teams with no members
                        for team in teams_copy:
                            if(team[0] == '-' and team[1] == '-' and team[2] == '-'):
                                continue
                            new_succ.append(team)

                        # To avoid duplicate computation
                        if(str(new_succ) not in succ_dict):
                            succ_dict[str(new_succ)] = []

                            # Use cached cost if already calculated
                            if(str(new_succ) in cost_dict):
                                new_succ_cost = cost_dict[str(new_succ)]
                            else:
                                new_succ_cost = compute_cost(new_succ,requested_dict ,requested_teamsize, not_requested_dict)
                                cost_dict[str(new_succ)] = new_succ_cost

                            if new_succ_cost < min_succ_cost:
                                min_succ_cost = new_succ_cost
                                min_cost_succ = new_succ

                        teams_copy = copy.deepcopy(teams)

                        del teams_copy[k]

                        if(k < l):
                            del teams_copy[l-1]
                        else:
                            del teams_copy[l]
    succ.append(min_cost_succ)
    return succ

"""
Checks if all students are present in a groups arrangement to check if the arrangement is a valid successor
"""
def check_if_all_students_assigned(students, teams):
    students_in_team = []
    for team in teams:
        for student in team:
            students_in_team.append(student)
    for student in students:
        if( student not in students_in_team):
            return False
    return True

# Function to remove '-' from the teams from a given group arrangement for correct display format required
def get_printable_teams(succ):
    teams_formed = []
    for team in succ:
        team_formed = []
        for student in team:
            if student != '-':
                team_formed.append(student)
        teams_formed.append(team_formed)
    return teams_formed


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
