<?php
    // Database connection details
    $host = "localhost"; 
    $username = "u978864605_wesonder";
    $password = "Elchapillo34?nmddam";
    $dbname = "u978864605_wesonder";

    // Connect to the database
    $conn = new mysqli($host, $username, $password, $dbname);

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Pagination settings
    $limit = 40;
    $page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
    $page = max($page, 1);
    $offset = ($page - 1) * $limit;

    // Sorting logic (excluding x_coordinate and y_coordinate)
    $valid_columns = [
        'license_number', 'business_type', 'contractor_name', 'street_address',
        'city', 'state', 'zip_code', 'county', 'phone_number',
        'issue_date', 'expiration_date', 'classifications',
        'complete_address'
    ];

    $sort_column = isset($_GET['sort']) && in_array($_GET['sort'], $valid_columns) ? $_GET['sort'] : 'license_number';
    $sort_order = isset($_GET['order']) && $_GET['order'] === 'desc' ? 'DESC' : 'ASC';

    // Total number of rows with state = 'CA'
    $total_result = $conn->query("SELECT COUNT(*) AS total FROM cslb_contractors WHERE state = 'CA'");
    $total_rows = $total_result->fetch_assoc()['total'];
    $total_pages = ceil($total_rows / $limit);

    // SQL query with WHERE, ORDER BY, LIMIT, and OFFSET
    $sql = "SELECT * FROM cslb_contractors 
            WHERE state = 'CA' 
            ORDER BY $sort_column $sort_order 
            LIMIT $limit OFFSET $offset";
    $result = $conn->query($sql);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/png" href="../media/bauhaus_logo_transparent.png"/>
    <title>Contractors Tabulation</title>
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
            cursor: pointer;
        }
        th.sort-asc::after {
            content: " ▲";
        }
        th.sort-desc::after {
            content: " ▼";
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
            <?php
            // Generate sortable table headers (excluding x_coordinate and y_coordinate)
            foreach ($valid_columns as $column) {
                $new_order = ($sort_column === $column && $sort_order === 'ASC') ? 'desc' : 'asc';
                $sort_class = ($sort_column === $column) ? 'sort-' . strtolower($sort_order) : '';
                echo "<th class='$sort_class' onclick=\"sortTable('$column', '$new_order')\">" . ucfirst(str_replace('_', ' ', $column)) . "</th>";
            }
            ?>
        </tr>

        <?php
        if ($result->num_rows > 0) {
            while ($row = $result->fetch_assoc()) {
                echo "<tr>";
                foreach ($valid_columns as $column) {
                    echo "<td>" . htmlspecialchars($row[$column]) . "</td>";
                }
                echo "</tr>";
            }
        } else {
            echo "<tr><td colspan='13'>No contractors found in California.</td></tr>";
        }

        $conn->close();
        ?>
    </table>

    <!-- Pagination Controls -->
    <div class="pagination">
        <button onclick="navigatePage(<?php echo $page - 1; ?>)" <?php if ($page <= 1) echo 'disabled'; ?>>Previous</button>

        <label for="pageInput">Page:</label>
        <input type="number" id="pageInput" min="1" max="<?php echo $total_pages; ?>" value="<?php echo $page; ?>">
        <button onclick="goToPage()">Go</button>

        <button onclick="navigatePage(<?php echo $page + 1; ?>)" <?php if ($page >= $total_pages) echo 'disabled'; ?>>Next</button>
    </div>

    <script>
        function navigatePage(page) {
            const params = new URLSearchParams(window.location.search);
            params.set('page', page);
            window.location.search = params.toString();
        }

        function goToPage() {
            const page = parseInt(document.getElementById('pageInput').value);
            if (page >= 1 && page <= <?php echo $total_pages; ?>) {
                navigatePage(page);
            } else {
                alert("Please enter a number between 1 and <?php echo $total_pages; ?>.");
            }
        }

        function sortTable(column, order) {
            const params = new URLSearchParams(window.location.search);
            params.set('sort', column);
            params.set('order', order);
            params.set('page', 1); // Reset to the first page when sorting
            window.location.search = params.toString();
        }

        document.getElementById('pageInput').addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                goToPage();
            }
        });
    </script>
</body>
</html>
