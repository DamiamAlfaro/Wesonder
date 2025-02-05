<!DOCTYPE<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="author" content="Damiam Alfaro">
    <meta name="description" content="WESONDER Tabulation">
    <link rel="icon" type="image/png" href="../media/bauhaus_logo_transparent.png"/>
    <title>Tabulations</title>
</head>
<body>


	<?php

        $host = "localhost"; 
        $username = "u978864605_wesonder";
        $password = "Elchapillo34?nmddam";
        $dbname = "u978864605_wesonder";
        
        // Connect to the database
        $conn = new mysqli($host, $username, $password, $dbname);
        
        
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

	?>


	<main>
	    <h1>Welcome to My Website!</h1>
	    <p>This is my first HTML page.</p>
	</main>











</body>
</html>
