import mysql.connector
import time
import os

#
# print("-------------------------------")
# print("     Dieses Skript wurde")
# print("            von")
# print("        Maximilian1021 ")
# print("         entworfen")
# print("-------------------------------")



mydb = mysql.connector.connect(
    host="localhost",
    user="YourUser",
    password="YourPassword",
    database="YourDatabase"
)
mycursor = mydb.cursor()



stmt = "SHOW TABLES LIKE 'Temperatur'"
mycursor.execute(stmt)
result = mycursor.fetchone()
if result:
    # there is a table named "tableName"
    print("[PiTemp] Skript gestartet")
else:
    print("[PiTemp] Skript gestartet")
    mycursor.execute("CREATE TABLE Temperatur(`id` INT NOT NULL AUTO_INCREMENT,`time` BIGINT NULL DEFAULT NULL,`temperature` TEXT NULL,PRIMARY KEY (`id`)) COLLATE = 'latin1_swedish_ci';")
    print("[PiTemp] Database created")
    # there are no tables named "tableName"


def current_time_in_mili():
    return round(time.time() * 1000)


def temp_of_raspberry():
    # cpu_temp = os.popen("vcgencmd measure_temp").readline()
    # return cpu_temp.replace("temp=", "")
    cpu_temp = open("/sys/class/thermal/thermal_zone0/temp", "r").readline()

    math_cpu_temp = (int(cpu_temp) / 1000)
    return math_cpu_temp


while True:
    mycursor = mydb.cursor()

    sql = "INSERT INTO Temperatur (time, temperature) VALUES (%s, %s)"

    val = (current_time_in_mili(), temp_of_raspberry())
    mycursor.execute(sql, val)
    mydb.commit()
    print(
        "[PiTemp] Werte an Database übermittelt: ID: ", mycursor.lastrowid, " - Zeit ", current_time_in_mili(), " Temperatur ",
        temp_of_raspberry(), ".")
    time.sleep(300)

