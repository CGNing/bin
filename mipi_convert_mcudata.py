#!/usr/bin/env python3
#-*- coding:UTF-8 -*-

import sys
import os
import re

CRC16_POLY = 0x8408;

def calc_crc16(func_list_int):
    crc = 0xFFFF;

    for item in func_list_int:
        crc ^= item;
        for j in range(0, 8):
            if ((crc & 0x0001) != 0):
                crc = (crc >> 1) ^ CRC16_POLY;
            else:
                crc >>= 1;

    func_list_int.extend([crc&0xFF]);
    func_list_int.extend([(crc&0xFF00)>>8]);
    # print("0x{:04X}".format(crc));

def calc_ecc(func_list_int):
    D=[]
    for i in range(0, 3):
        for j in range(0, 8):
            D.append((func_list_int[i] & (1 << j)) >> j);

    hex_data_ecc = 0;                   #Bit7
    hex_data_ecc = hex_data_ecc << 1;   #Bit6
    hex_data_ecc = (hex_data_ecc << 1) | (D[10] ^D[11] ^D[12] ^D[13] ^D[14] ^D[15] ^D[16] ^D[17] ^D[18] ^D[19] ^D[21] ^D[22] ^D[23]);           #Bit5
    hex_data_ecc = (hex_data_ecc << 1) | (D[4]  ^D[5]  ^D[6]  ^D[7]  ^D[8]  ^D[9]  ^D[16] ^D[17] ^D[18] ^D[19] ^D[20] ^D[22] ^D[23]);           #Bit4
    hex_data_ecc = (hex_data_ecc << 1) | (D[1]  ^D[2]  ^D[3]  ^D[7]  ^D[8]  ^D[9]  ^D[13] ^D[14] ^D[15] ^D[19] ^D[20] ^D[21] ^D[23]);           #Bit3
    hex_data_ecc = (hex_data_ecc << 1) | (D[0]  ^D[2]  ^D[3]  ^D[5]  ^D[6]  ^D[9]  ^D[11] ^D[12] ^D[15] ^D[18] ^D[20] ^D[21] ^D[22]);           #Bit2
    hex_data_ecc = (hex_data_ecc << 1) | (D[0]  ^D[1]  ^D[3]  ^D[4]  ^D[6]  ^D[8]  ^D[10] ^D[12] ^D[14] ^D[17] ^D[20] ^D[21] ^D[22] ^D[23]);    #Bit1
    hex_data_ecc = (hex_data_ecc << 1) | (D[0]  ^D[1]  ^D[2]  ^D[4]  ^D[5]  ^D[7]  ^D[10] ^D[11] ^D[13] ^D[16] ^D[20] ^D[21] ^D[22] ^D[23]);    #Bit0

    func_list_int.extend([hex_data_ecc]);

def mipi_dsi_package(func_list_int):
    package_type = func_list_int[0];
    package_data = func_list_int[1:];
    package_len = len(package_data);
    if (package_len > 2):
        package_type |= 0x01;

    if (package_type == 0x00):
        if (package_len == 1):
            package_head = [0x05] + package_data + [0x00];
        elif (package_len == 2):
            package_head = [0x15] + package_data;
        calc_ecc(package_head);
        package_out = package_head;

    elif (package_type == 0x01):
        package_head = [0x39] + [package_len & 0xFF] + [(package_len & 0xFF00) >> 8];
        calc_ecc(package_head);
        calc_crc16(package_data);
        package_out = package_head + package_data;

    elif (package_type == 0x10):
        if (package_len == 0):
            package_head = [0x03, 0x00, 0x00];
        elif (package_len == 1):
            package_head = [0x13] + package_data + [0x00];
        elif(package_len == 2):
            package_head = [0x23] + package_data;
        calc_ecc(package_head);
        package_out = package_head;

    elif (package_type == 0x11):
        package_head = [0x29] + [package_len & 0xFF] + [(package_len & 0xFF00) >> 8];
        calc_ecc(package_head);
        calc_crc16(package_data);
        package_out = package_head + package_data;

    return package_out;

# 打开文件
if len (sys.argv) > 1:
    str_file_path = sys.argv[1]
else:
    print ("无效的传入参数\n");
    exit(-1);

if os.path.isfile(str_file_path):
    with open (str_file_path, "r", encoding='UTF-8') as file_data:
        str_original_data = file_data.read();
else:
    print ("传入路径参数识别错误\n");
    exit(-1);

# 提取函数内容
match_func_contect = re.search(r"void\s*main\(\)\s*\{([\s\S]*?)\}", str_original_data, flags=0);
if (match_func_contect):
    str_initcode_type = "GY";
    print ("识别到国宇格式的初始化代码\n")

if (match_func_contect == None):
    match_func_contect = re.search(r"void\s*PwrOnSequence\(\)\s*\{([\s\S]*?)\}", str_original_data, flags=0);
    if (match_func_contect):
        str_initcode_type = "PX";
        print ("识别到PX格式的初始化代码\n")

if (match_func_contect == None):
    print ("未识别到初始化函数\n");
    exit(-1);

# 删除注释
str_parameter = re.sub(r"//(.*?)\n","", match_func_contect.group(1));
str_parameter = re.sub(r"/\*(.*?)\*/","",str_parameter);
str_parameter = re.sub(r"[ \n\t]","",str_parameter);

# 提取发送MIPI的函数
if (str_parameter):
    if (str_initcode_type == "GY"):
        str_parameter = re.sub(r"DCS_Short_Write_[N1]P\(","SSD_SEND(0x00,",str_parameter);
        str_parameter = re.sub(r"DCS_Long_Write_[N1-9]P\(","SSD_SEND(0x01,",str_parameter);
        str_parameter = re.sub(r"Generic_Short_Write_[N1]P\(","SSD_SEND(0x10,",str_parameter);
        str_parameter = re.sub(r"Generic_Long_Write_[N1-9]P\(","SSD_SEND(0x11,",str_parameter);
        list_mipiwrite = re.findall(r"SSD_SEND\((.*?)\)", str_parameter);
    elif(str_initcode_type == "PX"):
        str_parameter = re.sub(r"DCS","0x00",str_parameter);
        str_parameter = re.sub(r"GEN","0x10",str_parameter);
        list_mipiwrite = re.findall(r"MipiWrite\((.*?)\)", str_parameter);
else:
    print ("未找到有效MIPI发送函数");

# 转换为数字list
list_hex_mipiwite = [];
if (list_mipiwrite):
    for index, item in enumerate(list_mipiwrite):
        list_str_temp = re.split(r",[\s]*",item);
        list_hex_mipiwite.append([]);
        for cell in list_str_temp:
            list_hex_mipiwite[index].extend([int(cell,16)]);

# 打包MIPI DSI数据
list_mcu_mipiwite = [];
for item in list_hex_mipiwite:
    list_mipisend = mipi_dsi_package(item);
    list_mcu_mipiwite.append([len(list_mipisend)] + list_mipisend);

# print输出0x格式
for i, package in enumerate(list_mcu_mipiwite):
    for j, item in enumerate(package):
        if (j != (len(package)-1)):
            print ("0x{:02X}".format(item), end=", "),
        else:
            print ("0x{:02X}".format(item), end=""),

    if (i != (len(list_mcu_mipiwite)-1)):
        print (","),

exit();
