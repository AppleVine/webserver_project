from app import ma

class ResultSchema(ma.Schema):
    class Meta:
        fields = ('id', 'product_code', 'staff_id', 'specific_gravity', 'pH', 'reserve_alkalinity', 'water_content', 'test_time_date')


result_schema = ResultSchema()
results_schema = ResultSchema(many=True)

