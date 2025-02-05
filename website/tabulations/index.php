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
    <link rel="icon" type="image/png" href="../media/bauhaus_logo_transparent.png"/>
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
        .pagination input[type="number"] {
            width: 80px;
            padding: 6px;
            margin: 0 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        .pagination button {
            padding: 8px 16px;
            margin: 0 5px;
            border: none;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            border-radius: 4px;
        }
        .pagination button:hover {
            background-color: #45a049;
        }
        .pagination button:disabled {
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
                echo "</tr>";
            }
        } else {
            echo "<tr><td colspan='15'>No contractors found.</td></tr>";
        }

        $conn->close();
        ?>
    </table>

    <!-- Pagination Controls with Input -->
    <div class="pagination">
        <button onclick="navigatePage(<?php echo $page - 1; ?>)" <?php if ($page <= 1) echo 'disabled'; ?>>Previous</button>

        <label for="pageInput">Page:</label>
        <input type="number" id="pageInput" min="1" max="<?php echo $total_pages; ?>" value="<?php echo $page; ?>">
        <button onclick="goToPage()">Go</button>

        <button onclick="navigatePage(<?php echo $page + 1; ?>)" <?php if ($page >= $total_pages) echo 'disabled'; ?>>Next</button>
    </div>

    <script>
        function navigatePage(page) {
            if (page >= 1 && page <= <?php echo $total_pages; ?>) {
                window.location.href = "?page=" + page;
            }
        }

        function goToPage() {
            const page = parseInt(document.getElementById('pageInput').value);
            if (page >= 1 && page <= <?php echo $total_pages; ?>) {
                navigatePage(page);
            } else {
                alert("Please enter a number between 1 and <?php echo $total_pages; ?>.");
            }
        }

        // Trigger "Go" on Enter key press
        document.getElementById('pageInput').addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                goToPage();
            }
        });
    </script>
</body>
</html>
