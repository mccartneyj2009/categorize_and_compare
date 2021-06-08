import sys
import pyodbc
import os.path
from reporting import create_report
from create_file_types import create_file_types
from os import mkdir


def get_program_info(sql_statement):
    DSN = 'DSN=Delta ODBC 4'
    autocommit = True
    cnxn = pyodbc.connect(DSN, autocommit=autocommit)
    cursor = cnxn.cursor()
    sql_query_returned_list = [i for i in cursor.execute(sql_statement)]
    cursor.close()
    cnxn.close()
    return sql_query_returned_list


def working_loop():
    # retrieve all pg objects on a site
    site_name = input("Site Name: ")
    error_message = 'Enter an integer value.'
    while True:
        try:
            differences = int(input('Maximum differences until new Type? '))
            break
        except ValueError:
            print(error_message)
    while True:
        try:
            lower_index = int(input('First device in range? (Enter BACnet Address)'))
            break
        except ValueError:
            print(error_message)
    while True:
        try:
            upper_index = int(input('Last device in range? (Enter BACnet Address)'))
            break
        except ValueError:
            print(error_message)
    if os.path.isdir(f'{site_name}'):
        print('Directory already exists')
    else:
        mkdir(f'{site_name}')

    programs = [pg for pg in get_program_info(f"SELECT DEV_ID, INSTANCE, Program_Code, Object_Name FROM OBJECT_V4_PG WHERE SITE_ID = '{site_name}' AND DEV_ID BETWEEN {lower_index} AND {upper_index}")]
    number_of_errors = 0
    for pg in programs:
        dev_id, instance, pg_code, obj_name = pg[0], pg[1], pg[2], pg[3]
        try:
            obj_name = obj_name.replace('/', '_')
            if os.path.isdir(f'{site_name}'):
                with open(f'{site_name}/Device {dev_id} - PG{instance} - {obj_name}.txt', 'x') as file:
                    file.write(pg_code)
            else:
                mkdir(f'{site_name}')
                with open(f'{site_name}/Device {dev_id} - PG{instance} - {obj_name}.txt', 'x') as file:
                    file.write(pg_code)
        except:
            number_of_errors += 1
            e = sys.exc_info()[0]
            with open(f'ODBC Errors Report - {site_name}.txt', 'a')as f:
                f.write(f'{e} : {dev_id} : {obj_name}\n')

    # Get a list of files in directory and create base file structure
    with open('programs.txt', 'r') as pg_file:
        pg_names = [i.replace("\n", "") for i in pg_file.readlines()]
    contents_of_directory = os.listdir(f'{site_name}')
    for file in contents_of_directory:
        file_strings = file.split(sep=' - ')
        program_name = file_strings[2].split(sep='.')
        for pg_name in pg_names:
            if program_name[0] == pg_name:
                if os.path.isdir(f'{site_name}/{pg_name} PGs'):
                    os.rename(f'{site_name}/{file}', f'{site_name}/{pg_name} PGs/{file}')
                else:
                    mkdir(f'{site_name}/{pg_name} PGs')
                    os.rename(f'{site_name}/{file}', f'{site_name}/{pg_name} PGs/{file}')
    create_file_types(site_name, differences)
    create_report(site_name, pg_names)

    return 0
