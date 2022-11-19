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