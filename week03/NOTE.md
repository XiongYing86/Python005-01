学习笔记
1、	读取my.ini配置文件报错:
UnicodeDecodeError: 'gbk' codec can't decode byte 0x95 in position 97: illegal multibyte sequence

parse.read(filename,encoding='UTF-8') # ecoding=’UTF-8’
