
def nullIDCheck(table, initials): 

    if "id" in table:
        return f"""
        if {initials}.Id == uuid.Nil {{
            newId, _ = uuid.NewV4()
            {initials}.Id = newId
            slog.Info("replaced null id", "new id", {initials}.Id)
        }}
        """
