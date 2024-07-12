from database.DAO import DAO

DAO = DAO()
products=DAO.getAllProducts()
print(len(products))
sales=DAO.getAllSales()
print(len(sales))
for product in products:
    for product2 in products:
        weight=DAO.getWeight(product.Product_number,product2.Product_number,2018)
        if weight>0:
            print(f"{product} - {product2}: {weight}")
