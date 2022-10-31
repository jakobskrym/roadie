package models

type Country struct {
Id uuid.UUID
Alpha string
CountryName string
Created time.Time
Updated time.Time
}
    type CountryList struct {
        Countries []Country
    }
    