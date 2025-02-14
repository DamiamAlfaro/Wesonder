<?php
// Include Stripe's PHP library
require_once '../vendor/autoload.php';
require_once '../secrets.php'; // Contains Stripe secret key

// Database connection details
$servername = "localhost";
$username = "u978864605_wesonder";
$password_db = "Elchapillo34?nmddam";
$dbname = "u978864605_wesonder";

// Create connection
$conn = new mysqli($servername, $username, $password_db, $dbname);
if ($conn->connect_error) {
    die("Database connection failed: " . $conn->connect_error);
}

// Check if the request method is POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Retrieve form data and sanitize inputs
    $first_name = htmlspecialchars($_POST['first_name']);
    $last_name = htmlspecialchars($_POST['last_name']);
    $company = !empty($_POST['company']) ? htmlspecialchars($_POST['company']) : NULL;
    $email = htmlspecialchars($_POST['email']);
    $password = password_hash($_POST['password'], PASSWORD_DEFAULT);
    $created_at = date("Y-m-d H:i:s");

    // Check if the email already exists in pending_users
    $stmt = $conn->prepare("SELECT email FROM pending_users WHERE email = ?");
    $stmt->bind_param("s", $email);
    $stmt->execute();
    $stmt->store_result();
    
    if ($stmt->num_rows > 0) {
        // If the email exists, update the record
        $stmt->close();
        $update_stmt = $conn->prepare("UPDATE pending_users SET first_name = ?, last_name = ?, company = ?, password = ?, created_at = ? WHERE email = ?");
        $update_stmt->bind_param("ssssss", $first_name, $last_name, $company, $password, $created_at, $email);
        
        if (!$update_stmt->execute()) {
            die("Error updating pending user: " . $update_stmt->error);
        }
        $update_stmt->close();
    } else {
        // If email does not exist, insert new record
        $stmt->close();
        $insert_stmt = $conn->prepare("INSERT INTO pending_users (first_name, last_name, company, email, password, created_at) VALUES (?, ?, ?, ?, ?, ?)");
        $insert_stmt->bind_param("ssssss", $first_name, $last_name, $company, $email, $password, $created_at);

        if (!$insert_stmt->execute()) {
            die("Error inserting pending user: " . $insert_stmt->error);
        }
        $insert_stmt->close();
    }

    // Initialize Stripe with the secret key
    \Stripe\Stripe::setApiKey($stripeSecretKey);

    // Create a Stripe Checkout Session
    try {
        $checkout_session = \Stripe\Checkout\Session::create([
            'payment_method_types' => ['card'],
            'customer_email' => $email,
            'line_items' => [[
                'price' => 'price_1QqkhTDVIvP3qVPid3WsEudD',
                'quantity' => 1,
            ]],
            'mode' => 'subscription',
            'success_url' => 'https://wesonder.com/features/index.php?session_id={CHECKOUT_SESSION_ID}', 
            'cancel_url' => 'https://wesonder.com/',
            'metadata' => ['email' => $email]
        ]);

        // Redirect user to Stripe Checkout page
        header("Location: " . $checkout_session->url);
        exit;
    } catch (Exception $e) {
        die("Error creating Stripe Checkout session: " . $e->getMessage());
    }
}

// Close the database connection
$conn->close();
?>
