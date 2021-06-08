import os
import sys
import string_cleaner
from os import mkdir


def create_file_types(site_name, differences, type_count=1):
    try:
        # Look at what directories and files are in root directory
        types = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E',
                 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J',
                 11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O',
                 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T',
                 21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y',
                 26: 'Z', 27: 'AA', 28: 'BB', 29: 'CC', 30: 'DD',
                 31: 'EE', 32: 'FF', 33: 'GG', 34: 'HH', 35: 'II',
                 36: 'JJ', 37: 'KK', 38: 'LL', 39: 'MM', 40: 'NN',
                 41: 'OO', 42: 'PP', 43: 'QQ', 44: 'RR', 45: 'SS',
                 46: 'TT', 47: 'UU', 48: 'VV', 49: 'WW', 50: 'XX',
                 51: 'YY', 52: 'ZZ'}

        contents_of_directory = os.listdir(f'{site_name}')
        try:
            for item in contents_of_directory:
                path = f'{site_name}/{item}'  # path = OSU Something/<specific PG folder>
                if os.path.isdir(path):
                    files = os.listdir(f"{path}")
                    # iterate over files in specific program directories
                    prev_file = {}
                    for file in files:
                        if not os.path.isdir(f'{path}/{file}'):  # if its an actual file and not a directory
                            if prev_file == {}:  # This is the first time thru files after starting the app
                                if not os.path.isdir(f'{path}/{file}'):
                                    if not os.path.isdir(f'{path}/{types[type_count]}'):
                                        mkdir(f'{path}/Type {types[type_count]}')
                                        os.rename(f'{path}/{file}', f'{path}/Type {types[type_count]}/{file}')
                                    else:
                                        os.rename(f'{path}/{file}', f'{path}/Type {types[type_count]}/{file}')
                                    with open(f'{path}/Type {types[type_count]}/{file}', 'r') as f:
                                        pg = f.read()
                                    prev_file = {'path_to_file': f'{path}/Type {types[type_count]}', 'file_name': f'{file}', 'program': pg}
                            else:
                                # compare to whats in the type directories. if no match then insert into the next empty directory
                                with open(f'{path}/{file}', 'r') as f:
                                    current_program = f.read()
                                current_file = {'path_to_file': f'{path}/{file}', 'file_name': f'{file}', 'program': current_program}
                                total_differences = string_cleaner.string_cleaner(site_name, prev_file, current_file)
                                if total_differences < differences:
                                    os.rename(f'{current_file["path_to_file"]}', f'{path}/Type {types[type_count]}/{file}')

        except:
            e = sys.exc_info()[0]
            print(e)
        type_count += 1
        if type_count > 52:
            sys.exit()
        create_file_types(site_name, differences, type_count)
    except:
        pass
