from operator import indexOf
import os
import uuid
import re
import time

# Use this for subgroupings of tables
def validateInput_Dict(qst, allowed, error_msg):

    val = input(qst)

    if val in allowed:
        print("Success")
        return allowed[val]
    else:
        print(error_msg)
        return validateInput_Dict(qst, allowed, error_msg)

def validateInput_subGroupName(qst, error_msg, subgroups):

    subgroup_idx = int(input(qst)) - 1

    if (int(subgroup_idx) >= 1) and (int(subgroup_idx) <= len(subgroups)):
        linked_subgroup = subgroups[subgroup_idx]
        confirm = False
        answers = {
            "Y" : True,
            "y" : True,
            "N" : False,
            "n" : False,
            "no" : False,
            "yes" : True
        }
        confirm = validateInput_Dict(f"Table will be linked to {linked_subgroup}. Correct? (Y/N)", answers, error_msg)
        if confirm == True:
            return linked_subgroup
        else:
            return validateInput_subGroupName(qst, error_msg, subgroups)
    else:
        print(error_msg)
        return validateInput_subGroupName(qst, error_msg, subgroups)

def validateInput_PkgName(qst, error_msg, confirm_msg):

    val = input(qst)

    trimVal = val.lower().strip()

    if len(val) < 2:
        print(error_msg)
        return validateInput_PkgName(f"Please try again. {qst}", error_msg, confirm_msg)
    else:
        confirmed = False
        answers = {
            "Y" : True,
            "y" : True,
            "N" : False,
            "n" : False,
            "no" : False,
            "yes" : True
        }
        confirmed = validateInput_Dict(f"Package will be named {trimVal}. {confirm_msg}", answers, error_msg)
        if confirmed == True:
            return trimVal
        else:
            return validateInput_PkgName(qst, error_msg, confirm_msg)


def getMultiName(tableName):

        if "_" in tableName:
            multiName = tableName.split("_")[1].title()
        else:
            multiName = tableName.title()

        return multiName

def getTable(columns):

        table = {}
        for col in columns:
            table[col] = columns[col]["type"]
        
        return table

# TODO ADD SUPPORT FOR ARRAYS
def getDtype(input):
    if input == uuid:
        return "uuid.UUID"
    elif input == str:
        return "string"
    elif input == time.time:
        return "time.Time"
    elif input == int:
        return "int"
    elif input == float:
        return "float64"
    elif input == bool:
        return "bool"

def getStruct(table_in, table):
    structString = ""

    for i in table_in:
        structString += i.title().replace("_","")
        if table['columns'][i]['array'] == False:
            structString += f" {getDtype(table_in[i])}\n"
        else:
            structString += f" []{getDtype(table_in[i])}\n"

    return structString

def getColumnsWithoutId(table):
    insertionsString = ""

    for i in table:
        if i != "id":
            insertionsString += f"{i},"

    return insertionsString[:-1]

def getColumnsWith_Id(table):
    insertionsString = ""

    for i in table:
        insertionsString += f"{i},"

    return insertionsString[:-1]

def getDollars(table):
    dollars = ""

    for i in range(1, len(table)):
        dollars += f"${i},"

    return dollars[:-1]

def getDollarsID(table):
    dollars = ""

    for i in range(1, len(table)+1):
        dollars += f"${i},"

    return dollars[:-1]

def getParams(table, initials):
    paramsString = ""

    for i in table:
        if i != "id":
            paramsString += f"{initials}.{i.title().replace('_','')}, "

    return paramsString[:-2]

def getParamsID(table, initials):
    paramsString = ""
    for i in table:
        paramsString += f"{initials}.{i.title().replace('_','')}, "
    return paramsString[:-2]

def getReturnParams(table, initials):
    returnParamsString = ""
    for i in table:
        if i != "id":
            returnParamsString += f"{i.title().replace('_','')}: "
            returnParamsString += f"{initials}.{i.title().replace('_','')}, "
    return returnParamsString[:-2]

def insertionTime(table, initials):
    if "updated" in table:
        return f"""
        if {initials}.Updated.IsZero() {{
            {initials}.Updated = time.Now()
            {initials}.Created = time.Now()
        }}
        """
    else:
        return ""

def updateTime(table, initials):
    if "updated" in table:
        return f"""
        if {initials}.Updated.IsZero() {{
            {initials}.Updated = time.Now()
        }}
        """
    else:
        return ""

def cleanStructName(struct_name:str):
    if struct_name[-3:] == "ses":
        struct_name = struct_name[:-2]
    elif struct_name[-3:] == "pes":
        struct_name = struct_name[:-1]
    elif struct_name[-3:] == "ons":
        struct_name = struct_name[:-1]
    elif struct_name[-3:] == "ies":
        struct_name = struct_name[:-3] + "y"
    elif struct_name[-3:] == "ges":
        struct_name = struct_name[:-1]
    elif struct_name[-3:] == "ers":
        struct_name = struct_name[:-1]
    elif struct_name[-3:] == "nts":
        struct_name = struct_name[:-1]
    elif struct_name[-3:] == "ups":
        struct_name = struct_name[:-1]
    elif struct_name[-3:] == "ues":
        struct_name = struct_name[:-1]
    elif struct_name[-3:] == "tes":
        struct_name = struct_name[:-1]
    elif struct_name[-3:] == "ons":
        struct_name = struct_name[:-1]
    elif struct_name[-3:] == "cts":
        struct_name = struct_name[:-1]
    elif struct_name[-3:] == "ins":
        struct_name = struct_name[:-1]
    
    return struct_name

def getTablesFromSQLFile(parsedFile:str):

    tables = parsedFile.split("CREATE TABLE")

    tables_out = []

    for t in tables[1:]:

        table = {}

        name = t.split(" (")[0]

        t = t.replace(f"{name}","")
        t = t.replace("(","")
        t = t.replace(")","")
        t = t.split(";")[0]

        columns = t.split(",")

        table["name"] = name
        table["columns"] = {}
        table["columns"]["id"] = {"type" : uuid, "array": False}

        for col in columns[1:]:

            trimCol = col.strip()
            if "[]" in trimCol:
                arr = True
            else:
                arr = False
            if "REFERENCES" in trimCol:
                colName = re.sub('[^a-z_]', '', trimCol.split("REFERENCES")[0])
            else:    
                colName = re.sub('[^a-z_]', '', trimCol)
            colType = re.sub('[^A-Z]', '', trimCol).replace("\n","")
            table["columns"][f"{colName}"] = {}
            if ("TEXT" in colType) or ("VARCHAR" in colType):
                colTypeOut = str
                table["columns"][f"{colName}"]["type"] = colTypeOut
            elif ("UUID" in colType):
                colTypeOut = uuid
                table["columns"][f"{colName}"]["type"] = colTypeOut
            elif ("TIMESTAMP" in colType):
                colTypeOut = time.time
                table["columns"][f"{colName}"]["type"] = colTypeOut
            elif ("DATE" in colType):
                colTypeOut = time.time
                table["columns"][f"{colName}"]["type"] = colTypeOut
            elif ("INT" in colType):
                colTypeOut = int
                table["columns"][f"{colName}"]["type"] = colTypeOut
            elif ("FLOAT" in colType) or ("DOUBLE" in colType):
                colTypeOut = float
                table["columns"][f"{colName}"]["type"] = colTypeOut
            elif ("BOOLEAN" in colType):
                colTypeOut = bool
                table["columns"][f"{colName}"]["type"] = colTypeOut

            table["columns"][f"{colName}"]["array"] = arr
        
        tables_out.append(table)
    
    return tables_out

def nullIDCheck(table, initials): 

    if "id" in table:
        return f"""
        if {initials}.Id == uuid.Nil {{
            newId, _ = uuid.NewV4()
            {initials}.Id = newId
            slog.Info("replaced null id", "new id", {initials}.Id)
        }}
        """

def generateRequestParams(struct_name, table_dict, api_method, table):

    reqParamsString = f"""type {api_method}{struct_name}RequestParams struct {{
        {struct_name} models.{struct_name}
    }}"""

    return reqParamsString

def generateResponseParams(struct_name, table_dict, api_method, table):

    respParamsString = f"""type {api_method}{struct_name}ResponseParams struct {{
        {struct_name} models.{struct_name}
    }}"""

    return respParamsString

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

    

def generateControllerInsert(struct_name, table_name, initials, table_dict, access, table):

    # Adding struct def for request params
    function_string = generateRequestParams(struct_name, table_dict, "Insert", table) + "\n"
    # Adding struct def for response params
    function_string += generateResponseParams(struct_name, table_dict, "Insert", table) + "\n"

    function_string += f"""\n\n
    // Insert{struct_name} adds a row to the {table_name} table
    // If no id is passed in, one will be autogenerated

    //encore:api {access} method=POST
    func Insert{struct_name}(ctx context.Context, {initials} *Insert{struct_name}RequestParams) (*Insert{struct_name}ResponseParams, error) {{
        
        {insertionTime(table_dict, initials)}

        {nullIDCheck(table_dict, initials)}

        // Initializing transaction
        tx, err := sqldb.Begin(ctx)
        if err != nil {{
            return nil, &errs.Error{{Code: errs.Internal, Message: "Could not initialize SQL transaction"}}
        }} 
        defer tx.Rollback()

        // Executing insertion by calling repository layer
        err = repository.Insert{struct_name}(ctx, tx, {initials})
        if err != nil {{
            return nil, &errs.Error{{Code: errs.Internal, Message: "Could not insert {struct_name}"}}
        }}


        // Committing transaction
        err = tx.Commit()
         if err != nil {{
            return nil, &errs.Error{{Code: errs.Internal, Message: "Could not commit SQL transaction"}}
        }} 

        response := {initials}

        return &response, nil

    }}\n\n
    """

    return function_string


def createControllerFile(table, package_name, access):

    out_file = ""

    table_name = f"{table['name'].strip()}"
    multi_name = f"{getMultiName(table_name)}"

    table_dict = getTable(table['columns'])

    # Creating the main struct
    struct_name = table_name.title().replace("_","")
    struct_name = cleanStructName(struct_name)

    # Getting initials for simplified endpoint creation
    initials = re.sub('[^A-Z]', '', struct_name).lower()


    # Adding the insertion endpoint
    out_file += generateControllerInsert(struct_name, table_name, initials, table_dict, access, table)

    return out_file
    


def main():
    MIGRATIONS_PATH = input("Paste the path to your (clean) migrations file:\n")


    # Letting user create package name
    pkg_name_qst = "\nPlease enter the main package name (must be lowercase):\n\n"
    pkg_name_error_msg = "Invalid package name."
    pkg_name_confirm_msg = "\nIs this correct? (Y/N)\n\n"
    MAIN_PACKAGE_NAME = validateInput_PkgName(pkg_name_qst, pkg_name_error_msg, pkg_name_confirm_msg)

    print("Looking for file...")
    with open(f"{MIGRATIONS_PATH}", 'r') as file:
        data = file.read()
    print("Found file")
    tablesOut = getTablesFromSQLFile(data)
    print("Successfully parsed tables")

    tableGroups = []
    tables_in_tableGroup = {}
    table_objs_in_tableGroup = {}

    # Begin iterating over per table
    for table in tablesOut:

        if len(tableGroups) == 0:
            print(f"\nCURRENTLY HANDLING TABLE {table['name']} ({indexOf(tablesOut, table) + 1} / {len(tablesOut)})")
            sub_pkg_name_qst = "\nPlease enter the new sub-package name (lowercase only):\n\n"
            sub_pkg_name_error_msg = "Invalid package name."
            sub_pkg_name_confirm_msg = "\nIs this correct? (Y/N):\n\n"
            SUB_PACKAGE_NAME = validateInput_PkgName(sub_pkg_name_qst, sub_pkg_name_error_msg, sub_pkg_name_confirm_msg)
            tableGroups.append(SUB_PACKAGE_NAME)
            tables_in_tableGroup[SUB_PACKAGE_NAME] = [table['name']]
            table_objs_in_tableGroup[SUB_PACKAGE_NAME] = {}
            table_objs_in_tableGroup[SUB_PACKAGE_NAME][table['name']] = table
        else:
            print("\nYou have the following subgroups:\n--------------------------------------")

            for subgroup_idx in range(len(tableGroups)):
                print(f"\t({subgroup_idx + 1}):\t{tableGroups[subgroup_idx]} - ({tables_in_tableGroup[tableGroups[subgroup_idx]]})")

            print("--------------------------------------\n")
            print(f"\nCURRENTLY HANDLING TABLE {table['name']} ({indexOf(tablesOut, table) + 1} / {len(tablesOut)})")
            # New or existing subgroup
            want_new_group = False
            answers = {
                "Y" : True,
                "y" : True,
                "N" : False,
                "n" : False,
                "no" : False,
                "yes" : True
            }
            ask_new_group = validateInput_Dict(qst = f"\nDo you want to create a new group for table {table['name']}? (Y/N)\n\n", allowed = answers, error_msg = "Invalid input - try again.")

            # Creating a new subgroup
            if ask_new_group == True:
                sub_pkg_name_qst = "\nPlease enter the new sub-package name (lowercase only):\n\n"
                sub_pkg_name_error_msg = "Invalid package name."
                sub_pkg_name_confirm_msg = "\nIs this correct? (Y/N)\n\n"
                SUB_PACKAGE_NAME = validateInput_PkgName(sub_pkg_name_qst, sub_pkg_name_error_msg, sub_pkg_name_confirm_msg)
                tableGroups.append(SUB_PACKAGE_NAME)
                tables_in_tableGroup[SUB_PACKAGE_NAME] = [table['name']]
                table_objs_in_tableGroup[SUB_PACKAGE_NAME] = {}
                table_objs_in_tableGroup[SUB_PACKAGE_NAME][table['name']] = table

            # Linking to an existing subgroup
            else:
                link_qst = f"\nEnter the value of the subgroup you want to link the table to (1 - {len(tableGroups)}): \n\n"
                error_msg = "Could not link the table to group - try again."

                SUB_PACKAGE_NAME = validateInput_subGroupName(link_qst, error_msg, tableGroups)
                tables_in_tableGroup[SUB_PACKAGE_NAME].append(table['name'])
                table_objs_in_tableGroup[SUB_PACKAGE_NAME][table['name']] = table

        # TABLE HAS NOW BEEN CATEGORIZED AND LINKED PROPERLY
        print(f"Table {table['name']} has been successfully read and put in subgroup {SUB_PACKAGE_NAME}")

    print(f"{len(tableGroups)} tables have been categorized properly")
    for tableGroup in tableGroups:
        print(f"{indexOf(tableGroups, tableGroup) +1}.\t{tableGroup}")

    # Now iterating over each group to create a controller file

    for tableGroup in tableGroups:

        # Generating controller file
        controller_file = f"package {MAIN_PACKAGE_NAME}" + "\n\n"

        for table in tables_in_tableGroup[tableGroup]:

            table_obj = table_objs_in_tableGroup[tableGroup][table]

            controller_file += createControllerFile(
                table_obj,
                MAIN_PACKAGE_NAME,
                "auth"
            )


        # Create a new directory because it does not exist
        isExist = os.path.exists(f"{MAIN_PACKAGE_NAME}")
        if not isExist:
            os.makedirs(MAIN_PACKAGE_NAME)
            print("The new directory is created!")


        output_file = open(f"{MAIN_PACKAGE_NAME}/{tableGroup}.controllers.go", "a")
        output_file.write(controller_file)
        output_file.close()
    
    for tableGroup in tableGroups:

        # Generating controller file
        models_file = f"package models" + "\n\n"

        for table in tables_in_tableGroup[tableGroup]:

            table_obj = table_objs_in_tableGroup[tableGroup][table]

            models_file += createModelsFile(table_obj)


        # Create a new directory because it does not exist
        isExist = os.path.exists(f"{MAIN_PACKAGE_NAME}/models/")
        if not isExist:
            os.makedirs(f"{MAIN_PACKAGE_NAME}/models/")
            print("The new directory is created!")


        output_file = open(f"{MAIN_PACKAGE_NAME}/models/{tableGroup}.go", "a")
        output_file.write(models_file)
        output_file.close()
        

if __name__ == '__main__':
    main()