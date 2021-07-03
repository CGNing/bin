#!/usr/bin/env python3
#-*- coding:UTF-8 -*-

#将文件中的的TAB制表符全部转换成4个空格对其

import sys
import os

if len (sys.argv) > 1:
    str_file_path = sys.argv[1]
else:
    print ("无效的传入参数");
    exit(-1);

def do_adjust (str_file_name):
    with open(str_file_path, "r+") as file:
        str_file = file.read();
        file.seek(0);
        file.write (str_file.expandtabs(4));
        file.close();

if os.path.isfile(str_file_path):
    do_adjust(str_file_path);

elif os.path.isdir(str_file_path):
    print ("TODO");

else:
    print ("传入参数未知错误");

exit();
