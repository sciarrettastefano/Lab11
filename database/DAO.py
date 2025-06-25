from database.DB_connect import DBConnect
from model.edge import Edge
from model.product import Product


class DAO():

    @staticmethod
    def getAllColors():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct Product_color as pc
                    from go_products"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["pc"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct YEAR(gds.Date) as anno
                    from go_daily_sales gds"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllProductsByColor(color):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select gp.*
                    from go_products gp
                    where gp.Product_color = %s"""

        cursor.execute(query, (color, ))

        for row in cursor:
            result.append(Product(**row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllEdges(color, year, idMapProducts):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT gds1.Product_number as id1, gds2.Product_number as id2, count(distinct(gds1.Date)) as peso
                    from go_daily_sales gds1, go_daily_sales gds2, go_products gp1, go_products gp2
                    where gds1.Product_number = gp1.Product_number
                    and gp1.Product_color = %s
                    and gds2.Product_number = gp2.Product_number
                    and gp2.Product_color = gp1.Product_color
                    and gds1.Product_number < gds2.Product_number
                    and gds1.`Date` = gds2.`Date` 
                    and YEAR(gds1.Date) = YEAR(gds2.Date)
                    and YEAR(gds2.Date) = %s
                    and gds1.Retailer_code = gds2.Retailer_code
                    group by id1, id2"""

        cursor.execute(query, (color, year, ))

        for row in cursor:
            result.append(Edge(idMapProducts[row["id1"]], idMapProducts[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return result

