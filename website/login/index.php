<?php
session_start();
include 'db_connect.php'; // Ensure this file establishes a MySQL connection

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = trim($_POST['email']);
    $password = trim($_POST['password']);

    if (!empty($email) && !empty($password)) {
        // Fetch user details from MySQL
        $stmt = $conn->prepare("SELECT id, password FROM users WHERE email = ?");
        $stmt->bind_param("s", $email);
        $stmt->execute();
        $stmt->store_result();

        if ($stmt->num_rows > 0) {
            $stmt->bind_result($user_id, $hashed_password);
            $stmt->fetch();

            if (password_verify($password, $hashed_password)) {
                // Store user session data
                $_SESSION['user_id'] = $user_id;
                $_SESSION['email'] = $email;

                // Redirect to dashboard
                header("Location: features/");
                exit();
            } else {
                $error = "Invalid password. Please try again.";
            }
        } else {
            $error = "No account found with this email.";
        }

        $stmt->close();
    } else {
        $error = "Please enter both email and password.";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
        .login-container { max-width: 400px; margin: auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px; }
        input { width: 90%; padding: 10px; margin: 10px 0; }
        button { width: 100%; padding: 10px; background: #28a745; color: white; border: none; cursor: pointer; }
        button:hover { background: #218838; }
        .error { color: red; }
    </style>
</head>
<body>

<div class="login-container">
    <h2>Login</h2>
    <?php if (isset($error)) { echo "<p class='error'>$error</p>"; } ?>
    
    <form method="POST">
        <input type="email" name="email" placeholder="Enter Email" required>
        <input type="password" name="password" placeholder="Enter Password" required>
        <button type="submit">Login</button>
    </form>
    
    <p>Don't have an account? <a href="/payments/public/signup.php">Sign Up</a></p>
</div>

</body>
</html>
