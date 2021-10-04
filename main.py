import mysql.connector
import time


print("-------------------------------")
print("     Dieses Skript wurde")
print("            von")
print("        Maximilian1021 ")
print("         entworfen")
print("-------------------------------")


# mydb = mysql.connector.connect(
#     host="localhost",
#     user="YourUser",
#     password="YourPassword",
#     database="YourDatabase"
# )


class GetConfig:
    def __init__(self, config: str) -> None:
        with open(config) as f:
            for i in f.readlines():
                if i.startswith("host"):
                    self.host = i.replace("host =", "").strip()
                elif i.startswith("user"):
                    self.user = i.replace("user =", "").strip()
                elif i.startswith("password"):
                    self.password = i.replace("password =", "").strip()
                elif i.startswith("database"):
                    self.database = i.replace("database =", "").strip()


configDB = GetConfig("config.txt")
# print(config.host)

mydb = mysql.connector.connect(
    host=configDB.host,
    user=configDB.user,
    password=configDB.password,
    database=configDB.database
)

mycursor = mydb.cursor()

# Hier wird überprüft ob die Tabelle in der Datenbank bereits angelegt wurde
stmt = "SHOW TABLES LIKE 'Temperatur'"
mycursor.execute(stmt)
result = mycursor.fetchone()
if result:
    # ist bereits eine Tabelle vorhanden wenn ja tu dies
    print("[PiTemp] Skript gestartet")
else:
    # ist noch keine
    print("[PiTemp] Skript gestartet")
    mycursor.execute(
        "CREATE TABLE Temperatur(`id` INT NOT NULL AUTO_INCREMENT,`time` BIGINT NULL DEFAULT NULL,`temperature` TEXT "
        "NULL,PRIMARY KEY (`id`)) COLLATE = 'latin1_swedish_ci';")
    print("[PiTemp] Database created")


def current_time_in_mili():
    return round(time.time() * 1000)


def temp_of_raspberry():
    # cpu_temp = os.popen("vcgencmd measure_temp").readline()
    # return cpu_temp.replace("temp=", "")
    cpu_temp = open("/sys/class/thermal/thermal_zone0/temp", "r").readline()

    math_cpu_temp = (int(cpu_temp) / 1000)
    return math_cpu_temp


while True:

    try:
        mycursor = mydb.cursor()

        sql = "INSERT INTO Temperatur (time, temperature) VALUES (%s, %s)"

        val = (current_time_in_mili(), temp_of_raspberry())
        mycursor.execute(sql, val)
        mydb.commit()
        print(
            "[PiTemp] Werte an Database übermittelt: ID: ", mycursor.lastrowid, " - Zeit ", current_time_in_mili(),
            " Temperatur ",
            temp_of_raspberry(), ".")

        time.sleep(300)
    except Exception as e:
        print(e)
        mydb.close()
        break
