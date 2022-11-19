
![Benjamin Bannekat](assets/4x/RoadieLogoWhite@4x.png)

# The Encore developer's best friend

I started this project because I found myself spending hours upon hours writing code to set up the same CRUD endpoints over and over again. With Encore, the deployment part of this is already a breeze - but being lazy, I want to get to the fun part even faster. Therefore, I wrote a script to parse my migrations file to set up the folder structure with the endpoints in my own preferred way.

## TODO

### Basic CRUD

- [ ] Add `GET` endpoint for each column in table, always returning an array of entries (make sure to highlight endpoints where SQL unique constraint means max 1 entry is returned)
- [ ] Add `PUT` endpoint for updating a table entry, returning error if id is null, but allowing other values to be null and in that case not including them in SQL execution
- [ ] ADD `DELETE` endpoint for removing a table entry with a specified id

### Advanced CRUD

- [ ] Add ways of retrieving all related information from other tables as well by using the `REFERENCES` keyword in SQL
- [ ] Add `GET` functionality to retrieve entries with any `TIMESTAMP` column datatype for a specified to/from time interval

### Testing

- [ ] Add support for autogenerating tests with complete mock data

### Future ideas

- Allowing for different types of project structures, i.e. not always the `models` - `controllers` setup.
- Autogenerating a frontend client to view and execute CRUD operations

## How does it work?

## Intended use cases

## Functionality

## :warning: Important

Roadie is not intended to be used as a substitution for production-level development. Always make sure to test your code. 



