import os
from datetime import datetime, timedelta

from Packages.SqlDB import SqlDB
from Packages.UserPackage.Login import LoginUser
from Packages.UserPackage.NewUser import NewUser
from Packages.modules import ChnageToDict


# # ......................User Login
class User(LoginUser, NewUser):
    def __init__(self, Id=0, email='', name='', password='', phone='', profileImage=''):
        super().__init__(filename=os.getenv('DB_FILE'))
        self._id = Id
        self._name = name
        self._password = password
        self._email = email
        self._phone = phone
        self._profileImage = profileImage
        print(email, password)

    def GetUserData(self):
        return ChnageToDict(name=self._name, email=self._email, phone=self._phone,
                            profileImage=self._profileImage)

    def Login(self, bcrypt):
        super().SetValue(email=self._email, password=self._password)
        return super().Verify(bcrypt=bcrypt)

    def SaveUser(self, bcrypt):
        # return  "SAVING"
        print("saving")
        super().SetData(self._name, self._email, self._password, self._phone)
        res = super().CheckValidationError()
        # print(res)
        if res:
            print("res exist")
            return res
        res = super().SaveUser(bcrypt)
        print(res)
        if res:
            return False
        return True

    # # ........................Fetching data for Profile
    def FetchData(self):

        data = super().GetDataAdvance(table='users', FindKey={"id": self._id})
        print(data)
        if not data:
            print({"error": {"text": f"fail to update"}})
            return {"error": {"text": f"fail to update"}}
        self._id = data[0]
        self._name = data[1]
        self._email = data[2]
        self._phone = data[3]
        self._profileImage = data[4]
        return ChnageToDict(name=data[1], email=data[2], phone=data[3], profileImage=data[4], plan_id= data[5],
                            plan=data[6], per=data[7], days=data[8], start=data[9], expire=data[10])
    def GetPlanId(self):
        data = super().GetDataAdvance(table='users', FindKey={"id": self._id}, get=['plan_id'])
        print(data)
        return ChnageToDict(plan_id=data[0])
    # # ......................User Profile Update
    def UpdateData(self, username="", phone="", profileImage=""):
        print("update")
        # data = db.getData(f"""Select phone from user where email='{email}'""")[0]
        data = super().GetDataAdvance(table='user', FindKey={"phone": phone, 'id !': self._id}, get=['phone'])
        print(data)
        if data:
            return "phone number exist"

        sql = f"""update user set username='{username}', phone='{phone}', profile_image='{profileImage}',
               DOU=(CURRENT_TIMESTAMP) where id='{self._id}'"""
        if profileImage == "":
            sql = f"""update user set username='{username}', phone='{phone}', DOU=(CURRENT_TIMESTAMP)
                    where id='{self._id}'"""
        if super().UpdateData(sql):
            self._name = username
            self._phone = phone
            return ""
        return "something went wrong"

# # ...........................Updating Plan
    def UpdatePlan(self, plantype):
        planDays = super().getData(f"select days from plans where id = {plantype}")[0]
        # print(planDays)
        today = datetime.now().date()
        expire = today + timedelta(planDays[0])
        if super().UpdateDataAdvance(table='user', FindKey={"id": self._id}, plan_id=plantype,
                                     start_date=str(today), exp_date=str(expire), DOU=True):
            return ""
        return "something went wrong"

    def ForgetPassword(self):
        user = super().GetDataAdvance(table='user', FindKey={"email": self._email, "phone": self._phone}, get=['id'])
        print(user)
        if not user:
            return False
        return user[0]

    def NewPassword(self,bcrypt, newPassword=""):
        hash = bcrypt.generate_password_hash(newPassword).decode('utf8')
        if super().UpdateDataAdvance(table='user', FindKey={"id": self._id }, password=hash):
            return True
        return False


    def NextUser(self, great):
        print(great)
        middle = "<"
        if int(great) == 1:
            middle = ">"
        res = super().getOneData(f"select * from users where id {middle} {self._id}")
        print(res)
        if res:
            return True
        return False
