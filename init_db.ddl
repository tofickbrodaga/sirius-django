CREATE SCHEMA IF NOT EXISTS biobase;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS biobase.users (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    login text UNIQUE,
    password text,
    access text
);

CREATE TABLE IF NOT EXISTS biobase.strains (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    UIN text,
    name text,
    pedigree text,
    mutations text,
    transformations text,
    creation_date date,
    created_by uuid REFERENCES biobase.users(id)
);

CREATE TABLE IF NOT EXISTS biobase.strain_processing (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    strain_id uuid REFERENCES biobase.strains(id),
    processing_date date,
    description text,
    responsible uuid REFERENCES biobase.users(id)
);

CREATE TABLE IF NOT EXISTS biobase.substance_identification(
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    strain_id uuid REFERENCES biobase.strains(id),
    identification_date date,
    results text,
    identified_by uuid REFERENCES biobase.users(id)
);

CREATE TABLE IF NOT EXISTS biobase.experiments (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    strain_UIN uuid REFERENCES biobase.strains(id),
    start_date date,
    end_date date,
    growth_medium text,
    results text,
    created_by uuid users REFERENCES biobase.users(id)
);

CREATE TABLE IF NOT EXISTS biobase.cultivation_planning (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    strain_ID uuid,
    planning_date date,
    completion_date date,
    growth_medium text,
    status text,
    started_by uuid REFERENCES biobase.users(id)
);

CREATE TABLE IF NOT EXISTS biobase.projects (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_name text,
    start_date date,
    end_date date,
    results text,
    created_by uuid REFERENCES biobase.users(id)
);

CREATE TABLE IF NOT EXISTS biobase.cultures (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id uuid REFERENCES biobase.projects(id),
    planning_date date,
    results text,
    created_by uuid REFERENCES biobase.users(id)
);