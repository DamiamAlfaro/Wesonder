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
        'functional_url', 'solicitation_value', 'notice_type_element', 'due_date', 'posting_date', 'set_aside_code', 
        'contact_name', 'description', 'subject', 'product_service_code', 
        'naics_code', 'dodaac', 
        'office_address'
    ];

    $sort_column = isset($_GET['sort']) && in_array($_GET['sort'], $valid_columns) ? $_GET['sort'] : 'subject';
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

    $where_sql = $where_clauses ? implode(" AND ", $where_clauses) : '1';

    // Total number of rows with filters
    $total_result = $conn->query("SELECT COUNT(*) AS total FROM finalized_piee_bids WHERE $where_sql");
    $total_rows = $total_result->fetch_assoc()['total'];
    $total_pages = ceil($total_rows / $limit);

    // SQL query with WHERE, ORDER BY, LIMIT, and OFFSET
    $sql = "SELECT * FROM finalized_piee_bids 
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
    <link rel="icon" type="image/png" href="../../../../media/bauhaus_logo_transparent.png"/>
    <title>PIEE Bids</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            margin: 20px;
            background-color: #f9fafb;
            color: #333;
        }
        .header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-bottom: 1%;
        }
        .header img {
            height: 4rem;
            width: auto;
        }
        h1 {
            font-size: 2rem;
            margin: 0;
            cursor: default;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        th, td {
            padding: 12px 15px;
            text-align: center;
        }
        th {
            background-color: #23486A;
            color: white;
            text-transform: uppercase;
            position: sticky;
            top: 0;
            cursor: grab;
        }
        tr {
            cursor: crosshair;
        }
        th.sort-asc::after {
            content: " \25B2";
        }
        th.sort-desc::after {
            content: " \25BC";
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
            outline: none;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            border-color: #2563eb;
        }
        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
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
            transition: background-color 0.3s;
        }
        .pagination button:hover {
            background-color: #1d4ed8;
        }
        .pagination button:disabled {
            background-color: #9ca3af;
            cursor: not-allowed;
        }
        .pagination input[type="number"] {
            width: 60px;
            padding: 8px;
            border: 1px solid #d1d5db;
            border-radius: 4px;
        }
        .hidden-description {
            display: block;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 300px;
            transition: all 0.3s ease-in-out;
            text-decoration: underline;
        }
        .hidden-description:hover {
            white-space: normal;
            overflow: hidden;
            text-overflow: clip;
            max-height: 100%;
            background-color: #f9fafb;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 10px;
            font-size: 20px;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="header">
        <img src="../../../media/bauhaus_logo_circle_black.png" alt="Logo">
        <h1>PIEE Bids</h1>
    </div>
    
    <div class="pagination">
        <button onclick="navigatePage(<?php echo $page - 1; ?>)" <?php if ($page <= 1) echo 'disabled'; ?>>Previous</button>
        <label>Page:</label>
        <input type="number" min="1" max="<?php echo $total_pages; ?>" value="<?php echo $page; ?>" id="pageInput">
        <button onclick="goToPage()">Go</button>
        <button onclick="navigatePage(<?php echo $page + 1; ?>)" <?php if ($page >= $total_pages) echo 'disabled'; ?>>Next</button>
    </div>

    <form method="GET" id="searchForm">
        <table>
            <tr>
                <?php
                $column_emojis = [
                    'functional_url' => '🌐',
                    'solicitation_value' => '💵',
                    'notice_type_element' => '📄',
                    'due_date' => '📅',
                    'set_aside_code' => '🎯',
                    'contact_name' => '👤',
                    'description' => '📝',
                    'subject' => '📌',
                    'posting_date' => '📆',
                    'product_service_code' => '🔧',
                    'naics_code' => '📇',
                    'place_of_performance' => '📍',
                    'address' => '🏠',
                    'dodaac' => '🏢',
                    'office_name' => '🏛️',
                    'office_address' => '🏤',
                    'X_Coordinates' => '❌',
                    'Y_Coordinates' => '🔼'
                ];

                foreach ($valid_columns as $column) {
                    $new_order = ($sort_column === $column && $sort_order === 'ASC') ? 'desc' : 'asc';
                    $sort_class = ($sort_column === $column) ? 'sort-' . strtolower($sort_order) : '';
                    $emoji = isset($column_emojis[$column]) ? $column_emojis[$column] . ' ' : '';

                    echo "<th class='$sort_class' onclick=\"sortTable('$column', '$new_order')\">" 
                        . $emoji . strtoupper(str_replace('_', ' ', $column)) 
                        . "</th>";
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
                        if ($column === 'functional_url') {
                            echo "<td><a href='" . htmlspecialchars($row[$column]) . "' target='_blank'>Link</a></td>";
                        } elseif ($column === 'description') {
                            echo "<td class='hidden-description'>" . htmlspecialchars($row[$column]) . "</td>";
                        } else {
                            echo "<td>" . htmlspecialchars($row[$column]) . "</td>";
                        }
                    }
                    echo "</tr>";
                }
            } else {
                echo "<tr><td colspan='18'>No bids found with those parameters.</td></tr>";
            }
            $conn->close();
            ?>
        </table>
        <button type="submit" style="margin-top: 10px; background-color: #2563eb; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;">Apply Filters</button>
    </form>

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
            document.querySelectorAll('input[type="text"]').forEach(input => {
                if (input.value) params.set(input.name, input.value);
            });
            window.location.search = params.toString();
        }
    </script>
</body>
</html>