from app import ma

class ResultSchema(ma.Schema):
    class Meta:
        fields = ('id', 'product_code', 'staff_id', 'specific_gravity', 'potential_hydrogen', 'reserve_alkalinity', 'water_content', 'test_time_date')


result_schema = ResultSchema()
results_schema = ResultSchema(many=True)



class UserResultSchema(ma.Schema):
    class Meta:
        fields = ('id', 'staff_name', 'staff_id', 'product_code', 'product_code', 'specific_gravity', 'potential_hydrogen', 'reserve_alkalinity', 'water_content', 'test_time_date')


userresult_schema = UserResultSchema()
userresults_schema = UserResultSchema(many=True)


