<?php

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