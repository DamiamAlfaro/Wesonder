<?php
session_start();
?>

<!DOCTYPE html>
<html>
  <head>
    <title>Wesonder/Checkout</title>
    <link rel="icon" type="image/png" href="../../media/bauhaus_logo_transparent.png"/>
    <style>
        body {
          background: #F5F5F5;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Ubuntu', sans-serif;
          overflow-x: hidden;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          margin: 0;
        }
        
        #background-logo {
            position: fixed;
            top: 6%;
            left: 50%;
            transform: translate(-50%, 0);
            width: 900px; /* Fixed width */
            height: auto; /* Maintain aspect ratio */
            opacity: 0.07;
            transition: transform 0.1s ease-out;
            z-index: -1;
        }

        section {
            background: #FFFFFF;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            width: 100%;
        }

        input[type="text"], input[type="email"], input[type="password"] {
          width: 94%;
          padding: 10px;
          margin: 10px 0;
          border: 1px solid #ccc;
          border-radius: 4px;
        }
        
        label {
          font-weight: 500;
        }
        
        #checkout-and-portal-button {
          height: 36px;
          background: #727D73;
          color: white;
          width: 100%;
          font-size: 14px;
          border: 0;
          font-weight: 500;
          cursor: pointer;
          letter-spacing: 0.6px;
          border-radius: 6px;
          transition: all 0.2s ease;
          box-shadow: 0px 4px 5.5px 0px rgba(0, 0, 0, 0.2);
        }

        #checkout-and-portal-button:hover {
          opacity: 0.8;
        }
    </style>
    <script src="https://js.stripe.com/v3/"></script>
  </head>
  <body>
    <img src="../../media/bauhaus_logo_circle_black.png" id="background-logo" alt="Background Logo">
    
    <section>
      <form action="create-checkout-session.php" method="POST">
        <label for="first_name">First Name</label>
        <input type="text" id="first_name" name="first_name" required>

        <label for="last_name">Last Name</label>
        <input type="text" id="last_name" name="last_name" required>

        <label for="company">Company Name (optional)</label>
        <input type="text" id="company" name="company">

        <label for="email">Email Address</label>
        <input type="email" id="email" name="email" required>

        <label for="password">Password</label>
        <input type="password" id="password" name="password" required>

        <input type="hidden" name="price_id" value="price_1QqkhTDVIvP3qVPid3WsEudD" />
        <button id="checkout-and-portal-button" type="submit">Checkout</button>
      </form>
    </section>
  </body>
</html>
