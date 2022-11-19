from parsing import *

def createModelsFile(table):

    out_file = ""

    table_name = f"{table['name'].strip()}"
    multi_name = f"{getMultiName(table_name)}"

    table_dict = getTable(table['columns'])

    # Creating the main struct
    struct_name = table_name.title().replace("_","")
    struct_name = cleanStructName(struct_name)

    out_file += f"type {struct_name} struct {{\n{getStruct(table_dict, table)}}}"

    out_file += f"""
    type {struct_name}List struct {{
        {multi_name} []{struct_name}
    }}
    """

    # Getting initials for simplified endpoint creation
    initials = re.sub('[^A-Z]', '', struct_name).lower()

    return out_file

    