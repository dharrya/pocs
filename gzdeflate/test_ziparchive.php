<?php
$zip = new ZipArchive();
$filename = "ziparchive_test.php.zip";

if ($zip->open($filename, ZIPARCHIVE::CREATE)!==TRUE) {
    exit("Невозможно открыть <$filename>\n");
}
$zip->addFile("./php_deflate");
echo "numfiles: " . $zip->numFiles . "\n";
echo "status:" . $zip->status . "\n";
$zip->close();