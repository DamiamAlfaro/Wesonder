<?php
session_start();
require_once $_SERVER['DOCUMENT_ROOT'] . '/payments/secrets.php';

// Connect to the database
$conn = new mysqli($servername, $username, $password_db, $dbname);
if ($conn->connect_error) {
    die("Database connection failed: " . $conn->connect_error);
}

// Ensure user is logged in
if (!isset($_SESSION["user_id"])) {
    header("Location: ../");
    exit;
}

// Verify user has an active subscription
$user_id = $_SESSION["user_id"];
$stmt = $conn->prepare("SELECT subscription_status FROM users WHERE id = ?");
$stmt->bind_param("i", $user_id);
$stmt->execute();
$stmt->bind_result($subscription_status);
$stmt->fetch();
$stmt->close();
$conn->close();

if ($subscription_status !== 'paid') {
    header("Location: ../payments/public/signup.php");
    exit;
}
?>
