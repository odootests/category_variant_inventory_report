SELECT currentTable.product_id, currentTable.product_qty, newTable.create_date FROM
(SELECT product_id, MAX(create_date) AS create_date
FROM stock_inventory_line 
GROUP BY product_id) AS newTable
INNER JOIN stock_inventory_line AS currentTable
ON newTable.product_id = currentTable.product_id AND 
newTable.create_date = currentTable.create_date;
