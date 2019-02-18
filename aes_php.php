<?php

/**
 * Aes的ECB模式加解密库
 */
class Aes
{
    //密钥须是16位
    private $key;

    public function __construct($key)
    {
        $this->key = $key;
    }

    /**
     * 加密方法
     * @param string $str 字符串
     * @return string
     */
    public function encrypt($str)
    {
        return base64_encode(openssl_encrypt($str, "AES-128-ECB", $this->key, OPENSSL_RAW_DATA));
    }

    /**
     * 解密方法
     * @param string $str 字符串
     * @return string
     */
    public function decrypt($str)
    {
        return openssl_decrypt(base64_decode($str), "AES-128-ECB", $this->key, OPENSSL_RAW_DATA);
    }
}

/**
 *  测试案例
 */
$key = '123456789abcdef';  //16位密钥
$aes = new Aes($key);
$string = 'Hello World';  //需加密字符串
$encrypt = $aes->encrypt($string);
$decrypt = $aes->decrypt($encrypt);
echo '需加密字符串：' . $string . "\n";
echo '加密结果：' . $encrypt . "\n";
echo '解密结果：' . $decrypt . "\n";
