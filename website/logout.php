<?php
session_start();
session_destroy();
header("Location: /"); // Redirect back to homepage
exit;
?>
