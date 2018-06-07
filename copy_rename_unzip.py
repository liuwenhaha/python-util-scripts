# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 10:10:24 2018

@author: Raluca Sandu
"""

import os
import sys 
import shutil
import zipfile
from splitAllPaths import splitall as split_paths
# TODO 6. remove the German umlauts and the French umlauts from the names

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def copy_rename_unzip(src_dir, dst_dir):
    # Copy and rename all patient folders from src_dir to dest_dir'''
    # copy to destination folder
    copytree(src_dir,dst_dir)
    # rename
    for dirs in os.listdir(dst_dir):
        if not os.path.isdir(os.path.join(dst_dir, dirs)):
            continue
        else:
            if "Pat" in dirs: # rename folder
                os.rename(os.path.join(dst_dir,dirs),
                          os.path.join(dst_dir, dirs[dirs.find('Pat'):]))
    # Move Study to Root folder and Unzip XML Recordings
    for path, dirs, files in os.walk(src_dir):
        index_ir = [i for i, s in enumerate(dirs) if 'IR Data' in s]
        index_xml = [i for i, s in enumerate(dirs) if 'XML' in s]
        if index_ir:
            ir_data_dir = dirs[index_ir[0]]
            src = os.path.join(path,ir_data_dir)
            all_folders = split_paths(src)
            index = [i for i, s in enumerate(all_folders) if 'Pat' in s]
            dst = os.path.join(src_dir, all_folders[index[0]])
            copytree(src,dst)
        if index_xml:
            xml_dir = dirs[index_xml[0]]
            xml_dir = os.path.join(path, xml_dir)
            for file in os.listdir(xml_dir):
                if file.endswith(".zip"):
                    filename, file_extension = os.path.splitext(file)
                    # unzip file xml recordings
                    zip_filepath = os.path.join(xml_dir,file)
                    with zipfile.ZipFile(zip_filepath,"r") as zip_ref:
                        zip_ref.extractall(os.path.join(xml_dir,filename))
                        zip_ref.close()
                        
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('To few arguments, please specify a source directory and destination directory')
        exit()
    else:
        src_dir = os.path.normpath(sys.argv[1])
        print('Source Directory:', src_dir)
        dst_dir = os.path.normpath(sys.argv[2])
        print('Destination Directory:', dst_dir)
        copy_rename_unzip(src_dir, dst_dir)
#   src_dir = r"C:\develop\data\PATS" # source directory from where to copy the folders/files
#   dst_dir = r"C:\develop\data\TEST_DIR" # destination directory to where copy folders/files