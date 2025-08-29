import rets
from rets import Session
import json

login_url = 'https://rets.nlar.mlxmatrix.com/Rets/login.ashx'
username = 'SMARTERAGENTMOBILE'
password = '#SMA@22bile'
rets_client = Session(login_url, username, password)
rets_client.login()
system_data = rets_client.get_system_metadata()

# See available Resources
all_resources = rets_client.get_resource_metadata()
# print(all_resources)

# Get classes for the Property resource
resource = 'Property'
all_classes = rets_client.get_class_metadata(resource)

resource_class = 'Listing'
dmql_query ='(ListPrice=150000+)'
# {'version': '1.11.76004', 'system_description': 'MLS-RETS', 'system_id': 'MLS-RETS'}
# resources = rets_client.get_resource_metadata((resource='Agent')
# print(system_data)

# search_results = rets_client.search(resource='Property', resource_class='RES')
# for result in search_results:
#     result
# print(search_results)


print(dir(rets_client.get_table_metadata(resource, resource_class)))
print(rets_client.get_table_metadata(resource, resource_class))
print('-------------------------------------------------')

# test1 = rets_client.search(resource=resource,resource_class=resource_class,limit=1,dmql_query=dmql_query)
# print(test1)

# # print(list(test1))
# test1data = list(test1)
# # print(test1data[0])
# json_test = json.dumps(test1data[0], indent=4)
# print(json_test)

# rets_client.logout()