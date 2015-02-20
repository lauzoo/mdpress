<?php
/**
 * Created by PhpStorm.
 * User: root
 * Date: 2/20/15
 * Time: 11:59 PM
 */

$serverName = "localhost";
$username = "root";
$password = "root";
$dbName = "test";

$conn = new mysqli($serverName, $username, $password, $dbName);

if ($conn->connect_error)
{
    die ("Connection Faild" . $conn->connect_error);
}

$sql = "SELECT * FROM posts LIMIT 1";
$result = $conn->query($sql);

if ($result->num_rows > 0)
{
    while ($row = $result->fetch_assoc())
    {
        echo $row["content"];
    }
}
else
{
    echo "No Records";
}

$conn->close();
?>
