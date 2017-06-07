class DbClass:
    #Constructor - zaken die nodig zijn bij de start
    def __init__(self):
        import mysql.connector as connector

        self.__dsn = {"host": "localhost", "user": "docam-admin", "passwd": "docampwd", "db": "docam"}
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()

    # def getProducts(self):
    #     query = "SELECT product_id, product_name, product_img FROM tbl_products"
    #     # query uitvoeren
    #     self.__cursor.execute(query)
    #
    #     # resultaat opvragen
    #     result = self.__cursor.fetchall()
    #
    #     # cursor sluiten
    #     self.__cursor.close()
    #
    #     return result
    #
    # def getProductByName(self, productName):
    #     query = "SELECT product_id, product_name, product_oms, product_img, product_price FROM tbl_products WHERE = '" + productName + "'"
    #     self.__cursor.execute(query)
    #     result = self.__cursor.fetchone()
    #     self.__cursor.close()
    #     return result
