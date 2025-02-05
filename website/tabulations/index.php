<?php
    // Database connection details
    $host = "localhost"; 
    $username = "u978864605_wesonder";
    $password = "Elchapillo34?nmddam";
    $dbname = "u978864605_wesonder";

    // Connect to the database
    $conn = new mysqli($host, $username, $password, $dbname);

    // Check the connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Pagination logic
    $limit = 40; // Rows per page
    $page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
    $page = max($page, 1); // Ensure page is at least 1
    $offset = ($page - 1) * $limit;

    // Get total number of rows
    $total_result = $conn->query("SELECT COUNT(*) AS total FROM cslb_contractors");
    $total_rows = $total_result->fetch_assoc()['total'];
    $total_pages = ceil($total_rows / $limit);

    // SQL query with LIMIT and OFFSET
    $sql = "SELECT * FROM cslb_contractors LIMIT $limit OFFSET $offset";
    $result = $conn->query($sql);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contractors List</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f4f4;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            background-color: white;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
        .pagination {
            margin: 20px 0;
            text-align: center;
        }
        .pagination a {
            display: inline-block;
            padding: 8px 16px;
            margin: 0 5px;
            border: 1px solid #4CAF50;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 4px;
        }
        .pagination a:hover {
            background-color: #45a049;
        }
        .pagination a.disabled {
            background-color: #ccc;
            cursor: not-allowed;
        }
    </style>
</head>
<body>
    <h1>CSLB Contractors List</h1>
    <table>
        <tr>
            <th>License Number</th>
            <th>Business Type</th>
            <th>Contractor Name</th>
            <th>Street Address</th>
            <th>City</th>
            <th>State</th>
            <th>Zip Code</th>
            <th>County</th>
            <th>Phone Number</th>
            <th>Issue Date</th>
            <th>Expiration Date</th>
            <th>Classifications</th>
            <th>Complete Address</th>
            <th>X Coordinate</th>
            <th>Y Coordinate</th>
        </tr>

        <?php
        if ($result->num_rows > 0) {
            while ($row = $result->fetch_assoc()) {
                echo "<tr>";
                echo "<td>" . htmlspecialchars($row['license_number']) . "</td>";
                echo "<td>" . htmlspecialchars($row['business_type']) . "</td>";
                echo "<td>" . htmlspecialchars($row['contractor_name']) . "</td>";
                echo "<td>" . htmlspecialchars($row['street_address']) . "</td>";
                echo "<td>" . htmlspecialchars($row['city']) . "</td>";
                echo "<td>" . htmlspecialchars($row['state']) . "</td>";
                echo "<td>" . htmlspecialchars($row['zip_code']) . "</td>";
                echo "<td>" . htmlspecialchars($row['county']) . "</td>";
                echo "<td>" . htmlspecialchars($row['phone_number']) . "</td>";
                echo "<td>" . htmlspecialchars($row['issue_date']) . "</td>";
                echo "<td>" . htmlspecialchars($row['expiration_date']) . "</td>";
                echo "<td>" . htmlspecialchars($row['classifications']) . "</td>";
                echo "<td>" . htmlspecialchars($row['complete_address']) . "</td>";
                echo "<td>" . htmlspecialchars($row['x_coordinate']) . "</td>";
                echo "<td>" . htmlspecialchars($row['y_coordinate']) . "</td>";
                echo "</tr>";
            }
        } else {
            echo "<tr><td colspan='15'>No contractors found.</td></tr>";
        }

        $conn->close();
        ?>
    </table>

    <!-- Pagination Controls -->
    <div class="pagination">
        <?php if ($page > 1): ?>
            <a href="?page=<?php echo $page - 1; ?>">Previous</a>
        <?php else: ?>
            <a class="disabled">Previous</a>
        <?php endif; ?>

        <?php for ($i = 1; $i <= $total_pages; $i++): ?>
            <a href="?page=<?php echo $i; ?>" <?php if ($i == $page) echo 'style="background-color: #45a049;"'; ?>>
                <?php echo $i; ?>
            </a>
        <?php endfor; ?>

        <?php if ($page < $total_pages): ?>
            <a href="?page=<?php echo $page + 1; ?>">Next</a>
        <?php else: ?>
            <a class="disabled">Next</a>
        <?php endif; ?>
    </div>
</body>
</html>
