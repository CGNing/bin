#!/usr/bin/env python3
#-*- coding:UTF-8 -*-
import sys
import os
import shutil

if (len (sys.argv) == 2):
    str_input_path = sys.argv[1];
elif (len (sys.argv) > 2):
    str_input_path = sys.argv[1];
    str_input_step = sys.argv[2];
else:
    print ("无效的传入参数");
    exit(-1);

def do_unlock(fun_str_file_path, step):
    if (step == "1"):
        fun_str_filetmp_path = fun_str_file_path+".tmp";
        shutil.copyfile(fun_str_file_path, fun_str_filetmp_path);
        os.remove(fun_str_file_path);
    elif (step == "2"):
        fun_str_fileoriginal_path = os.path.splitext(fun_str_file_path)[0];
        fun_str_fileoriginal_ext = os.path.splitext(fun_str_file_path)[1];
        if (fun_str_fileoriginal_ext == ".tmp"):
            # os.system("ren " + fun_str_filetmp_path + " " +  fun_str_file_path);
            # os.rename(fun_str_filetmp_path, fun_str_file_path);
            shutil.copyfile(fun_str_file_path, fun_str_fileoriginal_path);
            os.remove(fun_str_file_path);

# start
if os.path.isfile(str_input_path):
    if (len (sys.argv) == 1):
        do_unlock(str_input_path, 1);
        do_unlock(str_input_path, 2);
    elif (len (sys.argv) > 2):
        do_unlock(str_input_path, str_input_step);
elif os.path.isdir(str_input_path):
    for root, dirs, files in os.walk(str_input_path):
        for f in files:
            str_file_path = os.path.join(root, f);
            if (len (sys.argv) == 1):
                do_unlock(str_file_path, 1);
                do_unlock(str_file_path, 2);
            elif (len (sys.argv) > 2):
                do_unlock(str_file_path, str_input_step);

else:
    print ("传入参数未知错误")

exit();
