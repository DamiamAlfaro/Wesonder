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
    
    $sql = "SELECT * FROM cslb_contractors WHERE county = '$checkboxValue' LIMIT 100";
    $result = $conn->query($sql);
    
    // Once connected to MySQL, let's implement all of the variables from the table in question, we will need them 
    // for map display in the future. We will create a list where we will store every single attribute of each of
    // the projects we want to display, once the list is filled with the variables, we will output it using to the
    // index file where the actual display takes place.
    
    $contractors = [];
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $contractors[] = [
                "license_number" => $row['license_number'],
                "business_type" => $row['business_type'],
                "contractor_name" => $row['name'],
                "county" => $row['county'],
                "phone_number" => $row['phone_number'],
                "issue_date" => $row['issue_date'],
                "expiration_date" => $row['expiration_date'],
                "classifications" => $row['classifications'],
                "complete_address" => $row['complete_address'],
                "x_coordinates" => $row['x_coordinate'],
                "y_coordinates" => $row['y_coordinate']
            ];
        }
    }
    

    if ($checkboxChecked === 'true') {
        echo json_encode([
            "status" => "success",
            "contractors" => $contractors
        ]);
    } else {
        echo json_encode([
            "status" => "unchecked",
            "message" => "Checkbox was unchecked."
        ]);
    }
    exit();
            
    //         $string_display = "
    //         <strong>Project Name:</strong> $project_name <br>
    //         <strong>Project Number:</strong> $project_number <br>
    //         <strong>Awarding Body:</strong> $awarding_body <br>
    //         <strong>Address:</strong> $complete_address <br>
    //         <strong>Project ID Number:</strong> $project_id_number <br>
    //         <strong>Project DIR Number:</strong> $project_dir_number <br>
    //         <strong>Description:</strong> $project_description <br>
    //         <strong>Start Date:</strong> $start_date <br>
    //         <strong>End Date:</strong> $finish_date <br>
    //         ";
            
            
    //     }
    // }
    
    

}

?>
