# from pymodm import MongoModel, fields
# from pymongo.write_concern import WriteConcern

# class User(MongoModel):
# 	email = fields.EmailField(primary_key=True)
# 	first_name = fields.CharField()
# 	last_name = fields.CharField()
    
# 	class Meta:
#         connection_alias = 'my-atlas-app'
#         write_concern = WriteConcern(j=True)