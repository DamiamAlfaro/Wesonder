<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
session_start();
require_once 'payments/secrets.php'; // Ensure this file exists

// Connect to the database
$conn = new mysqli($servername, $username, $password_db, $dbname);
if ($conn->connect_error) {
    die("Database connection failed: " . $conn->connect_error);
}

// Check if form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = trim($_POST["email"]);
    $password = $_POST["password"];

    // Validate email format
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        echo '<div style="background-color: #ffdddd; color: #d8000c; padding: 15px; border: 1px solid #d8000c; text-align: center; font-size: 16px; margin-top: 20px; border-radius: 5px;">
                ⚠️ Invalid email format.<br><br>
                <button onclick="history.back()" style="background-color: #d8000c; color: white; padding: 10px 15px; border: none; border-radius: 5px; cursor: pointer;">🔙 Go Back</button>
              </div>';
        exit;
    }

    // Retrieve user from database
    $stmt = $conn->prepare("SELECT id, name, last_name, password_hash, stripe_subscription_id, subscription_status FROM users WHERE email = ?");
    
    if (!$stmt) {
        die("Prepare statement failed: " . $conn->error);
    }

    $stmt->bind_param("s", $email);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows > 0) {
        $stmt->bind_result($user_id, $name, $last_name, $password_hash, $stripe_subscription_id, $subscription_status);
        $stmt->fetch();
        $stmt->close();

        // Verify password
        if (password_verify($password, $password_hash)) {
            if ($subscription_status === 'paid') {
                // Store session data
                $_SESSION["user_id"] = $user_id;
                $_SESSION["email"] = $email;
                $_SESSION["name"] = $name;
                $_SESSION["last_name"] = $last_name;
                $_SESSION["subscription_status"] = $subscription_status;

                header("Location: features/");
                exit;
            } else {
                echo '<div style="background-color: #ffdddd; color: #d8000c; padding: 15px; border: 1px solid #d8000c; text-align: center; font-size: 16px; margin-top: 20px; border-radius: 5px;">
                        🚫 Your subscription is not active. Please renew.<br><br>
                        <button onclick="history.back()" style="background-color: #d8000c; color: white; padding: 10px 15px; border: none; border-radius: 5px; cursor: pointer;">🔙 Go Back</button>
                      </div>';
                exit;
            }
        } else {
            echo '<div style="background-color: #ffdddd; color: #d8000c; padding: 15px; border: 1px solid #d8000c; text-align: center; font-size: 16px; margin-top: 20px; border-radius: 5px;">
                    ⚠️ Invalid email or password.<br><br>
                    <button onclick="history.back()" style="background-color: #d8000c; color: white; padding: 10px 15px; border: none; border-radius: 5px; cursor: pointer;">🔙 Go Back</button>
                  </div>';
            exit;
        }
    } else {
        echo '<div style="background-color: #ffdddd; color: #d8000c; padding: 15px; border: 1px solid #d8000c; text-align: center; font-size: 16px; margin-top: 20px; border-radius: 5px;">
                ⚠️ User not found. Please check your credentials.<br><br>
                <button onclick="history.back()" style="background-color: #d8000c; color: white; padding: 10px 15px; border: none; border-radius: 5px; cursor: pointer;">🔙 Go Back</button>
              </div>';
        exit;


    }
}

$conn->close();
?>
