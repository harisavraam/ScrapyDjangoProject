import pymysql

def dataReader():
    try:
        connection = pymysql.connect(host = 'localhost',
                               user = 'root',
                               passwd = '',
                               db = 'skroutz_4')
        sql_select_Query = "SELECT productSkroutzUrl FROM skroutz_4.api_allmyproducts;"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        record_list = []
        for record in records:
            record_list.append(record[0])
        # print(record_list)
        return record_list
        sql_truncate_query = "TRUNCATE TABLE api_datamaintable"
        cursor.execute(sql_truncate_query)
    finally:
        connection.close()
        cursor.close()

