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


-- This handles the investor newsletter signups
CREATE TABLE newsletter_signups (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- This handles the demo bookings
CREATE TABLE form_submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company TEXT,
    email TEXT NOT NULL,
    form_name TEXT,
    form_submission TEXT,
    honung TEXT,
    message TEXT,
    name TEXT NOT NULL,
    phone TEXT,
    role TEXT,
    status TEXT,
    subject TEXT,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Represents possible commercial relationships
CREATE TABLE relationship_types (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    relationship_type VARCHAR(80) NOT NULL UNIQUE,
    type_description VARCHAR(250) NOT NULL UNIQUE,
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- Represents possible stages within a commercial relationship
CREATE TABLE relationship_stages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    relationship_type UUID REFERENCES relationship_types(id),
    relationship_stage VARCHAR(80) NOT NULL,
    stage_description VARCHAR(250) NOT NULL,
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- Represents any company
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name TEXT NOT NULL UNIQUE,
    countries VARCHAR(2)[],
    company_type UUID REFERENCES company_types(id),
    company_segment UUID[],
    relationship_type UUID REFERENCES relationship_types(id),
    relationship_stage UUID REFERENCES relationship_stages(id),
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- Handles company customization 
CREATE TABLE company_customization (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id),
    primary_color VARCHAR(7),
    secondary_color VARCHAR(7),
    logo_path TEXT,
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- Additional operational information about companies working as retailers
CREATE TABLE retailer_info (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL UNIQUE REFERENCES companies(id),
    inventory_size INT,
    monthly_orders INT,
    avg_order_size FLOAT,
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- Represents any person
CREATE TABLE contacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    company_id UUID REFERENCES companies(id),
    role TEXT,
    email TEXT,
    phone TEXT,
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- Represents allowed action statuses
CREATE TABLE action_statuses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    status_name VARCHAR(80) NOT NULL UNIQUE,
    status_description VARCHAR(250) NOT NULL UNIQUE,
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- Represents an action point for a company
CREATE TABLE actions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    action_name TEXT NOT NULL,
    action_description TEXT NOT NULL,
    company_id UUID REFERENCES companies(id),
    action_deadline TIMESTAMPTZ DEFAULT NOW(),
    action_status UUID REFERENCES action_statuses(id),
    action_owner UUID NOT NULL REFERENCES team_members(id),
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- Represents general notes (previously timeline) relating to a company or contact
CREATE TABLE notes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subject_id UUID NOT NULL,
    note_title VARCHAR(250) NOT NULL,
    note_message TEXT NOT NULL,
    author UUID REFERENCES team_members(id),
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- Defines the allowed issue types
CREATE TABLE issue_types (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    issue_type TEXT NOT NULL UNIQUE,
    type_description TEXT NOT NULL UNIQUE,
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- Represents issues that have come up with clients
CREATE TABLE issues (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    issue_title VARCHAR(250) NOT NULL,
    issue_description TEXT NOT NULL,
    issue_type TEXT NOT NULL REFERENCES issue_types(issue_type),
    company_id UUID REFERENCES companies(id),
    issue_timestamp TIMESTAMPTZ DEFAULT NOW(),
    issue_author UUID REFERENCES team_members(id),
    issue_deadline TIMESTAMPTZ DEFAULT NOW(),
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- Defines allowed location types
CREATE TABLE location_types (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    location_type TEXT NOT NULL UNIQUE,
    type_description TEXT NOT NULL UNIQUE,
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);


-- Represents physical locations, can be shared across companies
CREATE TABLE locations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    location_type TEXT REFERENCES location_types(location_type),
    location_name TEXT NOT NULL,
    location_address TEXT NOT NULL,
    location_city TEXT NOT NULL,
    location_country VARCHAR(2) REFERENCES countries(alpha),
    location_latitude DOUBLE PRECISION NOT NULL,
    location_longitude DOUBLE PRECISION NOT NULL,
    company_id UUID NOT NULL REFERENCES companies(id),
    company_ownership BOOLEAN,
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);


-- This is meant for connections like introductions or historical uses
CREATE TABLE connection_statuses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    status_name VARCHAR(20) NOT NULL,
    status_description VARCHAR(250) NOT NULL,
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- Defines all allowed connections between entities origin/target types should only be contact or company
CREATE TABLE connection_types (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    connection_name VARCHAR(20) NOT NULL UNIQUE,
    type_description VARCHAR(250) NOT NULL UNIQUE,
    origin_type TEXT NOT NULL,
    target_type TEXT NOT NULL,
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- Defines the connections
CREATE TABLE connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    connection_type UUID NOT NULL REFERENCES connection_types(id),
    origin UUID NOT NULL,
    target UUID NOT NULL,
    connection_description TEXT,
    status UUID NOT NULL REFERENCES connection_statuses(id),
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- Used for commenting on connections
CREATE TABLE connection_notes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    connection_id UUID  REFERENCES connections(id),
    note_title VARCHAR(140) NOT NULL,
    note_message TEXT NOT NULL,
    author_id UUID  REFERENCES team_members(id),
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);


-- Defines allowed product categories like "Software"
CREATE TABLE product_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_category TEXT NOT NULL UNIQUE,
    category_description TEXT NOT NULL UNIQUE,
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- Defines allowed product subcategories like "TMS"
CREATE TABLE product_subcategories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    parent_category TEXT NOT NULL REFERENCES product_categories(product_category),
    product_subcategory TEXT NOT NULL UNIQUE,
    subcategory_description TEXT NOT NULL UNIQUE,
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);

-- Represents allowed product types
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_subcategory TEXT NOT NULL UNIQUE,
    product_name TEXT NOT NULL UNIQUE,
    product_description TEXT,
    provider_company UUID REFERENCES companies(id),
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);


-- Represents products/services and who uses them
CREATE TABLE product_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL REFERENCES products(id),
    user_company UUID NOT NULL REFERENCES companies(id),
    created TIMESTAMPTZ DEFAULT NOW(),
    updated TIMESTAMPTZ DEFAULT NOW()
);