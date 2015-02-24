<?php
include 'lib/Parser.php';
include 'lib/uuid.php';

use HtmlParser\Parser;

$name = $_REQUEST["name"];
$content = mysql_real_escape_string($_REQUEST["content"]);

$serverName = "localhost";
$username = "root";
$password = "";
$dbName = "test";
$conn = new mysqli($serverName, $username, $password, $dbName);

if ($conn->connect_error)
{
    die ("Connection Failed: " . $conn->connect_error);
}
echo "Connection Success<br/>";



//现在支持直接输入html字符串了
$html_dom = new Parser($content);
//$html_dom->parseStr($html);
$div = $html_dom->find('h2',0);
$name = mysql_real_escape_string($div->getPlainText());
$uuidCreater = new UUIDCreater();
$sql = "INSERT INTO posts(id, user_id, name, content) VALUES('" . $uuidCreater->create_uuid()
    . "','C2E7E3834535067D01DA68F5914122B8863AA2D0BC7A6D9D6C34052A4FD3BB84','"
    . $name . "', '" . $content . "')";

if ($conn->query($sql) === true)
{
    echo "Success Insert";
}
else
{
    echo "Insert Faild";
}

$conn->close();
?>