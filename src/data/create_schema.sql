-- NOTE: THIS IS JUST THE STEPS PERFORMED
-- WILL NEED FIXING TO RUN

CREATE SCHEMA buildingonsand
    AUTHORIZATION buildingonsand;

-- Change to use schema

--
CREATE TABLE buildingonsand."CVE"
(
    "NAME" character varying,
    "STATUS" character varying,
    "DESCRIPTION" character varying,
    "REFERENCES" character varying,
    "PHASE" character varying,
    "VOTES" character varying,
    "COMMENTS" character varying,
    "DATE_REGISTERED" date,
    PRIMARY KEY ("NAME")
);

ALTER TABLE IF EXISTS buildingonsand."CVE"
    OWNER to buildingonsand;

-- Table: buildingonsand.RELEASES

-- DROP TABLE IF EXISTS buildingonsand."RELEASES";

CREATE TABLE IF NOT EXISTS buildingonsand."RELEASES"
(
    "ID" character varying COLLATE pg_catalog."default",
    "VERSION" character varying COLLATE pg_catalog."default",
    "COMPONENT" character varying COLLATE pg_catalog."default",
    "RELEASE_DATE" date,
    "SUPPORT_END_DATE" date,
    "OSS_SUPPORT_END_DATE" date
);

-- Table: buildingonsand.RELEASE_CVE

-- DROP TABLE IF EXISTS buildingonsand."RELEASE_CVE";


CREATE TABLE IF NOT EXISTS buildingonsand."RELEASE_CVE"
(
    "RELEASE_NAME" character varying COLLATE pg_catalog."default" NOT NULL,
    "CVE" character varying COLLATE pg_catalog."default" NOT NULL,
    "TITLE" character varying COLLATE pg_catalog."default",
    "DESCRIPTION" character varying COLLATE pg_catalog."default",
    "CVSS_SCORE" character varying COLLATE pg_catalog."default",
    "CWE" character varying COLLATE pg_catalog."default",
    "REFERENCE" character varying COLLATE pg_catalog."default",
    "YEAR" integer,
    CONSTRAINT "RELEASE_CVE_pkey" PRIMARY KEY ("RELEASE_NAME", "CVE")
)

    TABLESPACE pg_default;

ALTER TABLE IF EXISTS buildingonsand."RELEASE_CVE"
    OWNER to buildingonsand;


-- Queries
select * from buildingonsand."RELEASES"
order by "RELEASE_DATE"

select * from buildingonsand."RELEASES"

select "SOFTWARE_VERSION" from buildingonsand."RELEASES"
where "RELEASE_DATE" < '2022-07-09'
order by string_to_array("SOFTWARE_VERSION", '.')::int[]

select "COMPONENT","SOFTWARE_VERSION","OSS_SUPPORT_END_DATE" from  buildingonsand."RELEASES"
                                                                       Join (
    select "COMPONENT" as c1, MAX("SOFTWARE_VERSION") as v1  from buildingonsand."RELEASES"
    where "RELEASE_DATE" < '2022-01-01'
    group by "COMPONENT"
) as cs
on cs.c1 = "COMPONENT" and cs.v1 = "SOFTWARE_VERSION"