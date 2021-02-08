import sqlite3


class SqlDB:
    def __init__(self, filename):
        try:
            self._mydb = sqlite3.connect(filename)
            print("connect")
            self._mydb_cursor = self._mydb.cursor()
        except Exception as e:
            print(e)

    def insertData(self, sql):
        try:
            self._mydb_cursor.execute(sql)
            self._mydb.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def UpdateData(self, sql):
        try:
            print(sql)
            self._mydb_cursor.execute(sql)
            self._mydb.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def getData(self, sql):
        try:
            print(sql)
            self._mydb_cursor.execute(sql)
            data = self._mydb_cursor.fetchall()
            # print(data)
            if data:
                return data
            return []
        except Exception as e:
            print("Exception Occurs At Getting Data :",e)
            return []

    def getOneData(self, sql):
        try:
            print(sql)
            self._mydb_cursor.execute(sql)
            data = self._mydb_cursor.fetchone()
            # print(data)
            if data:
                return data
            return []
        except Exception as e:
            print(e)
            return []

    def Close(self):
        self._mydb.close()

    # .................................AdvanceDB

    def InsertDataAdvance(self, table, **kwargs):
        try:
            SetData = ""
            Data = ""
            for key, value in kwargs.items():
                if key == 'DOU' or key == 'DOC':
                    SetData += key
                    Data += '(CURRENT_TIMESTAMP)'
                elif str(value).isnumeric():
                    SetData += f'{key}'
                    Data += f"{value}"
                else:
                    SetData += f'{key}'
                    Data += f"'{value}'"
                if key != list(kwargs.keys())[-1]:
                    SetData += ', '
                    Data += ', '
            print(kwargs)
            sql = f"Insert into {table} ({SetData}) Values({Data})"
            print(sql)
            self._mydb_cursor.execute(sql)
            self._mydb.commit()
            return True
        except IndexError as e:
            print(e)
            return False
        except Exception as e:
            print(e)
            return False

    def GetDataAdvance(self, table='', connection={}, FindKey={}, get=[] , order=[]):
        try:
            getData = "*"
            if get:
                getData = ", ".join([str(i) for i in get])
            connectData = ""
            for join, key in connection.items():
                connectData += f" join {join} on {key} "

            WhereData = " "
            if FindKey.keys():
                WhereData = "where "
                f = False
                for key, value in FindKey.items():
                    if key == "OR" and value:
                        f = True
                        WhereData += ' or '
                        continue
                    if key != list(FindKey.keys())[0] and not f:
                        WhereData += ' and '

                    WhereData += f"{key}= {value}" if str(value).isdecimal() else f"{key}= '{value}'"
                    f = False
            orderSql = ""
            if order:
                orderSql = f"order by {order[0]} {order[1]}"

            sql = f"""select {getData} from {table} {connectData} {WhereData} {orderSql}"""
            print(sql)
            self._mydb_cursor.execute(sql)
            data = list(self._mydb_cursor.fetchall())
            if len(data) == 1:
                return list(data[0])
            return (data)
        except IndexError as e:
            print(e)
            return False

        except Exception as e:
            print(e)
            return False

    def UpdateDataAdvance(self, table, FindKey, **kwargs):
        try:
            SetData = ""
            for key, value in kwargs.items():
                if key == 'DOU':
                    SetData += 'DOU = (CURRENT_TIMESTAMP)'
                else:
                    SetData += f"{key} = {value}" if value.isdecimal() else f" {key} = '{value}'"
                if key != list(kwargs.keys())[-1]:
                    SetData += ', '

            WhereData = ""
            f = False
            for key, value in FindKey.items():
                if key == "OR" and value:
                    f = True
                    WhereData += ' or '
                    continue
                if key != list(FindKey.keys())[0] and not f:
                    WhereData += ' and '

                WhereData += f"{key} = {value}" if str(value).isdecimal() else f"{key} = '{value}'"
                f = False

            print(kwargs)
            sql = f"Update {table} set {SetData} where {WhereData}"
            print(sql)
            self._mydb_cursor.execute(sql)
            self._mydb.commit()
            return True
        except IndexError as e:
            print(e)
            return False
        except Exception as e:
            print(e)
            return False

    def DeleteDataAdvance(self, table, FindKey):
        try:
            WhereData = ""
            f = False
            for key, value in FindKey.items():
                if key == "OR" and value:
                    f = True
                    WhereData += ' or '
                    continue
                if key != list(FindKey.keys())[0] and not f:
                    WhereData += ' and '

                WhereData += f"{key} = {value}" if str(value).isdecimal() else f"{key} = '{value}'"
                f = False

            print(FindKey)
            sql = f"Delete from {table} where {WhereData}"
            print(sql)
            self._mydb_cursor.execute(sql)
            self._mydb.commit()
            return True
        except IndexError as e:
            print(e)
            return False
        except Exception as e:
            print(e)
            return False
    def __del__(self):
        self._mydb.close()
