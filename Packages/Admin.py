import os

from Packages.SqlDB import SqlDB
from Packages.modules import ChnageToDict, fileRemove


class Admin(SqlDB):

    def __init__(self, Id=0, email="", password="", name="", phone=""):
        super().__init__(filename=os.getenv('DB_FILE'))
        self._id = Id
        self._email = email
        self._password = password
        self._hash_pass = ""
        self._name = name
        self._phone = phone
        # print(self._email, self._password)

    def Login(self, bcrypt):
        try:
            data = super().GetDataAdvance(table='admin', FindKey={"email": self._email},
                                     get=['id', 'email', 'password', 'username'])
            if not data:
                return []
            password_hash = str(data[2])
            if bcrypt.check_password_hash(password_hash, self._password):
                print("Admin.py 27: ",bcrypt.check_password_hash(password_hash, self._password))
                data.pop(2)
                print("Admin.py 29: ",data)
                return data
            return []
        except Exception as e:
            print(e)
            return []

    def SaveUser(self, bcrypt):
        self.__hash_pass = bcrypt.generate_password_hash(self._password).decode('utf8')
        try:
            if super().InsertDataAdvance(table='admin', username=self._name, email=self._email,
                                         password=self.__hash_pass, phone=self._phone, DOC=True, DOU=True):
                data = super().GetDataAdvance(table='admin', FindKey={"email": self._email, "phone": self._phone},
                                              get=['id', 'email', 'username'])
                return data
            return []
        except Exception as e:
            print(e)
            return []

    def ForgetPassword(self):
        user = super().GetDataAdvance(table='admin', FindKey={"email": self._email, "phone": self._phone}, get=['id'])
        print(user)
        if not user:
            return False
        return user[0]

    def NewPassword(self,bcrypt, newPassword=""):
        hash = bcrypt.generate_password_hash(newPassword).decode('utf8')
        if super().UpdateDataAdvance(table='admin', FindKey={"id": self._id }, password=hash):
            return True
        return False

    def AllUsers(self, Id, great):
        print(great)
        sql = f"select * from users where id >={Id} limit 5"
        if int(great) ==0:
            sql = f"select * from users where id <={Id} order by id desc limit 5"
        users = list(super().getData(sql=sql))
        users_dict_list= list()
        users.sort(key= lambda x: x[0])
        print(users)

        for user in users:
            print(user)

            users_dict_list.append(ChnageToDict(id=user[0], name=user[1], email=user[2], phone=user[3],
                                                profileImage=user[4], plan=user[5], start_date=user[8],
                                                expire_date=user[9], doc=user[10], dou=user[11]))
        print(users_dict_list)
        return (users_dict_list)

    def DeleteUser(self, user_id):

        res = super().DeleteDataAdvance(table='user', FindKey={"id": user_id})
        print(res)
        return res


    def __del__(self):
        super().Close()