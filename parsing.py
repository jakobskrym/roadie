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
