from database.DB_connect import DBConnect
from model.product import Product
from model.sale import Sale


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllProducts():
        conn=DBConnect.get_connection()
        result=[]
        query="Select * from go_products"
        cur=conn.cursor(dictionary=True)
        cur.execute(query,)
        for row in cur:
            result.append(Product(**row))
        cur.close()
        conn.close()
        return result

    @staticmethod
    def getAllSales():
        conn=DBConnect.get_connection()
        result=[]
        query=("Select go.Retailer_code as retailer_code, go.Product_number as number, go.Date as Date from go_daily_sales go")
        curr=conn.cursor(dictionary=True)
        curr.execute(query)
        for row in curr:
            sale=Sale(row["retailer_code"], row["number"], row["Date"])
            result.append(sale)
        curr.close()
        conn.close()
        return result

    @staticmethod
    def getSalesYear(year,products):
        conn=DBConnect.get_connection()
        result={}
        query=("Select go.Retailer_code as retailer_code, go.Product_number as p1, go.Date as Date from go_daily_sales go where YEAR(go.Date)=%s")
        curr=conn.cursor(dictionary=True)
        curr.execute(query,(year,))
        for row in curr:
            sale=Sale(row["retailer_code"], row["p1"], row["Date"])
            if sale.product_number in products:
                if sale.retailer_code in result:
                    result[sale.retailer_code].append(sale)
                else:
                    result[sale.retailer_code]=[sale]
        curr.close()
        conn.close()
        return result

    @staticmethod
    def getWeight(p1,p2,year):
        conn=DBConnect.get_connection()
        result=0
        query=("select count(distinct go1.Date) from go_daily_sales go1, go_daily_sales go2 "
               "where go1.Retailer_code=go2.Retailer_code and go1.Product_number=%s and go2.Product_number=%s and go1.Date=go2.Date and YEAR(go1.Date)=%s")
        cursor=conn.cursor(dictionary=True)
        cursor.execute(query, (p1,p2,year,))
        for row in cursor:
            result=row['count(distinct go1.Date)']
        cursor.close()
        conn.close()
        return result