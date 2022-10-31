package random

type InsertCompanyTypeRequestParams struct {
        CompanyType models.CompanyType
    }
type InsertCompanyTypeResponseParams struct {
        CompanyType models.CompanyType
    }



    // InsertCompanyType adds a row to the company_types table
    // If no id is passed in, one will be autogenerated

    //encore:api auth method=POST
    func InsertCompanyType(ctx context.Context, ct *InsertCompanyTypeRequestParams) (*InsertCompanyTypeResponseParams, error) {
        
        
        if ct.Updated.IsZero() {
            ct.Updated = time.Now()
            ct.Created = time.Now()
        }
        

        
        if ct.Id == uuid.Nil {
            newId, _ = uuid.NewV4()
            ct.Id = newId
            slog.Info("replaced null id", "new id", ct.Id)
        }
        

        // Initializing transaction
        tx, err := sqldb.Begin(ctx)
        if err != nil {
            return nil, &errs.Error{Code: errs.Internal, Message: "Could not initialize SQL transaction"}
        } 
        defer tx.Rollback()

        // Executing insertion by calling repository layer
        err = repository.InsertCompanyType(ctx, tx, ct)
        if err != nil {
            return nil, &errs.Error{Code: errs.Internal, Message: "Could not insert CompanyType"}
        }


        // Committing transaction
        err = tx.Commit()
         if err != nil {
            return nil, &errs.Error{Code: errs.Internal, Message: "Could not commit SQL transaction"}
        } 

        response := ct

        return &response, nil

    }


    type InsertTeamMemberRequestParams struct {
        TeamMember models.TeamMember
    }
type InsertTeamMemberResponseParams struct {
        TeamMember models.TeamMember
    }



    // InsertTeamMember adds a row to the team_members table
    // If no id is passed in, one will be autogenerated

    //encore:api auth method=POST
    func InsertTeamMember(ctx context.Context, tm *InsertTeamMemberRequestParams) (*InsertTeamMemberResponseParams, error) {
        
        
        if tm.Updated.IsZero() {
            tm.Updated = time.Now()
            tm.Created = time.Now()
        }
        

        
        if tm.Id == uuid.Nil {
            newId, _ = uuid.NewV4()
            tm.Id = newId
            slog.Info("replaced null id", "new id", tm.Id)
        }
        

        // Initializing transaction
        tx, err := sqldb.Begin(ctx)
        if err != nil {
            return nil, &errs.Error{Code: errs.Internal, Message: "Could not initialize SQL transaction"}
        } 
        defer tx.Rollback()

        // Executing insertion by calling repository layer
        err = repository.InsertTeamMember(ctx, tx, tm)
        if err != nil {
            return nil, &errs.Error{Code: errs.Internal, Message: "Could not insert TeamMember"}
        }


        // Committing transaction
        err = tx.Commit()
         if err != nil {
            return nil, &errs.Error{Code: errs.Internal, Message: "Could not commit SQL transaction"}
        } 

        response := tm

        return &response, nil

    }


    