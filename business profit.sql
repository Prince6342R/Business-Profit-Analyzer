create database business_profit_analysis;
use business_profit_analysis;

select*from superstore;

# total rows persent in table:-
select count(*) from superstore;

#Total column show hoga:-
describe superstore;

# total column present in the table:-
select count(*) from information_schema.columns
where table_name='superstore'
AND table_schema='business_profit_analysis';

# Total Sales :- Business ne overall 22.9 lakh sales generate ki
select sum(sales) as total_sales from superstore;

# Total Profit:-Business overall profit me hai aur total profit around 2.86 lakh hai
select sum(Profit) as total_profit from superstore;

# Total Loss Transactions:- 1869 transactions business ko loss de rahe hain
select count(*) as loss_Transactions from superstore
where profit<0;

#High Discount Transactions:-1165 transactions me 30% se zyada discount diya gaya
select count(*) as discount_Transactions from superstore
where discount>0.3;

# Top Loss States:-Texas business ko sabse zyada loss de raha hai
select State,sum(Profit) as state_profit
from superstore
group by State
order by state_profit asc limit 10;

# Loss-Making Categories:-Furniture category comparatively low profit / losses generate kar rahi hai
select Category,sum(Profit) as category_profit
from superstore
group by Category
order by category_profit;

# Most Loss-Making Sub-Categories:-
select Sub_category,sum(Profit) as SubCategory_Profit
from superstore
group by Sub_category
order by SubCategory_Profit limit 10;

# Risk Category Distribution:-
select Risk_Category,count(*) as riskcategory_transaction
from superstore
group by Risk_Category;

# Risk-wise Profit Analysis:-
SELECT Risk_Category, SUM(Profit) AS Total_Profit
FROM superstore
GROUP BY Risk_Category;

# Top High Discount Loss Transactions:-
SELECT Category, Sub_Category, Sales, Discount, Profit
FROM superstore
WHERE Discount > 0.3 AND Profit < 0
ORDER BY Profit ASC LIMIT 10;

#Region-wise Profit Analysis:-
SELECT Region, SUM(Profit) AS Region_Profit
FROM superstore
GROUP BY Region
ORDER BY Region_Profit DESC;

# Segment-wise Profit Analysis:-
SELECT Segment, SUM(Profit) AS Segment_Profit
FROM superstore
GROUP BY Segment
ORDER BY Segment_Profit DESC;

#Ship Mode Profit Analysis:-
SELECT Ship_Mode, SUM(Profit) AS ShipMode_Profit
FROM superstore
GROUP BY Ship_Mode
ORDER BY ShipMode_Profit DESC;

#Average Discount by Category:-
SELECT Category, AVG(Discount) AS Avg_Discount
FROM superstore
GROUP BY Category
ORDER BY Avg_Discount DESC;


SELECT
SUM(Sales) AS Total_Sales,
SUM(Profit) AS Total_Profit,
COUNT(CASE WHEN Profit < 0 THEN 1 END) AS Loss_Transactions,
COUNT(CASE WHEN Discount > 0.3 THEN 1 END) AS High_Discount_Transactions
FROM superstore;