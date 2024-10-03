import csv
import os
def file_exists(path):
    return os.path.exists(path)
def get_user_input1():

    print("if you do not want to use more placeholders give an empty column number to it"
          "and to use the placeholders, you will need to write %placeholder1 in your message template")

    math_column_index = int(input("Enter the column index (0-based) for the placeholder1: "))
    science_column_index = int(input("Enter the column index (0-based) for the placeholder2: "))
    hindi_column_index = int(input("Enter the column index (0-based) for the placeholder3: "))
    english_column_index = int(input("Enter the column index (0-based) for the placeholder4: "))
    social_science_column_index = int(input("Enter the column index (0-based) for the placeholder5: "))




    return  math_column_index, science_column_index, \
           hindi_column_index, english_column_index, social_science_column_index,

def get_last_row_index(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        total_rows = sum(1 for _ in reader)
    return total_rows - 1

def extract_numerical_digits(s):
    return ''.join(filter(str.isdigit, s))
def get_valid_input(prompt, validation_func, default_value=None):
    while True:
        user_input = input(prompt)
        if not user_input and default_value is not None:
            return default_value
        if validation_func(user_input):
            return user_input
        print("Invalid input. Please try again.")