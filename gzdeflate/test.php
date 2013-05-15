<?
file_put_contents("test", gzcompress(file_get_contents('php_deflate')));
include("test");