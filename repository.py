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

        {initials} := []models.{struct_name}{{}}

        reflected_{initials} := reflect.ValueOf(&{initials}).Elem() 
        for i := 0; i < reflected_{initials}.NumField(); i++ {{
            arg := reflected_{initials}.Field(i).Interface()

            switch reflected_{initials}.Type().Field(i).Type {{
                case float64:
                    if arg == 0.0 {{

                    }}
                case float32:
                    if arg == 0.0 {{

                    }}
                case string:
                    if arg == "" {{

                    }}
                case uuid.UUID:
                    if arg == uuid.Nil() {{

                    }}
                case int:
                    if arg == 0 {{

                    }}
                case []int:
                    if len(arg) == 0 {{

                    }}
                case []float64:
                    if len(arg) == 0 {{

                    }}
                case []float32:
                    if len(arg) == 0 {{

                    }}
                case []string:
                    if len(arg) == 0 {{

                    }}
                case []uuid.UUID:
                    if len(arg) == 0 {{

                    }}
            }}
        }}

        Create a for loop to construct the SQL query
        1. Find which columns are passed in as nil (diff per dtype) and exclude them from matching query
        2. Construct select query


        _, err := tx.Exec(ctx, `
            SELECT (
                {getColumnsWith_Id(table_dict)}
            )
            FROM 
            {table_name}
            WHERE
            MATCHING FUNCTION
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