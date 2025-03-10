import openpyxl

def schedule_maintenance(tasks, num_years):
    """
    Calculates maintenance tasks scheduled for each 10th day over a specified number of years.

    Args:
        tasks: A list of tuples, where each tuple contains (task_number, interval_days).
        num_years: The number of years to schedule for.

    Returns:
        A list of tuples, where each tuple contains (day, list_of_tasks_to_do).
    """

    days_in_year = 365  # Approximation, doesn't account for leap years perfectly.
    total_days = ((num_years * days_in_year) + 1)
    schedule = []
    total_tasks = 0

    for day in range(10, total_days + 1, 10):  # Iterate every 10th day
        tasks_to_do = []
        for task_num, interval in tasks:
            if day % interval == 0:
                tasks_to_do.append(task_num)
                total_tasks += 1 # Adds 1 to total_tasks per added task

        if tasks_to_do:
            schedule.append((day, tasks_to_do))
        
    print("Total tasks in this 5 year plan is: ",total_tasks)

    return schedule

# Example usage:
maintenance_tasks = [
    (1, 10),
    (2, 20),
    (3, 40),
    (4, 40),
    (5, 50),
    (6, 50),
    (7, 80),
    (8, 120),
    (9, 150),
    (10, 200),
    (11, 200),
    (12, 250),
    (13, 250),
    (14, 300),
    (15, 300),
    (16, 300),
    (17, 300),
    (18, 300),
    (19, 360),
    (20, 400),
    (21, 400),
    (22, 400),
    (23, 400),
    (24, 400),
    (25, 400),
    (26, 500),
    (27, 650),
    (28, 830),
    (29, 830),
    (30, 1250),
    (31, 1250),
    (32, 1250),
    (33, 1250),
    (34, 1250),
    (35, 1250),
    (36, 1250),
    (37, 1250),
    (38, 1750),
]

maintenance_schedule = schedule_maintenance(maintenance_tasks, 5)

# Create an Excel workbook
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.append(["Day", "Tasks"])  # Header row

# Write the schedule to the Excel sheet
for day, tasks in maintenance_schedule:
    sheet.append([day, ", ".join(map(str, tasks))]) # convert task list to comma seperated string

# Save the Excel file
workbook.save("maintenance_schedule.xlsx")

# Print the schedule to the console (optional)
for day, tasks in maintenance_schedule:
    print(f"Day {day}: Tasks to do - {tasks}")

