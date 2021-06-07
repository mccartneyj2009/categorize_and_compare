def string_cleaner(site_name, prev_file, current_file):
    # Convert prev pg list to dictionary
    prev_pg_list = prev_file['program'].replace('\n\n', ',').split(sep=',')
    prev_pg_dict = {}
    line_number = 1
    for line in prev_pg_list:
        prev_pg_dict[line_number] = line.strip()
        line_number += 1

    # Convert current pg list to dictionary
    current_pg_list = current_file['program'].replace('\n\n', ',').split(sep=',')
    current_pg_dict = {}
    line_number = 1
    for line in current_pg_list:
        current_pg_dict[line_number] = line.strip()
        line_number += 1

    # Keep track of where the differences are with a dictionary
    pg_diffs = {}
    diff_count = 0
    with open(f'Differences Report - {site_name}.txt', 'a') as f:
        f.write(f'---------------Comparison: "{prev_file["file_name"]}" and "{current_file["file_name"]}"---------------\n')
        for line, string in prev_pg_dict.items():
            for l, s in current_pg_dict.items():
                if line == l:
                    if string == s:
                        pass
                        #f.write(f'Line {line} of "{prev_file["file_name"]}" and "{current_file["file_name"]}" are the same\n\n')
                    else:
                        diff_count += 1
                        diff_dict = {'oldPGLine': line, 'oldPGString': string, 'newPGLine': l, 'newPGString': s}
                        pg_diffs[diff_count] = diff_dict
                        f.write(f'Line {line} {prev_file["file_name"]}:\n\tLine {line}: {string}\nLine {l} {current_file["file_name"]}:\n\tLine {l}: {s}\n\n')
        f.write(f'Total differences for\n\t{prev_file["file_name"]}\n\t{current_file["file_name"]}\n\tTotal:{diff_count}\n\n')
    return diff_count


# pf = {'path_to_file': 'OSU A/BDE Extract PG.txt PGs/Type A', 'file_name': 'Device 51101 - PG80 - BDE Extract PG.txt', 'program': '//Main PG\n\n this is line 1\n\n this is line 21'}
# cf = {'path_to_file': 'OSU A/BDE Extract PG.txt PGs/Device 51102 - PG80 - BDE Extract PG.txt', 'file_name': 'Device 51102 - PG80 - BDE Extract PG.txt', 'program': '//Main PG\n\n this is line 1     \n\n this is line 24'}
# string_cleaner('path', pf, cf)


    # with open(f'Differences Report - {site_name}.txt', 'a') as f:
    #     f.write(f'Total differences for\n\t{prev_file["file_name"]}\n\t{current_file["file_name"]}\n\tTotal:{diff_count}\n{}\n\n')


