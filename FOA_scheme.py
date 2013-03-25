import datetime
from schematics.models import Model
from schematics.types import StringType, IntType, UUIDType
from schematics.serialize import to_python, for_jsonschema, from_jsonschema
from schematics.types.compound import (ListType,ModelType)

class Userinfo(Model):
    _uid = UUIDType(auto_fill=True)
    uid = StringType(max_length=40)
    passwd = StringType(max_length=32)
    regdate = IntType(min_value=1900, max_value=datetime.datetime.now().year)
    level = IntType(min_value=0, max_value=100)
    exp = IntType(min_value=0, max_value=99999999)
    money = IntType(min_value=0, max_value=9999999999)
    cash = IntType(min_value=0, max_value=9999999999)
    
    
'''
user = Userinfo( uid='taejun',
              passwd='md5_string',
              regdate=19750505, 
              level=5,
              exp=2000,
              money=20000,
              cash=0)

user_schema = for_jsonschema(user)
user_data = to_python(user)

print user
print '\n'
print user_schema
print '\n'
print user_data
'''
