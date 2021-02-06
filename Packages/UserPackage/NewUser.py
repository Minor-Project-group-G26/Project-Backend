# ............... New User Class
from Packages.SqlDB import SqlDB


class NewUser(SqlDB):
    _name = ''
    _email = ''
    _password = ''
    _phone = ''
    __hash_pass = ''

    def SetData(self, name, email, password, phone):
        self._name = name
        self._email = email
        self._password = password
        self._phone = phone
        print(self)

    #  Checking Email and Phone Number is valid or not
    def CheckValidationError(self):
        try:
            data = super().GetDataAdvance(table="user", FindKey={"email": self._email, "OR": True,
                                                                 "phone": self._phone}, get=["email", "phone"])
            print(data)
            if not data:
                return []
            for email, phone in [data]:
                print(email, phone)
                if str(email) == str(self._email) and str(phone) == str(self._phone):
                    return {'errors': {"email": "already Exist", "phone": "already Exist"}}
                elif str(email) == str(self._email):
                    return {'errors': {"email": "already Exist"}}
                else:
                    return {'errors': {"phone": "already Exist"}}
        except IndexError as e:
            print(e)
            return "something went wrong"
        except TypeError as e:
            print(e)
            return "something went wrong"

    # Committing new User data in user table
    def SaveUser(self, bcrypt):
        self.__hash_pass = bcrypt.generate_password_hash(self._password).decode('utf8')
        # try:
        if super().InsertDataAdvance(table='user', username=self._name, email=self._email,
                                        password=self.__hash_pass, phone=self._phone, DOC=True, DOU=True):
            data = super().GetDataAdvance(table='user', FindKey={"email": self._email, "phone": self._phone},
                                              get=['id', 'email', 'username'])

                # print(data)
                # db.insertData(f"""CREATE TABLE {data[0]} (
                #     "id"	INTEGER,
                #     "movie_id"	INTEGER,
                #     "DOV"	Timestamp,
                #     PRIMARY KEY("id" AUTOINCREMENT)
                #     );""")
            return data
        return []
        # except Exception as e:
        #     print(e)
        #     return []