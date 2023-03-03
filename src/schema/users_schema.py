from app import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password', 'name', 'role')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


