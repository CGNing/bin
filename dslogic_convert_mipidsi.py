#!/usr/bin/env python3
#-*- coding:UTF-8 -*-

#dslogic的I2C解析结果的csv文件,将一列数据的格式转换成一行一个数据包的格式

import sys
import os

try:
    import csv
    import openpyxl
except ImportError:
    print ("找不到依赖库");
    print (ImportError);

if len (sys.argv) > 1:
    str_file_path = sys.argv[1]
else:
    print ("无效的传入参数");
    exit(-1);

if os.path.isfile(str_file_path):
    str_file_dir = os.path.dirname(str_file_path);
    str_file_base = os.path.basename(str_file_path);
    str_file_base = os.path.splitext(str_file_base)[0];
    if str_file_dir == "":
        str_fileout_path = os.path.join(".", str_file_base + ".xlsx"); # 兼容linux和windows路径
    else:
        str_fileout_path = os.path.join(str_file_dir, str_file_base + ".xlsx");

    with open (str_file_path, "r") as file_sheet:
        csv_sheet_reader = csv.reader(file_sheet, delimiter=',');

        # 将csv文件经过预处理去掉第一行和第一列并转换成列表
        list_csv_data = [];
        for index, item in enumerate(csv_sheet_reader):
            if (index == 0):
                continue;
            list_csv_data.append(item[2]);

        # 删掉无意义的符号
        list_data = [];
        for index, item in enumerate(list_csv_data):
            data_temp = item;

            if (data_temp == "Escape mode entry"):
                data_temp = "ESC";
            elif (data_temp == "Bi-directional Data Lane Turnaround"):
                data_temp = "BTA";

            # data_temp = "{:02X}".format(data_temp); # 修改数字格式

            list_data.append(data_temp);

        # 将一维列表转换成二维列表
        list_sheet = [];
        bool_newline = True;
        int_sheet_row = 0;
        for item in list_data:
            if (item == "Stop"):
                int_sheet_row = int_sheet_row + 1;
                bool_newline = True;
            elif (bool_newline == True):
                bool_newline = False;
                list_sheet.append([item]);
            else:
                list_sheet[int_sheet_row].extend([item]);




    # 保存为xlsx文件
    workbook = openpyxl.Workbook()
    sheet = workbook.active #Excel页签标识

    for list_data_row in list_sheet:
        sheet.append(list_data_row);
    workbook.save(str_fileout_path) #保存为xlsx文件，名字可以随意写

    '''
    # 保存为csv文件
    with open (str_fileout_path, "w", newline="") as file_result: # newline="" 是为了之后csv.writerow没有多余的空行
        file_result.truncate(); #清空文件
        csv_sheet_writer = csv.writer(file_result, delimiter=',');

        for item in list_sheet:
            csv_sheet_writer.writerow(item);
    '''

elif os.path.isdir(str_file_path):
    print ("传入参数的路径无效")

else:
    print ("传入参数未知错误")

exit();
