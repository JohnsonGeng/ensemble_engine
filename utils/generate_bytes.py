# -*- coding: utf=8 -*-
# @Time: 2023/12/17 
# @Author: Johnson Geng
# @FIle: generate_bytes.py 
# @Description: 生成Bytes文件


import os
import pefile
import binascii

def bytes_generator(file_path):

    byte_data = []
    line = []
    line_count = 0

    # 获得文件大小
    binary_size = os.path.getsize(file_path)

    try:
        # 如果成功打开文件并且没有抛出异常，则是PE文件
        pe = pefile.PE(file_path)
    except:
        # 如果抛出异常，则跳过
        print('不是PE文件！')
        os.remove(file_path)
        return False


    # 获取第一个节的物理偏移地址
    if hasattr(pe, 'sections') and len(pe.sections) > 0:
        first_section = pe.sections[0]
        physical_offset = first_section.PointerToRawData
    else:
        print('PE文件解析出错！')
        os.remove(file_path)
        return False


    # 以二进制形式读取可执行文件，每次读取一个字节
    with open(file_path, 'rb') as in_file:
        for i in range(binary_size):

            # Microsoft Malware Challenge数据没有头部，这里也略去头部
            if i < physical_offset:
                in_file.read(1)
                continue

            _byte = in_file.read(1)
            # 转换成16进制
            hex_string = str.upper(binascii.b2a_hex(_byte).decode('ascii'))
            line.append(hex_string)

            if (i + 1) % 16 == 0:

                # 获取当前行的物理地址
                physical_offset_str = fill_physical_address(hex(physical_offset+line_count*16))

                # 在每一行前面写上地址
                byte_data.append("{} {}".format(physical_offset_str, " ".join(line)))
                line = []

                line_count += 1

        # 剩下的字节如果不满一行也要写入
        if len(line) != 0:
            physical_offset_str = fill_physical_address(hex(physical_offset + line_count * 16))
            byte_data.append("{} {}".format(physical_offset_str, " ".join(line)))

    pe.close()

    return byte_data

# 将一个十六进制偏移地址转换成八位的字符串形式，如0x400 --> 00000400
def fill_physical_address(hex_physical_address):

    physical_address = str(hex_physical_address)[2:]

    return '0'*(8-len(physical_address)) + physical_address