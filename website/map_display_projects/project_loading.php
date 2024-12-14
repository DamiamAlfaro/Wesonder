<?php

// To my understanding, the code below is extracting the response from the 'index.php' function handleCheckboxClick
// where fetching of this file is occurring. The goal here is to first, make sure that the fetching actually works
// with the 'if' statement below.

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $checkboxName = $_POST['checkbox_name'] ?? '';
    $checkboxValue = $_POST['checkbox_value'] ?? '';
    $checkboxChecked = $_POST['checkbox_checked'] ?? '';
    
    // Once we enter the 'if' statement, i.e. once we assure connection with the fecthing, we begin to enter the MySQL
    // server and obtain all of the desired variables, i.e. the counties, names, etc. We do this in order to display 
    // such variables in the map on the other file. Basically, in this file we do the backbone of the map's
    // functionality. The first step, is to assure connection with MySQL. Once connected, we access our table in
    // question. We will echo a confirmation message "Working Properly".
    
    $host = "localhost"; 
    $username = "u978864605_wesonder";
    $password = "Elchapillo34?nmddam";
    $dbname = "u978864605_wesonder";
    
    $conn = new mysqli($host, $username, $password, $dbname);
    
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    } else {
        echo "\r\nWorking Properly\r\n";
    }
    
    $sql = "SELECT * FROM dir_projects WHERE county = '$checkboxValue' LIMIT 10";
    $result = $conn->query($sql);
    
    // Once connected to MySQL, let's implement all of the variables from the table in question, we will need them 
    // for map display in the future.
    
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            
            $project_number = $row['project_number'];
            $project_name = $row['project_name'];
            $awarding_body = $row['awarding_body'];
            $project_id_number = $row['project_id_number'];
            $project_dir_number = $row['project_dir_number'];
            $project_description = $row['project_description'];
            $start_date = $row['date_started'];
            $finish_date = $row['date_finished'];
            $complete_address = $row['complete_address'];
            $x_coordinates = $row['x_coordinates'];
            $y_coordinates = $row['y_coordinates'];
            $county = $row['county'];
            
            $string_display = "
            <strong>Project Name:</strong> $project_name <br>
            <strong>Project Number:</strong> $project_number <br>
            <strong>Awarding Body:</strong> $awarding_body <br>
            <strong>Address:</strong> $complete_address <br>
            <strong>Project ID Number:</strong> $project_id_number <br>
            <strong>Project DIR Number:</strong> $project_dir_number <br>
            <strong>Description:</strong> $project_description <br>
            <strong>Start Date:</strong> $start_date <br>
            <strong>End Date:</strong> $finish_date <br>
            ";
            
            echo $string_display . "\r\n\r\n";
            
        }
    }
    
    
    

    // Process the checkbox data
    if ($checkboxChecked === 'true') {
        echo  "Checkbox $checkboxName with value $checkboxValue was checked.";
        // Add your logic for a checked state here
    } else {
        echo "Checkbox $checkboxName with value $checkboxValue was unchecked.";
        // Add your logic for an unchecked state here
    }
    exit;
}

?>
