# -*- coding: utf-8 -*-
'''
Aes算法案例

Author: Michael
Date: 2019-02-18
Language: 3.7.2
'''

import base64
from Crypto.Cipher import AES


class Aes(object):
    '''
    Aes的ECB模式加解密库

    Attribute:
        key: 密钥
    '''

    def __init__(self, key):
        self.key = key

    def add_to_16(self, value):
        '''
        value不是16的倍数那就补足为16的倍数

        Returns:
            返回bytes
        '''
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)

    def encrypt(self, text):
        '''
        加密方法

        Returns:
            返回加密字符串
        '''
        key = self.key
        # 初始化加密器
        aes = AES.new(self.add_to_16(key), AES.MODE_ECB)
        # 先进行aes加密
        encrypt_aes = aes.encrypt(self.add_to_16(text))
        # 用base64转成字符串形式
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
        return encrypted_text

    def decrypt(self, text):
        '''
        解密方法

        Returns:
            返回解密后的字符串
        '''
        key = self.key
        # 初始化加密器
        aes = AES.new(self.add_to_16(key), AES.MODE_ECB)
        # 优先逆向解密base64成bytes
        base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
        # 执行解密密并转码返回str
        decrypted_text = str(
            aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')
        return decrypted_text


if __name__ == '__main__':
    key = '123456789abcdef'  # 16位密钥
    aes = Aes(key)
    string = 'Hello World'  # 需加密字符串
    encrypt = aes.encrypt(string)
    decrypt = aes.decrypt(encrypt)
    print('加密字符串：%s, 加密结果：%s, 解密结果：%s' % (string, encrypt, decrypt))
