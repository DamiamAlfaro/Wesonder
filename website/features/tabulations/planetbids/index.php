<?php
    // Enable error reporting
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
    ini_set('log_errors', 1);
    ini_set('error_log', __DIR__ . '/php-error.log'); // Log errors to a file

    // Custom error handler
    set_error_handler(function ($errno, $errstr, $errfile, $errline) {
        $errorMessage = "Error: $errstr in $errfile on line $errline";
        error_log($errorMessage);
        
        // Display a user-friendly error message
        echo "<div style='color: red; font-weight: bold; margin: 20px;'>
                An error occurred: <br>
                <strong>$errstr</strong> <br>
                Please contact <a href='mailto:support@wesonder.com'>support@wesonder.com</a> with this message.
              </div>";
        
        // Logout option
        echo "<div style='margin: 20px;'>
                <a href='/logout.php' style='color: blue; text-decoration: underline;'>Click here to log out</a>
              </div>";

        exit;
    });

    // Ensure the user is logged in
    require_once '../../auth_check.php';
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
        'bid_url', 'awarding_body', 'posted_date', 'bid_title', 'solicitation_number',
        'bid_due_date', 'bid_due_time', 'bid_status', 'submission_method', 'county',
        'naics_codes'
    ];

    $sort_column = isset($_GET['sort']) && in_array($_GET['sort'], $valid_columns) ? $_GET['sort'] : 'solicitation_number';
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
    $total_result = $conn->query("SELECT COUNT(*) AS total FROM planetbids_active_bids WHERE $where_sql");
    $total_rows = $total_result->fetch_assoc()['total'];
    $total_pages = ceil($total_rows / $limit);

    // SQL query with WHERE, ORDER BY, LIMIT, and OFFSET
    $sql = "SELECT * FROM planetbids_active_bids 
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
    <title>Bid Listings</title>
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
            table-layout: fixed;
        }
        th, td {
            padding: 12px 15px;
            text-align: center;
            word-wrap: break-word;
            max-height: 60px;
            overflow: hidden;
            text-overflow: ellipsis;
            cursor: pointer;
        }
        th {
            background-color: #3674B5;
            color: white;
            text-transform: uppercase;
        }
        tr:nth-child(even) {
            background-color: #f3f4f6;
        }
        tr:hover {
            background-color: #e5e7eb;
        }
        input[type="text"] {
            width: calc(100% - 16px);
            padding: 8px;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .pagination {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin: 20px 0;
        }
        .pagination button, button[type="submit"] {
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
        .pagination input[type="number"] {
            width: 80px;
            padding: 8px;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            text-align: center;
        }
        td.expanded {
            max-height: none !important;
            white-space: normal;
        }
    </style>
</head>
<body>
    <div class="header">
        <img src="../../../media/bauhaus_logo_circle_black.png" alt="Logo">
        <h1>Planetbids Active Bids</h1>
    </div>

    <form method="GET">
        <table>
            <tr>
                <?php
                // Mapping of emojis to each column
                $emojis = [
                    'bid_url' => '🔗',
                    'awarding_body' => '🏢',
                    'posted_date' => '📅',
                    'bid_title' => '📄',
                    'solicitation_number' => '🔢',
                    'bid_due_date' => '⏰',
                    'bid_due_time' => '🕒',
                    'bid_status' => '📊',
                    'submission_method' => '📤',
                    'county' => '🌍',
                    'naics_codes' => '💼'
                ];
                
                foreach ($valid_columns as $column) {
                    $new_order = ($sort_column === $column && $sort_order === 'ASC') ? 'desc' : 'asc';
                    $emoji = isset($emojis[$column]) ? $emojis[$column] : '';
                    echo "<th onclick=\"sortTable('$column', '$new_order')\">$emoji " . strtoupper(str_replace('_', ' ', $column)) . "</th>";
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
                        $content = htmlspecialchars($row[$column]);
                        if ($column === 'bid_url') {
                            echo "<td><a href='$content' target='_blank'>Bid Link</a></td>";
                        } elseif (strlen($content) > 50) {
                            echo "<td onclick=\"this.classList.toggle('expanded')\">" . substr($content, 0, 50) . "..." . "</td>";
                        } else {
                            echo "<td>$content</td>";
                        }
                    }
                    echo "</tr>";
                }
            } else {
                echo "<tr><td colspan='11'>No records found.</td></tr>";
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
