CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- List of countries with an alpha code and a short english country name
CREATE TABLE countries (
    id  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alpha  VARCHAR(2) NOT NULL UNIQUE,
    country_name TEXT NOT NULL UNIQUE,
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- List of accepted company types with descriptions to prevent duplication
CREATE TABLE company_types (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_type TEXT NOT NULL UNIQUE,
    type_description TEXT NOT NULL,
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- Temporary solution for user management
CREATE TABLE team_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL UNIQUE,
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- List of accepted segments
CREATE TABLE company_segments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_segment VARCHAR(80) NOT NULL,
    segment_description VARCHAR(250) NOT NULL,
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);
