-- set new column to null
UPDATE public.stock_quant SET product_template_id=null, product_template_id_name=null, product_attribute_id=null, product_attribute_id_name=null, product_category_id=null, product_category_id_name=null, product_attribute_value_id=null, product_attribute_value_id_name=null ;

-- Update product template ID 
UPDATE public.stock_quant SET product_template_id=(SELECT product_tmpl_id FROM product_product WHERE id=(product_id)) WHERE product_template_id is null;

-- Update product Template Name
UPDATE public.stock_quant SET product_template_id_name=(SELECT name FROM product_template WHERE id=(product_template_id)) WHERE product_template_id_name is null;

-- Update Product Attribute ID
UPDATE public.stock_quant SET product_attribute_id=(SELECT attribute_id FROM product_attribute_line WHERE product_tmpl_id=(product_template_id)) WHERE product_attribute_id is null;

-- Update Product Attribute Name
UPDATE public.stock_quant SET product_attribute_id_name=(SELECT name FROM product_attribute WHERE id=(product_attribute_id)) WHERE product_attribute_id_name is null;

-- Update Product Category ID
UPDATE public.stock_quant SET product_category_id=(SELECT categ_id FROM product_template WHERE id=(product_template_id)) WHERE product_category_id is null;

-- Update Product Category Name
UPDATE public.stock_quant SET product_category_id_name=(SELECT name FROM product_category WHERE id=(product_category_id)) WHERE product_category_id_name is null;

-- Update Product Attribute Value ID
UPDATE public.stock_quant SET product_attribute_value_id=(SELECT product_attribute_value_id FROM product_attribute_value_product_product_rel WHERE product_product_id=(product_id)) WHERE product_attribute_value_id is null;

-- Update Product Attribute Value Name
UPDATE public.stock_quant SET product_attribute_value_id_name=(SELECT name FROM product_attribute_value WHERE id=(product_attribute_value_id)) WHERE product_attribute_value_id_name is null;