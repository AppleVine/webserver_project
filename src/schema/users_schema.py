from app import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "password", "name", "lab_permission")

user_schema = UserSchema()
users_schema = UserSchema(many=True)


