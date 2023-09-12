#!/usr/bin/env python3

import sys
import os
import shutil
import re

def rename(packs):
    print('\n\n***Rename folders/files - replace all spaces and special characters to _***')
    triggers = [' ', '#', '%', '&', '\'', '*', '+', '/', ':', '?', '@', '<', '>', '|', '"', '©', '(', ')']
    for pack in packs:
        print('Renaming for %s' % pack)
        dir_list=[]
        for root, dirs, files in os.walk(pack):  
            for dir in dirs:
                dir_list.append(os.path.join(root, dir))
        for n in range(len(dir_list)):
            flag = False
            dir_item = dir_list[n]
            dirname = os.path.basename(dir_item)
            dir_dir = os.path.dirname(dir_item)
            for trigger in triggers:
                if trigger in dirname:
                    new_dirname = dirname.replace(trigger, '_')
                    os.rename(os.path.join(dir_dir,dirname),os.path.join(dir_dir,new_dirname))
                    flag = True
                    # print('Renamed %s to %s' % (os.path.join(dir_dir,dirname),os.path.join(dir_dir,new_dirname)))
                    # below is different from the loop for files
                    dir_list=[i.replace(dirname,new_dirname) if dirname in i else i for i in dir_list]
                    dirname = new_dirname
            if re.findall('__+', dirname):
                new_dirname = re.sub('__+', '_', dirname)
                os.rename(os.path.join(dir_dir,dirname),os.path.join(dir_dir,new_dirname))
                flag = True
                # print('Renamed %s to %s' % (os.path.join(dir_dir,dirname),os.path.join(dir_dir,new_dirname)))
                dir_list=[i.replace(dirname,new_dirname) if dirname in i else i for i in dir_list]
            if flag:
                now = os.path.join(dir_dir,new_dirname)
                print('Renamed %s to %s' % (dir_item,now))
        print()
        for root, dirs, files in os.walk(pack):    
            for file in files:
                flag = False
                was = os.path.join(root, file)
                title = os.path.splitext(file)[0]
                extension = os.path.splitext(file)[1]
                for trigger in triggers:
                    if trigger in title:
                        new_title = title.replace(trigger, '_')
                        new_file = new_title + extension
                        os.rename(os.path.join(root,file),os.path.join(root,new_file))
                        flag = True
                        # below is different from the loop for dirs
                        file = new_file
                        title = new_title
                if re.findall('__+', file):
                    new_file = re.sub('__+', '_', file)
                    os.rename(os.path.join(root,file),os.path.join(root,new_file))
                    flag = True
                if flag:
                    now = os.path.join(root,new_file)
                    print('Renamed %s to %s' % (was,now))
        print('---')
    print('\n\n***Rename package - replace spaces to _ and remove all special characters***')
    for pack in packs:
        flag = False
        packname = os.path.basename(pack)
        pack_dir = os.path.dirname(pack)
        for trigger in triggers[1:]:
            if trigger in packname:
                new_packname = packname.replace(trigger, '')
                os.rename(os.path.join(pack_dir,packname),os.path.join(pack_dir,new_packname))
                flag = True
                # print('Renamed %s to %s' % (os.path.join(pack_dir,packname),os.path.join(pack_dir,new_packname)))
                packname = new_packname
        if re.findall(' ', packname):
            new_packname = re.sub(' ', '_', packname)
            os.rename(os.path.join(pack_dir,packname),os.path.join(pack_dir,new_packname))
            flag = True
            # print('Renamed %s to %s' % (os.path.join(pack_dir,packname),os.path.join(pack_dir,new_packname)))
        if re.findall('__+', packname):
            new_packname = re.sub('__+', '_', packname)
            os.rename(os.path.join(pack_dir,packname),os.path.join(pack_dir,new_packname))
            flag = True
            # print('Renamed %s to %s' % (os.path.join(pack_dir,packname),os.path.join(pack_dir,new_packname)))
        if flag:
            now = os.path.join(pack_dir,new_packname)
            print('Renamed %s to %s' % (pack,now))

def move_to_root(packs):
    print('\n\n***Move subfiles and delete subfolders- move all files to the root of the packages and delete subfolders***')
    for pack in packs:
        print('Moving for %s' % pack)
        m = 0
        last_dir=''
        for root, dirs, files in os.walk(pack):
            for file in files:
                file_path = os.path.join(root,file)
                str_dir = root.replace(pack, '')
                str_dir = str_dir.replace('\\', '', 1)
                str_dir = str_dir.replace('/', '', 1)
                str_dir = str_dir.replace('\\', '_')
                str_dir = str_dir.replace('/', '_')
                if str_dir != '':
                    if str_dir == last_dir:
                        new_file_path = os.path.join(pack, str(m) + '_' + file)
                    else:
                        m = m + 1
                        new_file_path = os.path.join(pack, str(m) + '_' + file)
                        last_dir = str_dir
                    shutil.move(file_path, new_file_path)
                    print('Moved %s to %s' % (file_path, new_file_path))
        print('\nDeleting subfolders')
        for root, dirs, files in os.walk(pack):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                os.rmdir(dir_path)
                print('Deleted empty folder %s' % dir_path)
        print('---')


def main():
    root = sys.argv[1]
    dirs = os.listdir(root)
    print('Packages found in the input directory:')
    packs=[]
    for dir in dirs:
        pack_path = os.path.join(root,dir)
        print('\t' + pack_path)
        packs.append(pack_path)
    if packs==[]:
        print('No package was found in the directory.\nCheck the input directory and run the script again.\nScript ends.')
        sys.exit()
    answer = input('Are you sure you want to proceed?\nAnswer y/n\t->')
    if answer.lower() == 'y':
        print()
        list=[
            '1. Rename packages/folders/files - replace spaces and special characters',
            '2. Move subfiles and delete subfolders - move all files to the root of the packages and delete subfolders'
        ]
        print(*list, sep = '\n')
        func = input('Which feature do you need?\t-> ')  
        if func == '1':
            rename(packs)
        elif func == '2':
            move_to_root(packs)
    else:
        print('Check the input directory and run the script again.\nScript ends.')
        sys.exit()
    
if __name__ == '__main__':
    main()