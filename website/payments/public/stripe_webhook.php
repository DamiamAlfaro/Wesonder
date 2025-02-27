<?php
// Include Stripe's PHP library
require_once '../vendor/autoload.php';
require_once '../secrets.php'; // Contains $stripeSecretKey

// Database connection details
$servername = "localhost";
$username = "u978864605_wesonder";
$password_db = "Elchapillo34?nmddam";
$dbname = "u978864605_wesonder";

// Connect to MySQL database
$conn = new mysqli($servername, $username, $password_db, $dbname);
if ($conn->connect_error) {
    http_response_code(500);
    exit("Database connection failed: " . $conn->connect_error);
}

// Set Stripe API Key
\Stripe\Stripe::setApiKey($stripeSecretKey);

// Retrieve the raw POST body from Stripe
$payload = @file_get_contents("php://input");
$sig_header = $_SERVER["HTTP_STRIPE_SIGNATURE"];
$endpoint_secret = 'whsec_3FT9EqbyDDT61KMuDRiES6oYXsR7sFe6'; // Replace with your actual webhook secret

try {
    $event = \Stripe\Webhook::constructEvent($payload, $sig_header, $endpoint_secret);
} catch (\Exception $e) {
    http_response_code(400);
    exit("Invalid webhook signature: " . $e->getMessage());
}

// Handle webhook event for successful payment
if ($event->type == 'checkout.session.completed') {
    $session = $event->data->object;
    $email = $session->customer_email;
    $stripe_customer_id = $session->customer;
    $stripe_subscription_id = $session->subscription;
    $created_at = date("Y-m-d H:i:s");

    // Retrieve user data from pending_users
    $stmt = $conn->prepare("SELECT first_name, last_name, company, password FROM pending_users WHERE email = ?");
    $stmt->bind_param("s", $email);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows > 0) {
        $stmt->bind_result($first_name, $last_name, $company, $password_hash);
        $stmt->fetch();
        $stmt->close();

        // Insert into users table
        $insert_stmt = $conn->prepare("INSERT INTO users (name, last_name, email, company_name, password_hash, stripe_customer_id, stripe_subscription_id, subscription_status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, 'paid', ?)");
        $insert_stmt->bind_param(
            "ssssssss",
            $first_name,
            $last_name,
            $email,
            $company,
            $password_hash,
            $stripe_customer_id,
            $stripe_subscription_id,
            $created_at
        );

        if ($insert_stmt->execute()) {
            // Delete from pending_users
            $delete_stmt = $conn->prepare("DELETE FROM pending_users WHERE email = ?");
            $delete_stmt->bind_param("s", $email);
            $delete_stmt->execute();
            $delete_stmt->close();
            
            // Send confirmation email
            $to = $email;
            $subject = "Wesonder - Confirmation of Sign-Up";
            $message = "
            <html>
            <head>
                <title>Wesonder - Welcome!</title>
            </head>
            <body>
                <h2>Welcome to Wesonder, $first_name!</h2>
                <p>Thank you for signing up. Your account has been successfully activated.</p>
                <p>You now have access to premium features.</p>
                <p>Login here: <a href='https://wesonder.com/'>Wesonder Login</a></p>
                <p>If you have any questions, feel free to reach out to me <a href='mailto:damiamalfaro@wesonder.com'>damiamalfaro@wesonder.com</a></p>
                <br>
                <p>Best regards,</p>
                <p>Damiam Alfaro</p>
            </body>
            </html>
            ";
            $headers = "MIME-Version: 1.0" . "\r\n";
            $headers .= "Content-type:text/html;charset=UTF-8" . "\r\n";
            $headers .= "From: no-reply@wesonder.com" . "\r\n";

            // Send email
            if (!mail($to, $subject, $message, $headers)) {
                error_log("Failed to send confirmation email to " . $email);
            }

            http_response_code(200);
            echo "User moved to users table after successful payment.";
        } else {
            http_response_code(500);
            echo "Failed to move user to users table: " . $insert_stmt->error;
        }

        $insert_stmt->close();
    } else {
        http_response_code(404);
        echo "User not found in pending_users.";
    }
}

// Close the database connection
$conn->close();
http_response_code(200);
?>
