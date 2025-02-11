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
        echo json_encode(["error" => "Connection failed: " . $conn->connect_error]);
        exit();
    } 
    
    $sql = "SELECT * FROM dvbe_entities WHERE Certification_Type LIKE '%$checkboxValue%' AND State = 'CA'";
    $result = $conn->query($sql);
    
    // Once connected to MySQL, let's implement all of the variables from the table in question, we will need them 
    // for map display in the future. We will create a list where we will store every single attribute of each of
    // the projects we want to display, once the list is filled with the variables, we will output it using to the
    // index file where the actual display takes place.
    
    $dvbes = [];
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $dvbes[] = [
                "Certification_ID" => $row['Certification_ID'],
                "Legal_Business_Name" => $row['Legal_Business_Name'],
                "Doing_Business_As_1" => $row['Doing_Business_As_1'],
                "Other_DBAs" => $row['Other_DBAs'],
                "Certification_Type" => $row['Certification_Type'],
                "Start_Date" => $row['Start_Date'],
                "End_Date" => $row['End_Date'],
                "Email_ID" => $row['Email_ID'],
                "First_Name" => $row['First_Name'],
                "Last_Name" => $row['Last_Name'],
                "URLID" => $row['URLID'],
                "Telephone" => $row['Telephone'],
                "Keywords" => $row['Keywords'],
                "License" => $row['License'],
                "Industry_Type" => $row['Industry_Type'],
                "Ethnicity" => $row['Ethnicity'],
                "Race" => $row['Race'],
                "Gender_Identity" => $row['Gender_Identity'],
                "LGBQTIA" => $row['LGBQTIA'],
                "CompleteAddress" => $row['CompleteAddress'],
                "x_coordinates" => $row['X_Coordinates'],
                "y_coordinates" => $row['Y_Coordinates']
            ];
        }
    }
    

    if ($checkboxChecked === 'true') {
        echo json_encode([
            "status" => "success",
            "dvbes" => $dvbes
        ]);
    } else {
        echo json_encode([
            "status" => "unchecked",
            "message" => "Checkbox was unchecked."
        ]);
    }
    exit();
            
    
    

}

?>