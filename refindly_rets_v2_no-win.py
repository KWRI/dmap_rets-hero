import rets
from rets import Session
import json

# --- START NEW FUNCTION DEFINITION ---
def save_json_to_file(json_data, directory, file_name='rets_search_results.json'):
    """
    Saves a JSON formatted string to a specified file within a given directory.

    Args:
        json_data (str): The JSON formatted string to be saved.
        directory (str): The path to the directory where the file should be saved.
        file_name (str, optional): The name of the file. Defaults to 'rets_search_results.json'.
    """
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        except OSError as e:
            print(f"Error creating directory '{directory}': {e}")
            return # Exit the function if directory creation fails

    # Define the full path for the output file
    full_file_path = os.path.join(directory, file_name)

    # Save the JSON string to a file
    try:
        with open(full_file_path, 'w') as f:
            f.write(json_data)
        print(f"Successfully exported search results to '{full_file_path}'")
    except IOError as e:
        print(f"Error writing to file '{full_file_path}': {e}")
        
# --- END NEW FUNCTION DEFINITION ---

login_url = 'http://retsgw.flexmls.com:80/rets2_3/Login'
username = 'dub.rets.kellerwilliamsadvantagerets'
password = 'mP(706KhDv'
rets_client = Session(login_url, username, password)
rets_client.login()


system_data = rets_client.get_system_metadata()
system_data_json = json.dumps(system_data, indent=4)


# See available Resources and convert to JSON
my_resource = 'Property'
all_resources = rets_client.get_resource_metadata()  
all_resources_json = json.dumps(all_resources, indent=4)

# See available Classes and convert to JSON
all_classes = rets_client.get_class_metadata(my_resource) 
all_classes_json = json.dumps(all_classes, indent=4)

# Get table metadata
my_class = 'A'
metadata = rets_client.get_table_metadata(my_resource, my_class)
metadata_json = json.dumps(metadata, indent=4)

# Get object metadata
object_metadata = rets_client.get_object_metadata(my_resource)
object_metadata_json = json.dumps(object_metadata, indent=4)

# Get object metadata
my_lookup_name = '20000801143243610168000000'
lookup_values = rets_client.get_lookup_values(my_resource, my_lookup_name)
lookup_values_json = json.dumps(lookup_values, indent=4)


# Create query parameters for search
# dmql_query ='(LIST_22=150000+)' # 1=Active, 2=Sold
dmql_query ='(LIST_15=5OTE1C2YKMD)' # 1=Active, 2=Sold

# Get search results using parameters
search_results = rets_client.search(resource=my_resource,resource_class=my_class,limit=10,dmql_query=dmql_query)

# Put search results into a dictionary then convert to JSON
all_records = []
for record in search_results:
    all_records.append(record)
    
all_records_json = json.dumps(all_records, indent=4)

target_directory = '/mnt/c/Users/yanir.regev2/Downloads'
output_file = '741 RETS data' # You can specify a different file name if you want

# save_json_to_file(all_resources_json, target_directory, f'{output_file} resources.json')
# save_json_to_file(all_classes_json, target_directory, f'{output_file} classes.json')
# save_json_to_file(metadata_json, target_directory, f'{output_file} metadata.json') 
save_json_to_file(all_records_json, target_directory, f'{output_file} records.json')
