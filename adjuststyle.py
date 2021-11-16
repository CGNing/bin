#!/usr/bin/env python3
#-*- coding:UTF-8 -*-

#将文件中的的TAB制表符全部转换成4个空格对其

import sys
import os
import re

if len (sys.argv) > 1:
    str_input_path = sys.argv[1]
else:
    print ("无效的传入参数");
    exit(-1);

def do_adjust (fun_str_file_path):
    with open(fun_str_file_path, "r+") as file:
        str_file = file.read();
        str_replace = re.sub("\n\n\n+", "\n\n", str_file);
        file.seek(0);   # 归零指针
        file.truncate();   # 清空文件
        # print (str_file.expandtabs(4));
        file.write (str_replace.expandtabs(4));
        file.close();

# start
if os.path.isfile(str_input_path):
    do_adjust(str_input_path);

elif os.path.isdir(str_input_path):
    for root, dirs, files in os.walk(str_input_path):
        for f in files:
            str_file_path = os.path.join(root, f);
            do_adjust(str_file_path);

else:
    print ("传入参数未知错误");

exit();
