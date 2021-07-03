#!/usr/bin/env python3
#-*- coding:UTF-8 -*-
import sys
import os
import shutil

if len (sys.argv) > 1:
    str_file_path = sys.argv[1]
else:
    print ("无效的传入参数");
    exit(-1);

def do_unlock(fun_str_file_path):
    fun_str_filetmp_path = fun_str_file_path+".tmp";
    shutil.copyfile(fun_str_file_path, fun_str_filetmp_path);
    os.remove(fun_str_file_path);
    # os.system("ren " + fun_str_filetmp_path + " " +  fun_str_file_path);
    # os.rename(fun_str_filetmp_path, fun_str_file_path);
    shutil.copyfile(fun_str_filetmp_path, fun_str_file_path);
    os.remove(fun_str_filetmp_path);

if os.path.isfile(str_file_path):
    do_unlock(str_file_path);
elif os.path.isdir(str_file_path):
    print ("传入参数的路径无效")

else:
    print ("传入参数未知错误")

exit();
