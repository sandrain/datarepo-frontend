--
-- schema.mariadb.sql
--
-- Initial backend database schema for scalable data intfrastructure.
--

drop table if exists doi_author;
drop table if exists doi_record;
drop table if exists sys_permission;
drop table if exists sys_file;
drop table if exists sys_dataset;
drop table if exists sys_user;

------------------------------------------------------------------------------
-- User account releated tables: 
--
-- sys_user
--
-- TODO: what should be here if we authenticate with globus?
--
------------------------------------------------------------------------------

-- sys_user
-- we should be adding more fields, e.g., globus information, xcams, etc.
create table sys_user (
    id bigint(20) unsigned not null auto_increment,
    email varchar(256) not null,
    primary key (id),
    unique (email)
) engine=InnoDB;

------------------------------------------------------------------------------
-- Dataset related tables:
--
-- sys_dataset
-- sys_file
--
------------------------------------------------------------------------------

-- sys_dataset
-- @uuid can be used for external applications to identify the physical
-- datasets.
create table sys_dataset (
    id bigint(20) unsigned not null auto_increment,
    uuid varchar(36) not null,             -- maybe useful for externally
    owner bigint(20) unsigned not null,    -- owner of the dataset
    public boolean default true,           -- is dataset public?
    size bigint(20) unsigned default 0,    -- total size
    properties json,                       -- metadata from user
    structure json,                        -- directory hierarchy
    primary key (id),
    unique (uuid),
    foreign key (owner) references sys_user (id) on delete cascade
) engine=InnoDB;

-- sys_file
create table sys_file (
    id bigint(20) unsigned not null auto_increment,
    dataset_id bigint(20) unsigned not null, -- dataset this file belongs to
    name varchar(512) not null,              -- file name
    size bigint(20) unsigned default 0,      -- file size
    primary key (id),
    foreign key (dataset_id) references sys_dataset (id) on delete cascade
) engine=InnoDB;

------------------------------------------------------------------------------
-- Dataset sharing:
--
-- sys_permission
--
------------------------------------------------------------------------------

-- sys_permission
-- individually set access permission for non-public datasets
create table sys_permission (
    dataset_id bigint(20) unsigned not null,
    user_id bigint(20) unsigned not null,
    writable boolean default false,
    foreign key (dataset_id) references sys_dataset (id) on delete cascade,
    foreign key (user_id) references sys_user (id) on delete cascade,
    unique (dataset_id, user_id)
);

------------------------------------------------------------------------------
-- DIO releated tables: A subset of datasets will have associated doi records.
--
-- doi_record
-- doi_author
--
------------------------------------------------------------------------------

-- doi_record
-- TODO: almost copied from the constellation repo. any necessary
-- modifications?
create table doi_record (
    id bigint(20) unsigned not null auto_increment,
    dataset_id bigint(20) unsigned not null,
    doi varchar(64) default null,
    suid bigint(20) unsigned not null,
    title text default null,
    keywords text default null,
    description text default null,
    site_url text default null,
    olcf_project_id varchar(8) default null,
    dataset_type varchar(1024) default null,
    subjects text default null,
    product_nos varchar(255) default null,
    doe_contract_nos varchar(255) default null,
    other_contract_nos varchar(255) default null,
    origin_orgs varchar(1024) default 'Oak Ridge National Laboratory',
    sponsor_orgs varchar(1024) default null,
    contrib_orgs varchar(1024) default null,
    software_needed varchar(1024) default null,
    other_id_nos varchar(255) default null,
    create_time timestamp not null default current_timestamp(),
    publish_time timestamp null default null,
    language char(8) default 'English',
    country char(2) default 'US',
    doi_infix char(8) default 'OLCF',
    contact_name varchar(64) default 'Sudharshan Vazhkudai',
    contact_org varchar(64) default 'ORNL-OLCF',
    contact_email varchar(255) default 'olcf-doi-admin@email.ornl.gov',
    contact_phone char(32) default '865-576-5547',
    request_status
        enum('INITIAL','SUBMITTED','PENDING','REVIEWING',
  	         'ACCEPTED','ISSUE_FAILED','REJECTED','ISSUED') default 'INITIAL',
    data_status
        enum('NOT_INITIATED','PROGRESS','COMPLETE','PENDING_DELETE','DELETED',
  	         'PENDING_ARCHIVE','ARCHIVED') default 'NOT_INITIATED',
    admin_suid bigint(20) unsigned default null,
    admin_comments text default null,
    PRIMARY KEY (id),
    foreign key (dataset_id) references sys_dataset (id) on delete cascade
) engine=InnoDB;

-- doi_author
-- TODO: almost copied from the constellation repo. any necessary
-- modifications?
create table doi_author (
    id bigint(20) unsigned not null auto_increment,
    doi_record_id bigint(20) unsigned NOT NULL ,
    user_id bigint(20) unsigned not null,
    first_name varchar(255) default null,
    middle_name varchar(255) default '',
    last_name varchar(255) default null,
    email varchar(255) default '',
    organization varchar(255) default '',
    primary key (id),
    foreign key (doi_record_id) references doi_record (id) on delete cascade,
    foreign key (user_id) references sys_user (id) on delete cascade
) engine=InnoDB;

