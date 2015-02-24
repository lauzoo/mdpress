<?php
/**
 * Created by PhpStorm.
 * User: vasquez
 * Date: 2/20/15
 * Time: 11:59 PM
 */

$serverName = "localhost";
$username = "root";
$password = "";
$dbName = "test";


$id = mysql_real_escape_string($_GET["pid"]);
if (empty($id))
{
    echo "Error. Empty Id";
    return ;
}

$conn = new mysqli($serverName, $username, $password, $dbName);
if ($conn->connect_error)
{
    die ("Connection Faild" . $conn->connect_error);
}

$sql = "SELECT content FROM posts where id = '" . $id . "'";
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
