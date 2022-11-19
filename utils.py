import json

def nullIDCheck(table, initials): 

    if "id" in table:
        return f"""
        if {initials}.Id == uuid.Nil {{
            newId, _ = uuid.NewV4()
            {initials}.Id = newId
            slog.Info("replaced null id", "new id", {initials}.Id)
        }}
        """

def getColumnNames(table_dict):

    keys = json.dumps(list(table_dict.keys()))
    str_keys = str(keys).replace("[","")
    str_keys = str_keys.replace("]", "")

    return str_keys