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
    $limit = 20;
    $page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
    $page = max($page, 1);
    $offset = ($page - 1) * $limit;

    // Valid columns for sorting and searching
    $valid_columns = [
        'weblink', 'county', 'bid_url', 'bid_ab', 'bid_posted_date', 'bid_title', 
        'bid_invitation_id', 'bid_due_date', 'bid_status', 'bid_submission_method'
    ];

    $sort_column = isset($_GET['sort']) && in_array($_GET['sort'], $valid_columns) ? $_GET['sort'] : 'bid_invitation_id';
    $sort_order = isset($_GET['order']) && $_GET['order'] === 'desc' ? 'DESC' : 'ASC';

    // Building the WHERE clause for search filters
    $where_clauses = [];
    $search_params = [];

    foreach ($valid_columns as $column) {
        if (!empty($_GET[$column])) {
            $search_value = strtolower($conn->real_escape_string($_GET[$column]));
            $where_clauses[] = "LOWER($column) LIKE '%$search_value%'";
            $search_params[$column] = $_GET[$column];
        }
    }

    $where_sql = $where_clauses ? implode(" AND ", $where_clauses) : "1";

    // Total number of rows with filters
    $total_result = $conn->query("SELECT COUNT(*) AS total FROM planetbids WHERE $where_sql");
    $total_rows = $total_result->fetch_assoc()['total'];
    $total_pages = ceil($total_rows / $limit);

    // SQL query with WHERE, ORDER BY, LIMIT, and OFFSET
    $sql = "SELECT * FROM planetbids 
            WHERE $where_sql 
            ORDER BY $sort_column $sort_order 
            LIMIT $limit OFFSET $offset";
    $result = $conn->query($sql);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PlanetBids List</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f9fafb;
            color: #333;
        }
        h1 {
            text-align: center;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            table-layout: fixed;
        }
        th, td {
            padding: 12px 15px;
            text-align: center;
            word-wrap: break-word;
        }
        th {
            background-color: #3674B5;
            color: white;
            text-transform: uppercase;
            cursor: pointer;
        }
        tr:nth-child(even) {
            background-color: #f3f4f6;
        }
        tr:hover {
            background-color: #e5e7eb;
        }
        input[type="text"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #d1d5db;
            border-radius: 4px;
        }
        .pagination {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin: 20px 0;
        }
        .pagination button {
            padding: 10px 20px;
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .pagination button:disabled {
            background-color: #9ca3af;
            cursor: not-allowed;
        }
    </style>
</head>
<body>
    <h1>PlanetBids</h1>

    <form method="GET">
        <table>
            <tr>
                <?php
                foreach ($valid_columns as $column) {
                    $new_order = ($sort_column === $column && $sort_order === 'ASC') ? 'desc' : 'asc';
                    echo "<th onclick=\"sortTable('$column', '$new_order')\">" . strtoupper(str_replace('_', ' ', $column)) . "</th>";
                }
                ?>
            </tr>
            <tr>
                <?php
                foreach ($valid_columns as $column) {
                    $value = isset($search_params[$column]) ? htmlspecialchars($search_params[$column]) : '';
                    echo "<td><input type='text' name='$column' value='$value' placeholder='Search...'></td>";
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
                echo "<tr><td colspan='10'>No records found.</td></tr>";
            }
            $conn->close();
            ?>
        </table>
        <button type="submit">Apply Filters</button>
    </form>

    <div class="pagination">
        <button onclick="navigatePage(<?php echo $page - 1; ?>)" <?php if ($page <= 1) echo 'disabled'; ?>>Previous</button>
        <input type="number" min="1" max="<?php echo $total_pages; ?>" value="<?php echo $page; ?>" id="pageInput">
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
                alert("Please enter a valid page number.");
            }
        }

        function sortTable(column, order) {
            const params = new URLSearchParams(window.location.search);
            params.set('sort', column);
            params.set('order', order);
            params.set('page', 1);
            window.location.search = params.toString();
        }
    </script>
</body>
</html>
