#!/usr/bin/python
# -*- coding: UTF-8 -*-

#verilog中module的快速例化

import re;
try:
    import pyperclip;
    is_pyperclip_exist = 1;
except ImportError:
    is_pyperclip_exist = 0;
    print ("pyperclip模块不存在")
    print (ImportError)

str_temp = "";

# input
str_input = "";

str_input = raw_input("请输入模块声明：");

while str_input[-1] != ';':
    str_temp = raw_input();
    str_input = str_input + "\n" + str_temp;

# module name
list_temp = re.findall(r"(?<=module)(.*?)[#(]", str_input);
if (list_temp):
    str_module_name = list_temp[0];
    str_module_name = str_module_name.strip(" ");
else:
    print ("Error: can not find module name");
    exit(-1);

# interface string
list_temp = re.findall(r"[#]\([\s\n]([\s\S]*?)[\s\n]\)", str_input);
if (list_temp):
    str_parameter = list_temp[0];
else:
    str_parameter = "";

list_temp = re.findall(r"[^#]\([\s\n]([\s\S]*?)[\s\n]\)", str_input);
if (list_temp):
    str_interface = list_temp[0];
else:
    str_interface = "";

# interface list
list_parameter = [];
list_parameter_gap = [];
list_parameter_value = [];
list_interface = [];
list_interface_gap = [];
list_interface_width = [];

if (str_parameter):
    # 删除注释
    str_parameter = re.sub(r"//(.*?)\n","",str_parameter);
    str_parameter = re.sub(r"/\*(.*?)\*/","",str_parameter);
    list_parameter = str_parameter.split(",");

# parameter list name
for index,value in enumerate(list_parameter):
    # '\n' char
    # parameter之间的换行
    list_temp = re.findall(r"\n([\n]*).*", value);
    if (list_temp):
        list_parameter_gap.append(list_temp[0]);
    else:
        list_parameter_gap.append("");

    list_temp = re.findall(r"parameter[\s\S\[\]]*?=[\s]*(.*?)[\s]*$", value);

    if (list_temp):
        list_parameter_value.append(list_temp[0]);
    else:
        list_parameter_value.append("");

    list_parameter[index] = re.findall(r"parameter[\s\S\[\]](\S*?)[\s]", value)[0];

if (str_interface):
    # 删除注释
    str_interface = re.sub(r"//(.*?)\n","",str_interface);
    str_interface = re.sub(r"/\*(.*?)\*/","",str_interface);
    list_interface = str_interface.split(",");

# interface list name
for index,value in enumerate(list_interface):
    # '\n' char
    # interface之间的换行
    list_temp = re.findall(r"\n([\n]*).*", value);
    if (list_temp):
        list_interface_gap.append(list_temp[0]);
    else:
        list_interface_gap.append("");

    #"[]" wire width
    list_temp = re.findall(r"(\[.*?\])", value);
    if (list_temp):
        list_interface_width.append(list_temp[0]);
    else:
        list_interface_width.append("");

    list_interface[index] = re.findall(r"[\s](\S*?)[\s]*$", value)[0];

# 替换wire中存在的parameter
for index_p,value_p in enumerate(list_parameter):
    for index_i,value_i in enumerate(list_interface_width):
        list_interface_width[index_i] = re.sub(r"\b"+value_p+r"\b", list_parameter_value[index_p], value_i);

# print
str_output = "";

print ("实例化结果：");
# wire 声明
for index,value in enumerate(list_interface):
    if (len(list_interface_width[index]) == 0):
        str_temp = "wire" + "\t\t\t" + value + ";\n";
    else:
        str_temp = "wire" + "\t" + list_interface_width[index] + "\t" + value + ";\n";
    str_output = str_output + str_temp;

# parameter 声明
if (str_parameter):
    int_parameter_maxlen = 0;

    for value in list_parameter:
        if (len(value) > int_parameter_maxlen):
            int_parameter_maxlen = len(value);

    str_output = str_output + "\n" + str_module_name + " #(\n" ;
    for index,value in enumerate(list_parameter):
        str_temp = list_parameter_gap[index] + "\t." + value.ljust(int_parameter_maxlen) + "\t(" + list_parameter_value[index] + "),\n";
        str_output = str_output + str_temp;
    str_output = str_output[:-2] + "\n)" + str_module_name + "(\n";
else:
    str_output = str_output + "\n" + str_module_name + " " + str_module_name + " (\n";

# interface 声明
int_interface_maxlen = 0;

for value in list_interface:
    if (len(value) > int_interface_maxlen):
        int_interface_maxlen = len(value);

for index,value in enumerate(list_interface):
    str_temp = list_interface_gap[index] + "\t." + value.ljust(int_interface_maxlen) + "\t(" + value + "),\n";
    str_output = str_output + str_temp;

str_output = str_output[:-2] + "\n);";
str_output = str_output.expandtabs(4);

if (is_pyperclip_exist == 1):
    pyperclip.copy(str_output);

print (str_output);
