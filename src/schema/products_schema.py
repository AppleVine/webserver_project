from app import ma

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'product_name', 'product_description', 'product_cost')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

