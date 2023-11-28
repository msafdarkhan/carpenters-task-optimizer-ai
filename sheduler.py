
# pip install PuLP

import pandas as pd
from pulp import LpVariable, LpProblem, lpSum, LpMinimize, LpStatus, value

# Define constants
budget_per_job = 50  # Replace X with the budget per job
plywood_per_job = 2  # Replace Y with the square meters of plywood per job
auxiliary_hours_per_plywood = 4

# Number of carpenters
num_carpenters = 10
carpenters = range(1, num_carpenters + 1)

# Create a schedule dataframe
schedule_df = pd.DataFrame(index=carpenters, columns=['Day', 'Work', 'Plywood'])

# Create LP problem
problem = LpProblem("Carpenter_Schedule_Optimization", LpMinimize)

# Define decision variables
work_days = range(1, 7)  # 6 days work week
days_off = range(7, 19)  # 12 days leave per annum

work_vars = LpVariable.dicts("Work", (carpenters, work_days), 0, 1, LpMinimize)
days_off_vars = LpVariable.dicts("DayOff", (carpenters, days_off), 0, 1, LpMinimize)

# Objective function
problem += lpSum([work_vars[i][j] for i in carpenters for j in work_days]) + lpSum([days_off_vars[i][k] for i in carpenters for k in days_off]), "Total_Days"

# Constraints
for i in carpenters:
    problem += lpSum([work_vars[i][j] for j in work_days]) + lpSum([days_off_vars[i][k] for k in days_off]) <= 12, f"Leave_Constraint_{i}"

for j in work_days:
    problem += lpSum([work_vars[i][j] for i in carpenters]) == 1, f"One_Work_Day_Per_Week_{j}"

# Add more constraints based on your requirements

# Solve the problem
problem.solve()

# Check the status of the solution
if LpStatus[problem.status] == "Optimal":
    # Extract the schedule from the solution
    for i in carpenters:
        for j in work_days:
            if value(work_vars[i][j]) == 1:
                schedule_df.at[i, 'Day'] = j
                schedule_df.at[i, 'Work'] = "Work"
                schedule_df.at[i, 'Plywood'] = plywood_per_job + auxiliary_hours_per_plywood

            elif value(days_off_vars[i][j + 6]) == 1:
                schedule_df.at[i, 'Day'] = j + 6
                schedule_df.at[i, 'Work'] = "Day Off"

    print(schedule_df)
else:
    print("No optimal solution found.")
