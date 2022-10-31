package models

type CompanyType struct {
Id uuid.UUID
CompanyType string
TypeDescription string
Created time.Time
Updated time.Time
}
    type CompanyTypeList struct {
        Types []CompanyType
    }
    type TeamMember struct {
Id uuid.UUID
Name string
Email string
Phone string
Role string
Created time.Time
Updated time.Time
}
    type TeamMemberList struct {
        Members []TeamMember
    }
    