import sys
import os
import hashlib
args = sys.argv
try:
    files_stats = dict()
    for root, dirs, files in os.walk(args[1]):
        for name in files:
            file_size = os.path.getsize(os.path.join(root, name))
            file_path = os.path.join(root, name)
            if file_size not in files_stats.keys():
                files_stats[file_size] = [file_path]
            else:
                files_stats[file_size].append(file_path)

    file_format = str(input('Enter file format:\n'))
    option = input('Size sorting options:\n1. Descending\n2. Ascending\n\nEnter a sorting option:\n')
    rever = {'1': True, '2': False}
    while option not in ['1', '2']:
        print('Wrong option')
        option = input('Enter a sorting option:\n')

    files_stats = {k: v for k, v in sorted(files_stats.items(), key=lambda key: key[0], reverse=rever[option])}

    for i in files_stats.keys():
        print(i, 'bytes')
        for j in files_stats[i]:
            if file_format != '':
                if j.endswith(file_format):
                    print(j)
                else:
                    files_stats[i].remove(j)
            else:
                print(j)

    duplicates_check = input('Check for duplicates?\n')
    while duplicates_check not in ['yes', 'no']:
        print('Wrong option')
        duplicates_check = input('Check for duplicates?\n')

    if duplicates_check == 'yes':
        hash_dic = {size: {} for size in files_stats.keys()}
        for size, file_list in files_stats.items():
            for file in file_list:
                with open(file, 'rb') as f:
                    md_hash = hashlib.md5()
                    read = f.read()
                    md_hash.update(read)
                    hash_val = md_hash.hexdigest()
                    if hash_val not in hash_dic[size].keys():
                        hash_dic[size].update({hash_val: []})
                        hash_dic[size][hash_val].append(file)
                    else:
                        hash_dic[size][hash_val].append(file)
        n = 1
        duplicated_files = {}
        for size_file_group, inner_dict in hash_dic.items():
            print(size_file_group, "bytes")
            for hash_value, file_lst in inner_dict.items():
                if len(file_lst) > 1:
                    print("Hash: ", hash_value)
                    for dup_file in file_lst:
                        print(f"{n}. {dup_file}")
                        duplicated_files[str(n)] = (size_file_group, dup_file)
                        n += 1

    delete_check = input('Delete files?\n')
    while delete_check not in ['yes', 'no']:
        print('Wrong option')
        delete_check = input('Delete files?\n')

    if duplicates_check:
        if delete_check == 'yes':
            file_to_delete = input('Enter file numbers to delete:\n').split()
            while len(file_to_delete) == 0 or\
                    set(duplicated_files.keys()).intersection(set(file_to_delete)) != set(set(file_to_delete)):
                print('Wrong format')
                file_to_delete = input('Enter file numbers to delete:\n').split()
            freed_up_space = 0
            for file_number in file_to_delete:
                os.remove(duplicated_files[file_number][1])
                freed_up_space += duplicated_files[file_number][0]
            print(f'Total freed up space: {freed_up_space} bytes')


except IndexError:
    print('Directory is not specified')