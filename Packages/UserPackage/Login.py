from Packages.SqlDB import SqlDB


class LoginUser(SqlDB):
    _email = ''
    _password = ''

    def SetValue(self, email, password):
        self._email = email
        self._password = password

    # Verifying email and password
    def Verify(self, bcrypt):
        try:
            # sql = f"select id,email,password,username from user where email='{self._email}'"
            data = list(super().GetDataAdvance(table='user', FindKey={"email": self._email},
                                               get=['id', 'email', 'password', 'username', "exp_date"]))
            print(data)
            if not data:
                return []
            password_hash = str(data[2])

            # comparing hash password
            if bcrypt.check_password_hash(password_hash, self._password):
                print(bcrypt.check_password_hash(password_hash, self._password))
                data.pop(2)
                print(data)
                return data
            return []
        except Exception as e:
            print(e)
            return []