<?php
// Terms of Service Page
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terms of Service</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            max-width: 60vw;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        h1 {
        }

        h1, h2 {
            color: #333;
        }
        p {
            line-height: 1.6;
            text-align: left;
        }

        .go-back-button button {
            position: absolute;
            top: 4vh;
            left: 2vw;
        }
    </style>
</head>
<body>
    <div class="go-back-button">
        <button onclick="history.back()">&#8592;</button>
    </div>
    <div class="container">
        <h1>Terms of Service</h1>
        
        <h2>1. Subscription & Payment Terms</h2>
        <p>My service is offered on a subscription basis and billed on a recurring basis (e.g., monthly). By providing payment information, you authorize me to charge your selected payment method at the start of each billing cycle. Your subscription will automatically renew unless you cancel before the next billing period.</p>
        
        <h2>2. Refund & Cancellation Policy</h2>
        <p><strong>No Refunds:</strong> All subscription payments are final. I do not issue refunds for canceled subscriptions. When you cancel, you will retain access until the end of your current billing cycle, and you will not be charged again.</p>
        
        <h2>3. User Responsibilities & Account Security</h2>
        <p>You must provide accurate and complete information when registering and updating your account. You are responsible for maintaining the confidentiality of your login credentials.</p>
        
        <h2>4. Account Termination</h2>
        <p>I reserve the right to suspend or terminate your account if we detect fraud, misuse, or violations of these Terms.</p>
        
        
        <h2>5. Changes to These Terms</h2>
        <p>I reserve the right to update these Terms at any time. Your continued use of my service after any changes constitutes acceptance of the updated Terms.</p>
        
        <h2>6. Contact Information</h2>
        <p>For any questions about these Terms, please contact me at <a href="mailto:damiamalfaro@wesonder.com">damiamalfaro@wesonder.com</a></p>
    </div>
</body>
</html>
