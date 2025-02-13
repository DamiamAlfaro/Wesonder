<?php
$host = "localhost";
$username = "u978864605_wesonder";
$password = "Elchapillo34?nmddam";
$dbname = "u978864605_wesonder";

// Create connection
$conn = new mysqli($host, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Set charset to utf8mb4 (better for special characters)
$conn->set_charset("utf8mb4");
?>
