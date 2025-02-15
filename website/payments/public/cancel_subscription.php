<?php
session_start();
require_once '../vendor/autoload.php';
require_once '../secrets.php'; // Ensure it includes DB credentials and Stripe key

// Ensure user is logged in
if (!isset($_SESSION["user_id"])) {
    die("Unauthorized access. Please log in.");
}

// Connect to the database
$conn = new mysqli($servername, $username, $password_db, $dbname);
if ($conn->connect_error) {
    die("Database connection failed: " . $conn->connect_error);
}

// Get user ID from session
$user_id = $_SESSION["user_id"];

// Retrieve user's email and Stripe subscription ID
$stmt = $conn->prepare("SELECT email, stripe_subscription_id FROM users WHERE id = ?");
$stmt->bind_param("i", $user_id);
$stmt->execute();
$stmt->store_result();

if ($stmt->num_rows === 0) {
    die("User not found.");
}

$stmt->bind_result($email, $stripe_subscription_id);
$stmt->fetch();
$stmt->close();

// Initialize Stripe API
\Stripe\Stripe::setApiKey($stripeSecretKey);

// Cancel the subscription in Stripe
try {
    $subscription = \Stripe\Subscription::retrieve($stripe_subscription_id);
    $subscription->cancel();
} catch (Exception $e) {
    die("Error canceling subscription: " . $e->getMessage());
}

// Update the database to reflect the canceled status
$update_stmt = $conn->prepare("UPDATE users SET subscription_status = 'unpaid' WHERE id = ?");
$update_stmt->bind_param("i", $user_id);
$update_stmt->execute();
$update_stmt->close();

// Close the database connection
$conn->close();

// Redirect the user with a success message
header("Location: features/index.php?message=Subscription Canceled");
exit;
?>
