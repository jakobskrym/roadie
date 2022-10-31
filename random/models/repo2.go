package models

type CompanySegment struct {
Id uuid.UUID
CompanySegment string
SegmentDescription string
Created time.Time
Updated time.Time
}
    type CompanySegmentList struct {
        Segments []CompanySegment
    }
    