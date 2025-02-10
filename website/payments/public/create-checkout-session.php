<?php

require_once '../vendor/autoload.php';
require_once '../secrets.php';

\Stripe\Stripe::setApiKey($stripeSecretKey);

header('Content-Type: application/json');

$YOUR_DOMAIN = 'https://wesonder.com/payments/public/';

try {
  // Use the price_id directly from the form POST data
  $price_id = $_POST['price_id'];

  // Create the checkout session
  $checkout_session = \Stripe\Checkout\Session::create([
    'line_items' => [[
      'price' => $price_id,
      'quantity' => 1,
    ]],
    'mode' => 'subscription',
    'success_url' => $YOUR_DOMAIN . 'success.html?session_id={CHECKOUT_SESSION_ID}',
    'cancel_url' => $YOUR_DOMAIN . 'cancel.html',
  ]);

  // Redirect to the checkout session
  header("HTTP/1.1 303 See Other");
  header("Location: " . $checkout_session->url);
} catch (Exception $e) {
  http_response_code(500);
  echo json_encode(['error' => $e->getMessage()]);
}
