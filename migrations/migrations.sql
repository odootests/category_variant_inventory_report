-- set new column values to null
UPDATE public.stock_inventory_line SET product_template_id=null, product_template_name=null, product_attribute_id=null, product_attribute_name=null, product_category_id=null, product_category_name=null, product_attribute_value_id=null, product_attribute_value_name=null, actual_qty=null ;

-- Update product template ID 
UPDATE public.stock_inventory_line SET product_template_id=(SELECT product_tmpl_id FROM product_product WHERE id=(product_id)) WHERE product_template_id is null;

-- Update product Template Name
UPDATE public.stock_inventory_line SET product_template_name=(SELECT name FROM product_template WHERE id=(product_template_id)) WHERE product_template_name is null;

-- Update Product Attribute ID
UPDATE public.stock_inventory_line SET product_attribute_id=(SELECT attribute_id FROM product_attribute_line WHERE product_tmpl_id=(product_template_id)) WHERE product_attribute_id is null;

-- Update Product Attribute Name
UPDATE public.stock_inventory_line SET product_attribute_name=(SELECT name FROM product_attribute WHERE id=(product_attribute_id)) WHERE product_attribute_name is null;

-- Update Product Category ID
UPDATE public.stock_inventory_line SET product_category_id=(SELECT categ_id FROM product_template WHERE id=(product_template_id)) WHERE product_category_id is null;

-- Update Product Category Name
UPDATE public.stock_inventory_line SET product_category_name=(SELECT name FROM product_category WHERE id=(product_category_id)) WHERE product_category_name is null;

-- Update Product Attribute Value ID
UPDATE public.stock_inventory_line SET product_attribute_value_id=(SELECT product_attribute_value_id FROM product_attribute_value_product_product_rel WHERE product_product_id=(product_id)) WHERE product_attribute_value_id is null;

-- Update Product Attribute Value Name
UPDATE public.stock_inventory_line SET product_attribute_value_name=(SELECT name FROM product_attribute_value WHERE id=(product_attribute_value_id)) WHERE product_attribute_value_name is null;

-- Update Product Actual Quantity 
UPDATE public.stock_inventory_line SET actual_qty=(select currentTable.product_qty from (select product_id, MAX(create_date) as create_date from stock_inventory_line group by product_id) as newTable Inner JOIN stock_inventory_line as currentTable ON newTable.product_id = currentTable.product_id AND newTable.create_date = currentTable.create_date WHERE newTable.product_id =(stock_inventory_line.product_id)) where actual_qty is null;