# -*- coding: utf-8 -*-
'''
有个目录，里面是你自己写过的程序，统计一下你写过多少行代码。包括空行和注释，但是要分别列出来。[不考虑多行注释的情况]

Author: Insomnia
Version: 0.0.1
Date: 2017-11-21
Language: python3.6.2
Editor: Sublime Text 3
'''

import os

def get_files(path, postfix='py'):
    '''
    获取指定目录下的某种后缀名的所有文件

    Args:
        path: 指定目录路径
        postfix: 指定获取文件的后缀名
    '''
    files = os.listdir(path)
    files_path = []
    for fi in files:
        fi_path = os.path.join(path, fi)
        if os.path.isfile(fi_path):
            if fi.split('.')[-1] == postfix:
                files_path.append(fi_path)
        elif os.path.isdir(fi_path):
            files_path += get_files(fi_path)
    return files_path

def count(files):
    '''
    计算代码，空行，注释

    Args:
        fils: 需要计算的所有文件路径
    '''
    line_code, blank, comments = 0, 0, 0
    for filename in files:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line == '':
                    blank += 1
                elif line[0] == '#':
                    comments += 1
                else:
                    line_code += 1
    return (line_code, blank, comments)

def main():
    files = get_files('/usr/src/myapp/python_practice_everyday/')
    print(files)

    lines = count(files)
    print('Line_code: %d, blank_line: %d, comments_line: %d' % (lines[0], lines[1], lines[2]))

if __name__ == '__main__':
    main()