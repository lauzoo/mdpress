<?php
include 'lib/Parser.php';
use HtmlParser\Parser;

$name = $_REQUEST["name"];
$content = $_REQUEST["content"];

echo $content;


$serverName = "localhost";
$username = "root";
$password = "root";
$dbName = "test";
$conn = new mysqli($serverName, $username, $password, $dbName);

if ($conn->connect_error)
{
    die ("Connection Failed: " . $conn->connect_error);
}
echo "Connection Success<br/>";



//现在支持直接输入html字符串了
$html_dom = new Parser($content);
echo "1";
//$html_dom->parseStr($html);
$div = $html_dom->find('h2',0);
echo "2";
$name = $div->getPlainText();
echo "3" . "<br/>";
echo $name . "<br/>";

$sql = "INSERT INTO posts(name, content) VALUES('" . $name . "', '" . $content . "')";
echo $sql . "<br/>";

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