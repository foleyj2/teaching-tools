import pandas as pd
import numpy as np

np.random.seed(123)

df = pd.read_excel('Picking a project(1-28).xlsx', sheet_name='Sheet1')

num_groups_requested = df['How many teams do you want working on your project?'].tolist()

number_list = df['What is your project number assigned by Joe Foley?'].tolist()

requests = df['What teams would you want working on your project, with most preferred group number first. Separate with commas.'].tolist()

## Remove indices that have a nan value in either list
for i in range(len(number_list)-1, -1, -1):
    if np.isnan(number_list[i]) or requests[i] != requests[i]:
        del number_list[i]
        del requests[i]
        del num_groups_requested[i]

## split the strings by commas otherwise it is integer
requests = [i.split(',') if type(i) == str else [int(i)] for i in requests]
## convert to integers
group_interests = [[int(x.strip()) if type(x)==str else x for x in i] for i in requests]

projects = [int(i) for i in number_list]


def remove_first_index(group_interests):
    '''Take in a list of lists
    Iterate through the first index in all lists in group_interests
    if the first index is shared by another list, use random.choice to select one of the lists to remove the first index
    '''
    try:
        for i in range(len(group_interests)):        
            for j in range(i+1, len(group_interests)):
                if group_interests[i][0] == group_interests[j][0]:
                    winner = np.random.choice([i,j])
                    del group_interests[winner][0]
                    break
    except IndexError:
        pass
# Call the function before the main loop
remove_first_index(group_interests)


# Initialize an empty dictionary to store the project allocations
allocations = {project:[] for project in projects}

# Initialize an empty set to store the assigned groups
assigned_groups = set()

for project, n_groups in zip(projects, num_groups_requested):
    '''
    Iterate through the projects and try to fulfil the number of groups requested.
    '''
    
    # Iterate through the group interests for the current project
for project, n_groups in zip(projects, num_groups_requested):
    # Iterate through the group interests for the current project
    for group in group_interests[projects.index(project)]:
        # Check if the group has already been assigned to another project
        if group not in assigned_groups:
            # Assign the group to the current project
            allocations[project].append(group)
            assigned_groups.add(group)
            break
        # In case of a tie, select randomly between the projects
        else:
            other_projects = [p for p, g_list in allocations.items() if group in g_list]
            winner = np.random.choice(other_projects)
            # If the current project wins the tie, assign the group to the current project
            if winner == project:
                allocations[project].append(group)
                assigned_groups.add(group)
                break

## Check if the number of groups assigned is equal to the number requested
for project, n_groups in zip(projects, num_groups_requested):
    if len(allocations[project]) < n_groups:
        # Check if there are any groups in the project's interest list that have not been assigned to other projects yet
        # If there are, assign them to the current project
        for group in group_interests[projects.index(project)]:
            if group not in assigned_groups:
                allocations[project].append(group)
                assigned_groups.add(group)
            if len(allocations[project]) == n_groups:
                break


    
# Print the allocations
for project, groups in allocations.items():
    print(f'Project {project}: {groups}')

