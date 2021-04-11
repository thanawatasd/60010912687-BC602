import mysql.connector

def insertmysql(**kwargs):
    mydb = mysql.connector.connect(
        host= "localhost",
        user="root",
        password="",
        database="temp_db"
    )

    mycursor = mydb.cursor()
    sql = "INSERT INTO temp_tb (id_human, name, date, time, temp) VALUES (%s, %s, %s, %s, %s)"
    val = (kwargs["id_human"], kwargs["name"], kwargs["date"], kwargs["time"], kwargs["temp"])

    mycursor.execute(sql, val)
    mydb.commit()
    return True


# insertmysql(id_human="555",name="11",date="11",time="11",temp="34")
