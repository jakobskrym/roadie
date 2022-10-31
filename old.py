FILE += f"""

    // Insert{structName} adds a row to the {TABLE_NAME} table
    //encore:api public method=POST path=/Insert{structName}
    func Insert{structName}(ctx context.Context, {initials} *{structName}) (*{structName}, error) {{

        {insertionTime(TABLE)}

        _, err := sqldb.Exec(ctx, `
        INSERT INTO {TABLE_NAME} ({getColumnsWithoutId(TABLE)}) VALUES ({getDollars(TABLE)})`, {getParams(TABLE)})

        return &{structName}{{{getReturnParams(TABLE)}}}, err
    }}

        """

    # FOR INSERTING WITH ID
    FILE += f"""

    // Insert{structName}_ID adds a row to the {TABLE_NAME} table with a predefined ID
    //encore:api public method=POST path=/Insert{structName}_ID
    func Insert{structName}ID(ctx context.Context, {initials} *{structName}) (*{structName}, error) {{

        {insertionTime(TABLE)}

        _, err := sqldb.Exec(ctx, `
        INSERT INTO {TABLE_NAME} ({getColumnsWith_Id(TABLE)}) VALUES ({getDollarsID(TABLE)})`, {getParamsID(TABLE)})

        return &{structName}{{{getReturnParams(TABLE)}}}, err
    }}

        """

    def getParamsSelection(table):

        paramsString = ""

        for i in table:
            if i != "id":
                paramsString += f"&{initials}.{i.title().replace('_','')}, "
        return paramsString[:-2]


    def getParamsSelectionMulti(table):

        paramsString = ""

        for i in table:
            paramsString += f"&{initials}.{i.title().replace('_','')}, "
        return paramsString[:-2]

    def getColumnsWithId(table):

        insertionsString = ""

        for i in table:
            insertionsString += f"{i},"

        return insertionsString[:-1]

    FILE += f"""
    // Get{structName} selects a row from the {TABLE_NAME} table by id
    //encore:api public method=GET path=/Get{structName}/:id
    func Get{structName}(ctx context.Context, id uuid.UUID) (*{structName}, error) {{
        {initials} := &{structName}{{Id: id}}

        err := sqldb.QueryRow(ctx, 
        `SELECT {getColumnsWithoutId(TABLE)} FROM {TABLE_NAME} WHERE id = $1`, id).Scan({getParamsSelection(TABLE)})

    return {initials}, err
    }}

    """


    FILE += f"""
    // Get{structName}List returns a list of all rows from the {TABLE_NAME} table
    //encore:api public method=GET path=/Get{structName}List
    func Get{structName}List(ctx context.Context) (*{structName}List, error) {{
        rows, err := sqldb.Query(ctx, `SELECT {getColumnsWithId(TABLE)} FROM {TABLE_NAME}`)

        if err != nil {{
            return nil, err
        }}

        defer rows.Close()

        {MULTIPLE_NAME.lower()} := []{structName}{{}}

        for rows.Next() {{
            var {initials} {structName}
            err = rows.Scan({getParamsSelectionMulti(TABLE)})
            if err != nil {{
                return nil, err
            }}

            {MULTIPLE_NAME.lower()} = append({MULTIPLE_NAME.lower()}, {initials})
        }}
        if err := rows.Err(); err != nil {{
            return nil, err
        }}

        response := &{structName}List{{{MULTIPLE_NAME}: {MULTIPLE_NAME.lower()}}}

        return response, err
    }}
    """

    def getColumnsWithoutIdUpdate(table):

        insertionsString = ""

        count = 0

        for i in table:
            count += 1
            if i != "id":
                insertionsString += f"{i} = ${count},"

        return insertionsString[:-1]

    FILE += f"""
    // Update{structName} updates an existing row in the {TABLE_NAME} table
    //encore:api public method=PUT path=/Update{structName}
    func Update{structName}(ctx context.Context, {initials} *{structName}) (*{structName}, error) {{

        {updateTime(TABLE)}

        _, err := sqldb.Exec(ctx, `
        UPDATE {TABLE_NAME} SET {getColumnsWithoutIdUpdate(TABLE)} WHERE id = $1`, {initials}.Id, {getParams(TABLE)})

        return {initials}, err
    }}
    """

    FILE += f"""
    // Delete{structName} deletes an existing company type
    //encore:api public method=DELETE path=/Delete{structName}
    func Delete{structName}(ctx context.Context, {initials} *{structName}) (*{structName}, error) {{

        _, err := sqldb.Exec(ctx, `
        DELETE FROM {TABLE_NAME} WHERE id  = $1`, {initials}.Id)

        return {initials}, err
    }}
    """


    f = open(f"{MAIN_PACKAGE_NAME}/{TABLE_NAME}_CRUD.go", "a")
    f.write(FILE)
    f.close()

