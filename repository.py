from utils import *
from structs import *
from parsing import *


def generateRepositoryInsert(struct_name, table_name, initials, table_dict, table):

    function_string = ""

    function_string += f"""\n\n
    // Insert{struct_name} inserts an entry into the {table_name} table

    func Insert{struct_name}(ctx context.Context, tx *sqldb.Tx, {initials} models.{struct_name}) error {{

        _, err := tx.Exec(ctx, `
            INSERT INTO {table_name} (
                {getColumnsWith_Id(table_dict)}
            )
            VALUES ({getDollarsID(table_dict)})
        `, {getParamsID(table_dict, initials)})

        if err != nil {{
            slog.Error("Could not insert {struct_name}", "err", err)
            return err
        }}

        return nil

    }}
    """

    return function_string

def generateRepositoryRetrieval(struct_name, table_name, initials, table_dict, table):

    function_string = ""

    function_string += f"""\n\n
    // Get{struct_name} retrieves all entries from the {table_name} table that match the passed arguments

    func Get{struct_name}(ctx context.Context, tx *sqldb.Tx, {initials} models.{struct_name}) ([]models.{struct_name}, error) {{

        {initials}List := []models.{struct_name}{{}}

        column_names := []string{{{getColumnNames(table_dict)}}}

        struct_to_column := make(map[string]string)
        query_params := make(map[string]bool)
        var query_values []any
        reflected_{initials} := reflect.ValueOf(&{initials}).Elem()
        no_query_params := reflected_{initials}.NumField()

        for i := 0; i < reflected_{initials}.NumField(); i++ {{
            param := reflected_{initials}.Type().Field(i).Name
            arg := reflected_{initials}.Field(i).Interface()

            struct_to_column[param] = column_names[i]

            // Defaulting to true
            query_params[param] = true
            
            // Overriding if null
            switch reflected_{initials}.Type().Field(i).Type {{
                case float64:
                    if arg == 0.0 {{
                        query_params[param] = false
                        no_query_params -= 1
                    }} else {{
                        query_values = append(query_values, arg)
                    }}
                case float32:
                    if arg == 0.0 {{
                        query_params[param] = false
                        no_query_params -= 1
                    }} else {{
                        query_values = append(query_values, arg)
                    }}
                case string:
                    if arg == "" {{
                        query_params[param] = false
                        no_query_params -= 1
                    }} else {{
                        query_values = append(query_values, arg)
                    }}
                case uuid.UUID:
                    if arg == uuid.Nil() {{
                        query_params[param] = false
                        no_query_params -= 1
                    }} else {{
                        query_values = append(query_values, arg)
                    }}
                case int:
                    if arg == 0 {{
                        query_params[param] = false
                        no_query_params -= 1
                    }} else {{
                        query_values = append(query_values, arg)
                    }}
                case []int{{}}:
                    if len(arg) == 0 {{
                        query_params[param] = false
                        no_query_params -= 1
                    }} else {{
                        query_values = append(query_values, arg)
                    }}
                case []float64{{}}:
                    if len(arg) == 0 {{
                        query_params[param] = false
                        no_query_params -= 1
                    }} else {{
                        query_values = append(query_values, arg)
                    }}
                case []float32{{}}:
                    if len(arg) == 0 {{
                        query_params[param] = false
                        no_query_params -= 1
                    }} else {{
                        query_values = append(query_values, arg)
                    }}
                case []string{{}}:
                    if len(arg) == 0 {{
                        query_params[param] = false
                        no_query_params -= 1
                    }} else {{
                        query_values = append(query_values, arg)
                    }}
                case []uuid.UUID{{}}:
                    if len(arg) == 0 {{
                        query_params[param] = false
                        no_query_params -= 1
                    }} else {{
                        query_values = append(query_values, arg)
                    }}
            }}
        }}

        // Constructing the retrieval query
        var query strings.Builder

        query.WriteString(`
        SELECT (
            {getColumnsWith_Id(table_dict)}
        )
        FROM
            {table_name} 
        `)

        // Returning all rows if no specified query params
        if len(query_params) != 0 {{
            query.WriteString("WHERE")
        }}

        param_idx := 1
        for param, notNil := range query_params {{
            if notNil == true {{
                query.WriteString(
                    fmt.Sprintf("%d = '$%d'", struct_to_column[param], param_idx)
                )
                if param_idx < no_query_params {{
                    query.WriteString(", ")
                }} else {{
                    query.WriteString("")
                }}
                param_idx += 1
            }}
        }}

        // Executing query
        rows, err := sqldb.Query(ctx, query.String(), query_values...)

        defer rows.Close()
        for rows.Next() {{
            {initials}Row := models.{struct_name}{{}}

            err := rows.Scan(
                {getParamsSelectionMulti(table_dict, initials)}
            )

            if err != nil {{
                slog.Error("Could not scan {struct_name}", "err", err)
            }}

            {initials}List = append({initials}List, {initials})
        }}


        if err != nil {{
            slog.Error("Could not retrieve {struct_name}", "err", err)
            return err
        }}

        return {initials}List, nil

    }}
    """

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
    out_file += generateRepositoryRetrieval(struct_name, table_name, initials, table_dict, table)

    return out_file