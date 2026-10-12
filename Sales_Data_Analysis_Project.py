import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# SALES DATA ANALYSIS PROJECT
# ============================================================
# Dataset files required in the same folder as this Python file:
#     customers.csv
#     products.csv
#     sales.csv
#
# Libraries used:
#     Pandas
#     Matplotlib
#     Seaborn
# ============================================================

sns.set_theme(style="whitegrid")


# ============================================================
# 1. LOAD DATASET
# ============================================================

customers = pd.read_csv("customers.csv")
products = pd.read_csv("products.csv")
sales = pd.read_csv("sales.csv")

print("=" * 70)
print("SALES DATA ANALYSIS PROJECT")
print("=" * 70)

print("\nCUSTOMERS DATA")
print(customers.head())
print("Shape:", customers.shape)

print("\nPRODUCTS DATA")
print(products.head())
print("Shape:", products.shape)

print("\nSALES DATA")
print(sales.head())
print("Shape:", sales.shape)


# ============================================================
# 2. DATASET INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("DATASET INFORMATION")
print("=" * 70)

print("\nCustomers columns:")
print(customers.columns.tolist())

print("\nProducts columns:")
print(products.columns.tolist())

print("\nSales columns:")
print(sales.columns.tolist())

print("\nCustomers information:")
customers.info()

print("\nProducts information:")
products.info()

print("\nSales information:")
sales.info()


# ============================================================
# 3. DATA QUALITY CHECK
# ============================================================

print("\n" + "=" * 70)
print("DATA QUALITY CHECK")
print("=" * 70)

print("\nMissing values in customers:")
print(customers.isnull().sum())

print("\nMissing values in products:")
print(products.isnull().sum())

print("\nMissing values in sales:")
print(sales.isnull().sum())

print("\nDuplicate rows:")
print("Customers:", customers.duplicated().sum())
print("Products:", products.duplicated().sum())
print("Sales:", sales.duplicated().sum())

print("\nUnique IDs:")
print("Customer IDs:", customers["Customer_ID"].nunique())
print("Product IDs:", products["Product_ID"].nunique())
print("Order IDs:", sales["Order_ID"].nunique())


# ============================================================
# 4. DATA TYPE CONVERSION
# ============================================================

customers["Registration_Date"] = pd.to_datetime(
    customers["Registration_Date"], errors="coerce"
)

customers["Date_of_Birth"] = pd.to_datetime(
    customers["Date_of_Birth"], errors="coerce"
)

sales["Order_Date"] = pd.to_datetime(
    sales["Order_Date"], errors="coerce"
)

sales["Delivery_Date"] = pd.to_datetime(
    sales["Delivery_Date"], errors="coerce"
)

sales["Quantity"] = pd.to_numeric(sales["Quantity"], errors="coerce")
sales["Unit_Price"] = pd.to_numeric(sales["Unit_Price"], errors="coerce")
sales["Order_Value"] = pd.to_numeric(sales["Order_Value"], errors="coerce")
sales["Shipping_Cost"] = pd.to_numeric(sales["Shipping_Cost"], errors="coerce")
sales["Coupon_Discount"] = pd.to_numeric(sales["Coupon_Discount"], errors="coerce")
sales["Total_Amount"] = pd.to_numeric(sales["Total_Amount"], errors="coerce")
sales["Rating"] = pd.to_numeric(sales["Rating"], errors="coerce")

products["Original_Price"] = pd.to_numeric(products["Original_Price"], errors="coerce")
products["Discount_Percent"] = pd.to_numeric(products["Discount_Percent"], errors="coerce")
products["Discount_Amount"] = pd.to_numeric(products["Discount_Amount"], errors="coerce")
products["Selling_Price"] = pd.to_numeric(products["Selling_Price"], errors="coerce")
products["Stock_Quantity"] = pd.to_numeric(products["Stock_Quantity"], errors="coerce")
products["Weight_kg"] = pd.to_numeric(products["Weight_kg"], errors="coerce")
products["Avg_Rating"] = pd.to_numeric(products["Avg_Rating"], errors="coerce")
products["Total_Reviews"] = pd.to_numeric(products["Total_Reviews"], errors="coerce")


# ============================================================
# 5. CREATE USEFUL DATE COLUMNS
# ============================================================

sales["Order_Year"] = sales["Order_Date"].dt.year
sales["Order_Month"] = sales["Order_Date"].dt.month
sales["Order_Month_Name"] = sales["Order_Date"].dt.month_name()
sales["Delivery_Days"] = (
    sales["Delivery_Date"] - sales["Order_Date"]
).dt.days


# ============================================================
# 6. MERGE CUSTOMER + PRODUCT INFORMATION
# ============================================================

sales_data = sales.merge(
    customers[
        [
            "Customer_ID",
            "Customer_Name",
            "Gender",
            "Age",
            "Age_Group",
            "Customer_Tier",
        ]
    ],
    on="Customer_ID",
    how="left",
)

sales_data = sales_data.merge(
    products[
        [
            "Product_ID",
            "Product_Name",
            "Category",
            "Brand",
            "Original_Price",
            "Discount_Percent",
            "Selling_Price",
            "Avg_Rating",
        ]
    ],
    on="Product_ID",
    how="left",
)

print("\nMerged sales dataset shape:", sales_data.shape)


# ============================================================
# 7. BASIC BUSINESS KPIs
# ============================================================

print("\n" + "=" * 70)
print("BUSINESS KPIs")
print("=" * 70)

all_orders = sales_data["Order_ID"].nunique()
all_order_value = sales_data["Total_Amount"].sum()
all_quantity = sales_data["Quantity"].sum()

# Revenue from successfully delivered orders
successful_sales = sales_data[sales_data["Order_Status"] == "Delivered"]

delivered_orders = successful_sales["Order_ID"].nunique()
delivered_revenue = successful_sales["Total_Amount"].sum()
delivered_quantity = successful_sales["Quantity"].sum()

average_order_value = successful_sales.groupby("Order_ID")["Total_Amount"].sum().mean()

cancelled_orders = sales_data.loc[
    sales_data["Order_Status"] == "Cancelled", "Order_ID"
].nunique()

returned_orders = sales_data.loc[
    sales_data["Order_Status"] == "Returned", "Order_ID"
].nunique()

processing_orders = sales_data.loc[
    sales_data["Order_Status"] == "Processing", "Order_ID"
].nunique()

shipped_orders = sales_data.loc[
    sales_data["Order_Status"] == "Shipped", "Order_ID"
].nunique()

average_rating = successful_sales["Rating"].mean()
average_delivery_days = successful_sales["Delivery_Days"].mean()

print("Total orders:", all_orders)
print("Total order amount:", round(all_order_value, 2))
print("Total quantity:", int(all_quantity))
print("Delivered orders:", delivered_orders)
print("Delivered revenue:", round(delivered_revenue, 2))
print("Delivered quantity:", int(delivered_quantity))
print("Average Order Value:", round(average_order_value, 2))
print("Cancelled orders:", cancelled_orders)
print("Returned orders:", returned_orders)
print("Processing orders:", processing_orders)
print("Shipped orders:", shipped_orders)
print("Average rating:", round(average_rating, 2))
print("Average delivery days:", round(average_delivery_days, 2))


# ============================================================
# 8. ORDER STATUS ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("1. ORDER STATUS ANALYSIS")
print("=" * 70)

status_report = sales_data.groupby("Order_Status")["Order_ID"].nunique().sort_values(ascending=False)
print(status_report)

plt.figure(figsize=(10, 6))
sns.countplot(data=sales_data, x="Order_Status", order=status_report.index)
plt.title("Order Status Distribution")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()


# ============================================================
# 9. MONTHLY REVENUE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("2. MONTHLY REVENUE ANALYSIS")
print("=" * 70)

monthly_revenue = (
    successful_sales.groupby(sales["Order_Date"].dt.to_period("M"))["Total_Amount"]
    .sum()
    .sort_index()
)

print(monthly_revenue)

plt.figure(figsize=(12, 6))
sns.lineplot(x=monthly_revenue.index.astype(str), y=monthly_revenue.values, marker="o")
plt.title("Monthly Delivered Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# 10. YEARLY REVENUE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("3. YEARLY REVENUE ANALYSIS")
print("=" * 70)

yearly_revenue = successful_sales.groupby("Order_Year")["Total_Amount"].sum().sort_index()
print(yearly_revenue)

plt.figure(figsize=(10, 6))
sns.barplot(x=yearly_revenue.index, y=yearly_revenue.values)
plt.title("Yearly Delivered Revenue")
plt.xlabel("Year")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()


# ============================================================
# 11. CATEGORY REVENUE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("4. CATEGORY REVENUE ANALYSIS")
print("=" * 70)

category_revenue = (
    successful_sales.groupby("Category")["Total_Amount"]
    .sum()
    .sort_values(ascending=False)
)
print(category_revenue)

plt.figure(figsize=(10, 6))
sns.barplot(x=category_revenue.values, y=category_revenue.index)
plt.title("Revenue by Product Category")
plt.xlabel("Revenue")
plt.ylabel("Category")
plt.tight_layout()
plt.show()


# ============================================================
# 12. TOP 10 PRODUCTS BY REVENUE
# ============================================================

print("\n" + "=" * 70)
print("5. TOP 10 PRODUCTS BY REVENUE")
print("=" * 70)

top_products = (
    successful_sales.groupby("Product_Name")["Total_Amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print(top_products)

plt.figure(figsize=(12, 7))
sns.barplot(x=top_products.values, y=top_products.index)
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")
plt.tight_layout()
plt.show()


# ============================================================
# 13. TOP 10 BRANDS BY REVENUE
# ============================================================

print("\n" + "=" * 70)
print("6. TOP 10 BRANDS BY REVENUE")
print("=" * 70)

top_brands = (
    successful_sales.groupby("Brand")["Total_Amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print(top_brands)

plt.figure(figsize=(12, 7))
sns.barplot(x=top_brands.values, y=top_brands.index)
plt.title("Top 10 Brands by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Brand")
plt.tight_layout()
plt.show()


# ============================================================
# 14. TOP 10 CUSTOMERS BY SPENDING
# ============================================================

print("\n" + "=" * 70)
print("7. TOP 10 CUSTOMERS BY SPENDING")
print("=" * 70)

top_customers = (
    successful_sales.groupby(["Customer_ID", "Customer_Name"])["Total_Amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print(top_customers)

plt.figure(figsize=(12, 7))
sns.barplot(x=top_customers.values, y=top_customers.index.get_level_values("Customer_Name"))
plt.title("Top 10 Customers by Delivered Spending")
plt.xlabel("Spending")
plt.ylabel("Customer")
plt.tight_layout()
plt.show()


# ============================================================
# 15. STATE-WISE REVENUE
# ============================================================

print("\n" + "=" * 70)
print("8. STATE-WISE REVENUE")
print("=" * 70)

state_revenue = (
    successful_sales.groupby("State")["Total_Amount"]
    .sum()
    .sort_values(ascending=False)
)
print(state_revenue)

plt.figure(figsize=(12, 8))
sns.barplot(x=state_revenue.values, y=state_revenue.index)
plt.title("Revenue by State")
plt.xlabel("Revenue")
plt.ylabel("State")
plt.tight_layout()
plt.show()


# ============================================================
# 16. PAYMENT MODE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("9. PAYMENT MODE ANALYSIS")
print("=" * 70)

payment_report = (
    successful_sales.groupby("Payment_Mode")["Total_Amount"]
    .sum()
    .sort_values(ascending=False)
)
print(payment_report)

plt.figure(figsize=(10, 6))
sns.barplot(x=payment_report.index, y=payment_report.values)
plt.title("Delivered Revenue by Payment Mode")
plt.xlabel("Payment Mode")
plt.ylabel("Revenue")
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()


# ============================================================
# 17. CUSTOMER TIER ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("10. CUSTOMER TIER ANALYSIS")
print("=" * 70)

tier_revenue = (
    successful_sales.groupby("Customer_Tier")["Total_Amount"]
    .sum()
    .sort_values(ascending=False)
)
print(tier_revenue)

plt.figure(figsize=(10, 6))
sns.barplot(x=tier_revenue.index, y=tier_revenue.values)
plt.title("Revenue by Customer Tier")
plt.xlabel("Customer Tier")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()


# ============================================================
# 18. GENDER-WISE REVENUE
# ============================================================

print("\n" + "=" * 70)
print("11. GENDER-WISE REVENUE")
print("=" * 70)

gender_revenue = (
    successful_sales.groupby("Gender")["Total_Amount"]
    .sum()
    .sort_values(ascending=False)
)
print(gender_revenue)

plt.figure(figsize=(8, 5))
sns.barplot(x=gender_revenue.index, y=gender_revenue.values)
plt.title("Revenue by Gender")
plt.xlabel("Gender")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()


# ============================================================
# 19. AGE GROUP ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("12. AGE GROUP ANALYSIS")
print("=" * 70)

age_group_revenue = (
    successful_sales.groupby("Customer_Age_Group")["Total_Amount"]
    .sum()
    .sort_values(ascending=False)
)
print(age_group_revenue)

plt.figure(figsize=(10, 6))
sns.barplot(x=age_group_revenue.index, y=age_group_revenue.values)
plt.title("Revenue by Customer Age Group")
plt.xlabel("Age Group")
plt.ylabel("Revenue")
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()


# ============================================================
# 20. QUANTITY SOLD BY CATEGORY
# ============================================================

print("\n" + "=" * 70)
print("13. QUANTITY SOLD BY CATEGORY")
print("=" * 70)

category_quantity = (
    successful_sales.groupby("Category")["Quantity"]
    .sum()
    .sort_values(ascending=False)
)
print(category_quantity)

plt.figure(figsize=(10, 6))
sns.barplot(x=category_quantity.values, y=category_quantity.index)
plt.title("Quantity Sold by Category")
plt.xlabel("Quantity")
plt.ylabel("Category")
plt.tight_layout()
plt.show()


# ============================================================
# 21. DISCOUNT VS REVENUE
# ============================================================

print("\n" + "=" * 70)
print("14. DISCOUNT VS ORDER AMOUNT")
print("=" * 70)

print("Average coupon discount:", round(successful_sales["Coupon_Discount"].mean(), 2))
print("Average total amount:", round(successful_sales["Total_Amount"].mean(), 2))

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=successful_sales,
    x="Coupon_Discount",
    y="Total_Amount",
    alpha=0.45,
)
plt.title("Coupon Discount vs Delivered Order Amount")
plt.xlabel("Coupon Discount")
plt.ylabel("Total Amount")
plt.tight_layout()
plt.show()


# ============================================================
# 22. DELIVERY TIME ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("15. DELIVERY TIME ANALYSIS")
print("=" * 70)

print("Minimum delivery days:", successful_sales["Delivery_Days"].min())
print("Maximum delivery days:", successful_sales["Delivery_Days"].max())
print("Average delivery days:", round(successful_sales["Delivery_Days"].mean(), 2))
print("Median delivery days:", successful_sales["Delivery_Days"].median())

plt.figure(figsize=(10, 6))
sns.histplot(successful_sales["Delivery_Days"].dropna(), bins=10, kde=True)
plt.title("Delivery Time Distribution")
plt.xlabel("Delivery Days")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.show()


# ============================================================
# 23. CUSTOMER RATING ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("16. CUSTOMER RATING ANALYSIS")
print("=" * 70)

rating_report = successful_sales["Rating"].value_counts().sort_index()
print(rating_report)

plt.figure(figsize=(10, 6))
sns.countplot(
    data=successful_sales,
    x="Rating",
    order=sorted(successful_sales["Rating"].dropna().unique()),
)
plt.title("Customer Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of Ratings")
plt.tight_layout()
plt.show()


# ============================================================
# 24. MONTHLY ORDER COUNT
# ============================================================

print("\n" + "=" * 70)
print("17. MONTHLY ORDER COUNT")
print("=" * 70)

monthly_orders = (
    successful_sales.groupby(sales["Order_Date"].dt.to_period("M"))["Order_ID"]
    .nunique()
    .sort_index()
)
print(monthly_orders)

plt.figure(figsize=(12, 6))
sns.lineplot(x=monthly_orders.index.astype(str), y=monthly_orders.values, marker="o")
plt.title("Monthly Delivered Order Count")
plt.xlabel("Month")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# 25. CATEGORY VS CUSTOMER TIER
# ============================================================

print("\n" + "=" * 70)
print("18. CATEGORY VS CUSTOMER TIER")
print("=" * 70)

category_tier = pd.pivot_table(
    successful_sales,
    values="Total_Amount",
    index="Category",
    columns="Customer_Tier",
    aggfunc="sum",
    fill_value=0,
)

print(category_tier)

plt.figure(figsize=(12, 7))
sns.heatmap(category_tier, annot=True, fmt=".0f")
plt.title("Category Revenue by Customer Tier")
plt.xlabel("Customer Tier")
plt.ylabel("Category")
plt.tight_layout()
plt.show()


# ============================================================
# 26. CORRELATION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("19. CORRELATION ANALYSIS")
print("=" * 70)

correlation_data = successful_sales[
    [
        "Quantity",
        "Unit_Price",
        "Order_Value",
        "Shipping_Cost",
        "Coupon_Discount",
        "Total_Amount",
        "Rating",
        "Delivery_Days",
    ]
]

correlation_matrix = correlation_data.corr(numeric_only=True)
print(correlation_matrix.round(2))

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Sales Dataset Correlation Heatmap")
plt.tight_layout()
plt.show()


# ============================================================
# 27. PRODUCT PERFORMANCE REPORT
# ============================================================

print("\n" + "=" * 70)
print("20. PRODUCT PERFORMANCE REPORT")
print("=" * 70)

product_report = (
    successful_sales.groupby(["Product_ID", "Product_Name", "Category"])
    .agg(
        Orders=("Order_ID", "nunique"),
        Quantity=("Quantity", "sum"),
        Revenue=("Total_Amount", "sum"),
        Average_Rating=("Rating", "mean"),
    )
    .sort_values("Revenue", ascending=False)
)

print(product_report.head(20).round(2))


# ============================================================
# 28. CUSTOMER PERFORMANCE REPORT
# ============================================================

print("\n" + "=" * 70)
print("21. CUSTOMER PERFORMANCE REPORT")
print("=" * 70)

customer_report = (
    successful_sales.groupby(["Customer_ID", "Customer_Name", "Customer_Tier"])
    .agg(
        Orders=("Order_ID", "nunique"),
        Quantity=("Quantity", "sum"),
        Revenue=("Total_Amount", "sum"),
        Average_Rating=("Rating", "mean"),
    )
    .sort_values("Revenue", ascending=False)
)

print(customer_report.head(20).round(2))


# ============================================================
# 29. SIMPLE BUSINESS INSIGHTS
# ============================================================

print("\n" + "=" * 70)
print("BUSINESS INSIGHTS")
print("=" * 70)

if len(monthly_revenue) > 0:
    best_month = monthly_revenue.idxmax()
    best_month_value = monthly_revenue.max()
    print(
        "1. Highest revenue month:",
        best_month,
        "with revenue",
        round(best_month_value, 2),
    )

if len(category_revenue) > 0:
    best_category = category_revenue.idxmax()
    print(
        "2. Highest revenue category:",
        best_category,
        "with revenue",
        round(category_revenue.max(), 2),
    )

if len(top_brands) > 0:
    best_brand = top_brands.index[0]
    print(
        "3. Highest revenue brand in top-10 report:",
        best_brand,
        "with revenue",
        round(top_brands.iloc[0], 2),
    )

if len(state_revenue) > 0:
    best_state = state_revenue.index[0]
    print(
        "4. Highest revenue state:",
        best_state,
        "with revenue",
        round(state_revenue.iloc[0], 2),
    )

if len(tier_revenue) > 0:
    best_tier = tier_revenue.index[0]
    print(
        "5. Highest revenue customer tier:",
        best_tier,
        "with revenue",
        round(tier_revenue.iloc[0], 2),
    )

print(
    "6. Delivered order share:",
    round((delivered_orders / all_orders) * 100, 2),
    "%",
)

print(
    "7. Cancelled order share:",
    round((cancelled_orders / all_orders) * 100, 2),
    "%",
)

print(
    "8. Returned order share:",
    round((returned_orders / all_orders) * 100, 2),
    "%",
)


# ============================================================
# 30. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL PROJECT SUMMARY")
print("=" * 70)

print("Customers:", customers.shape[0])
print("Products:", products.shape[0])
print("Orders:", all_orders)
print("Delivered Revenue:", round(delivered_revenue, 2))
print("Average Order Value:", round(average_order_value, 2))
print("Average Rating:", round(average_rating, 2))
print("Average Delivery Days:", round(average_delivery_days, 2))
print("Cancelled Orders:", cancelled_orders)
print("Returned Orders:", returned_orders)
print("\nPROJECT COMPLETED")
print("=" * 70)
