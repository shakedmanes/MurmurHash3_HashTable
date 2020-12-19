"""
Main file used for running the task.

Get input from the user for M and K values for the hash table and creates it,
read input file values and insert them into the hash table,
read check file values and test their existence in the hash table while showing results
of existence for each value.

In the end also show report which contains:
* List of values entered into the hash table.
* List of values checked existence in the table.
* Error percentage of the check existence function of the hash table.
* Errors occurred by the check existence function of the hash table.
"""

from os.path import isfile as is_file_exists
from os import system
import hash_table as hash_table_module

# Little hack for allowing console colors to work on windows cmd.
system('')

# Input files paths.
INPUT_LIST_FILE_PATH = './input-files/input_list.txt'
CHECK_LIST_FILE_PATH = './input-files/check_list.txt'

# Console colors for the print statements.
CONSOLE_COLORS = {
    'SUCCESS': '\x1b[1;32;40m',
    'WARNING': '\x1b[1;31;40m',
    'ERROR': '\x1b[2;31;40m',
    'RESET_COLOR': '\x1b[0m',
    'UNDERLINE': '\x1b[4;37;40m',
}

"""
Utilities functions used for reading and performing actions on input files content.
"""


def read_file_and_perform_action(file_path, action):
    """
    Reads a file which contains comma separated values and perform action on each value.

    :param file_path: Path of the file to read.
    :param action: Function which receives as first argument some value of the file.
    """

    # Check if the file is exists to avoid errors.
    if not is_file_exists(file_path):
        raise FileNotFoundError('{} path given is not exists.'.format(file_path))

    # Perform action for each value found in the file.
    with open(file_path, 'r') as file_handle:
        for line in file_handle.readlines():
            values_in_line = line.split(',')
            for value in values_in_line:
                action(value.strip())


def insert_action(hash_table_instance, current_values_list, value):
    """
    Insert action which perform insert of given value to hash table instance and
    current values list.

    :param hash_table_instance: HashTable class instance.
    :param current_values_list: List of current values entered to the hash table.
    :param value: Value to insert into the hash table and the current values entered list.
    """

    # Insert value for hash table and current values list.
    hash_table_instance.insert(value)
    current_values_list.append(value)


def test_existence_action(hash_table_instance, current_values_list, check_values_list, errors_list, value):
    """
    Text existence action which perform the check existence function of a given hash table instance.

    Add each value to the given check values list, which contains all the values currently checked.
    While checking existence, check if the result was an error regarding the given current values list,
    which contains the values inserted to the hash table.

    Add any error to the given errors list, and print the result of the existence check.

    :param hash_table_instance: HashTable class instance.
    :param current_values_list: List of current values entered to the hash table.
    :param check_values_list: List of current check values.
    :param errors_list: List of current errors noticed.
    :param value: Value to check existence in the hash table.
    """

    # Insert the value into the checked values list.
    check_values_list.append(value)

    # Check if really suppose to be exist in hash table.
    really_exists = value in current_values_list

    # Check of existence in the hash table.
    if hash_table_instance.check_existence(value):
        if not really_exists:
            errors_list.append(
                '{}Value {} considered exist in hash table{}'.format(
                    CONSOLE_COLORS['ERROR'],
                    value,
                    CONSOLE_COLORS['RESET_COLOR']
                )
            )
        print(
            '{}V - {} exists in the hash table.{}'.format(
                CONSOLE_COLORS['SUCCESS'],
                value,
                CONSOLE_COLORS['RESET_COLOR']
            )
        )
    else:
        if really_exists:
            errors_list.append(
                '{}Value {} considered NOT exist in hash table.{}'.format(
                    CONSOLE_COLORS['ERROR'],
                    value,
                    CONSOLE_COLORS['RESET_COLOR']
                )
            )
        print(
            '{}X - {} NOT exists in the hash table.{}'.format(
                CONSOLE_COLORS['WARNING'],
                value,
                CONSOLE_COLORS['RESET_COLOR']
            )
        )


def print_results_report(inserted_values_list, check_values_list, errors_list):
    """
    Print detailed results report, contains inserted values list and check values list.
    Print error percentage and the errors noticed by the check existence function of the hash table.

    :param inserted_values_list: List of values entered to the hash table.
    :param check_values_list: List of values which checked existence in the hash table.
    :param errors_list: List of current errors noticed by the results of check existence function of the hash table.
    """
    print(
        '\n{}Values inserted into the hash table:{}'.format(
            CONSOLE_COLORS['UNDERLINE'],
            CONSOLE_COLORS['RESET_COLOR']
        )
    )
    print(inserted_values_list)

    print(
        '{}Values which tested existence in the hash table:{}'.format(
            CONSOLE_COLORS['UNDERLINE'],
            CONSOLE_COLORS['RESET_COLOR']
        )
    )
    print(check_values_list)

    print(
        '\n{}Errors percentage{}: {:.2f}%'.format(
            CONSOLE_COLORS['UNDERLINE'] + CONSOLE_COLORS['ERROR'],
            CONSOLE_COLORS['RESET_COLOR'],
            len(errors_list) * (100.0 / len(check_values_list))
        )
    )
    print(
        '\n{}Errors noticed:{}\n'.format(
            CONSOLE_COLORS['UNDERLINE'] + CONSOLE_COLORS['ERROR'],
            CONSOLE_COLORS['RESET_COLOR'],
        )
    )

    if len(errors_list) == 0:
        print('NONE.')
    else:
        for error in errors_list:
            print('{}{}{}.'.format(CONSOLE_COLORS['ERROR'], error, CONSOLE_COLORS['RESET_COLOR']))


"""
Actual main program which runs the task.
"""

# Getting m value from user input.
m = input('Enter m value for the hash table (Size of the hash table): ')
while not m.isdecimal():
    print('Invalid input for m value - m must be integer')
    m = input('Enter m value for the hash table (Size of the hash table): ')

# Getting k value from user input.
k = input('Enter k value for the hash table (Number of hash functions): ')
while not k.isdecimal():
    print(print('Invalid input for m value - m must be integer'))
    k = input('Enter k value for the hash table (Number of hash functions): ')

# Create hash table with given input values.
hash_table = hash_table_module.HashTable(int(k), int(m))

# Create list for collecting the values entered to the hash table for calculating
# error percentage at the end of the existence test with the check list.
current_inserted_values = []

# Create list for collecting the values which will be checked existence in the hash table.
current_checked_values = []

# Create list for collecting errors by existence check of the hash table.
errors = []

# Read input file and insert values to hash table and current inserted values list.
read_file_and_perform_action(
    INPUT_LIST_FILE_PATH,
    lambda value: insert_action(hash_table, current_inserted_values, value)
)

# Read check list file and test existence of each value in the hash table, while collecting errors.
print('\nChecking existence for check list:')
read_file_and_perform_action(
    CHECK_LIST_FILE_PATH,
    lambda value: test_existence_action(
        hash_table,
        current_inserted_values,
        current_checked_values,
        errors,
        value
    )
)

# Print detailed report of the results of the check existence of the hash table.
print_results_report(current_inserted_values, current_checked_values, errors)
