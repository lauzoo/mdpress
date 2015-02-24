<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="utf-8" />
    <title></title>
    <link rel="stylesheet" href="css/style.css" />
    <link rel="stylesheet" href="css/editormd.css" />
</head>

<body>
    <div id="content">
        <div class="markdown-body editormd-preview-container">
            <h2 id="all-contents">
                <a href="#All Contents" name="All Contents" class="anchor" />
                <span class="header-link">
                </span>
                All Contents
            </h2>
            <ul>
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

                $conn = new mysqli($serverName, $username, $password, $dbName);
                if ($conn->connect_error)
                {
                    die ("Connection Faild" . $conn->connect_error);
                }

                $sql = "SELECT * FROM posts ORDER BY id";
                $result = $conn->query($sql);

                if ($result->num_rows > 0)
                {
                    while ($row = $result->fetch_assoc())
                    {
                        ?>
                        <li>
                            <a href="query.php?pid=<?php echo $row["id"] ?>" title="<?php echo $row["name"] ?>">
                                <?php echo $row["name"] ?>
                            </a>
                        </li>
                        <?php
                    }
                }
                else
                {
                    ?>
                    <li>
                        <a href="#">
                            <?php echo "No Records"; ?>
                        </a>
                    </li>
                <?php
                }

                $conn->close();
                ?>
            </ul>
        </div>
    </div>
</body>