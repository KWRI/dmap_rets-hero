import rets.client
from rets.client import RetsClient

# client = RetsClient(
#     login_url='https://rets.nlar.mlxmatrix.com/Rets/login.ashx',
#     username='SMARTERAGENTMOBILE',
#     password='#SMA@22bile',
    # Ensure that you are using the right auth_type for this particular MLS
    # auth_type='basic',
    # Alternatively authenticate using user agent password
    # user_agent='rets-python/0.3',
    # user_agent_password=''
    # )

# print(dir(client))
# print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
# print(vars(client))
# print(client.__dict__)
# print(client.metadata)

# Get list of resources
# print(client.resources[0])
# print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
# Prints the resource chosen
# resource = client.get_resource('Property')
# print(resource)

# Obtains the key field
# key_field = resource.key_field
# print(key_field)
# 'LIST_1'


# print(client._resources_from_metadata)
# resource_class = resource.get_class('Property')

# resource_class.has_key_index
# True

# photo_object_type = resource.get_object_type('HiRes')

# photo_object_type.mime_type
# 'image/jpeg'


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


client = rets.http.RetsHttpClient(
    login_url='https://rets.nlar.mlxmatrix.com/Rets/login.ashx',
    username='SMARTERAGENTMOBILE',
    password='#SMA@22bile',
    # Alternatively authenticate using user agent password
    # user_agent='rets-python/0.3',
    # user_agent_password=''
)

# Authenticate and fetch available transactions
client.login()

# See available Resources
resource = client.get_metadata('resource')
# print(resource)

# See available Classes for the Property resource
meta_class_res = client.get_metadata('class', resource='Property')
# print(meta_class_res)

# See the Table definition for Class A
meta_table_res = client.get_metadata('class', resource='Property', class_=None)
print(meta_table_res)

# Get a sample of recent listings
search_result = client.search(
    resource='Property',
    class_= 'Listing',
    query='(TRUE)',
    # select='LIST_87,LIST_105,LIST_1',
    limit=10,
    count=1,
)

# Get the KeyField values of the listings
# resource_keys = [r['LIST_1'] for r in search_result.data]

# Fetch the photo URLs for those recent listings
# objects = client.get_object(
#     resource='Property',
#     object_type='HiRes',
#     resource_keys=resource_keys,
#     location=True,
# )

