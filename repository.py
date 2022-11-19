from utils import *
from structs import *
from parsing import *

def createRepositoryFile(table, package_name):

    out_file = ""

    table_name = f"{table['name'].strip()}"
    multi_name = f"{getMultiName(table_name)}"

    # Creating the main struct
    struct_name = table_name.title().replace("_","")
    struct_name = cleanStructName(struct_name)

    # Getting initials for simplified endpoint creation
    initials = re.sub('[^A-Z]', '', struct_name).lower()

    # Adding the repository functions

    return out_file