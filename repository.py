from utils import *
from structs import *
from parsing import *

def generateRepositoryInsert(struct_name, table_name, initials, table_dict, table):

    function_string = ""

    return function_string

def createRepositoryFile(table, package_name):

    out_file = ""

    table_name = f"{table['name'].strip()}"
    multi_name = f"{getMultiName(table_name)}"

    table_dict = getTable(table['columns'])

    # Creating the main struct
    struct_name = table_name.title().replace("_","")
    struct_name = cleanStructName(struct_name)

    # Getting initials for simplified endpoint creation
    initials = re.sub('[^A-Z]', '', struct_name).lower()

    # Adding the repository functions
    out_file += generateRepositoryInsert(struct_name, table_name, initials, table_dict, table)
    #out_file += generateRepositoryRetrieval()

    return out_file