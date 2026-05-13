-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;

-- DROP SEQUENCE public.ficheros_exportados_id_seq;

CREATE SEQUENCE public.ficheros_exportados_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.ficheros_exportados_id_seq OWNER TO appuser;
GRANT ALL ON SEQUENCE public.ficheros_exportados_id_seq TO appuser;

-- DROP SEQUENCE public.indice_texto_detalle_id_seq;

CREATE SEQUENCE public.indice_texto_detalle_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.indice_texto_detalle_id_seq OWNER TO appuser;
GRANT ALL ON SEQUENCE public.indice_texto_detalle_id_seq TO appuser;

-- DROP SEQUENCE public.indice_texto_id_seq;

CREATE SEQUENCE public.indice_texto_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.indice_texto_id_seq OWNER TO appuser;
GRANT ALL ON SEQUENCE public.indice_texto_id_seq TO appuser;
-- public.allshifts definition

-- Drop table

-- DROP TABLE public.allshifts;

CREATE TABLE public.allshifts (
	id int8 NOT NULL,
	employee_id int8 NOT NULL,
	workplace_id int8 NULL,
	company_id int8 NULL,
	time_settings_break_configuration_id int8 NULL,
	"date" date NOT NULL,
	reference_date date NULL,
	clock_in time NULL,
	clock_out time NULL,
	clock_in_with_seconds time NULL,
	created_at timestamptz NULL,
	updated_at timestamptz NULL,
	in_source varchar(50) NULL,
	out_source varchar(50) NULL,
	in_location_latitude numeric(9, 6) NULL,
	in_location_longitude numeric(9, 6) NULL,
	in_location_accuracy numeric(8, 3) NULL,
	out_location_latitude numeric(9, 6) NULL,
	out_location_longitude numeric(9, 6) NULL,
	out_location_accuracy numeric(8, 3) NULL,
	location_type varchar(50) NULL,
	observations text NULL,
	half_day bool NULL,
	workable bool DEFAULT true NULL,
	minutes int4 NULL,
	CONSTRAINT allshifts_pkey PRIMARY KEY (id)
);
CREATE INDEX idx_company_id ON public.allshifts USING btree (company_id);
CREATE INDEX idx_employee_date ON public.allshifts USING btree (employee_id, date);

-- Permissions

ALTER TABLE public.allshifts OWNER TO appuser;
GRANT ALL ON TABLE public.allshifts TO appuser;


-- public.empleados definition

-- Drop table

-- DROP TABLE public.empleados;

CREATE TABLE public.empleados (
	id int8 NOT NULL,
	access_id int8 NULL,
	first_name text NULL,
	last_name text NULL,
	full_name text NULL,
	preferred_name text NULL,
	birth_name text NULL,
	gender text NULL,
	identifier text NULL,
	identifier_type text NULL,
	email text NULL,
	login_email text NULL,
	birthday_on date NULL,
	nationality text NULL,
	address_line_1 text NULL,
	address_line_2 text NULL,
	postal_code text NULL,
	city text NULL,
	state text NULL,
	country text NULL,
	bank_number text NULL,
	swift_bic text NULL,
	bank_number_format text NULL,
	company_id int8 NULL,
	legal_entity_id int8 NULL,
	location_id int8 NULL,
	created_at timestamp NULL,
	updated_at timestamp NULL,
	social_security_number text NULL,
	is_terminating bool NULL,
	terminated_on date NULL,
	termination_reason_type text NULL,
	termination_reason text NULL,
	termination_observations text NULL,
	manager_id int8 NULL,
	timeoff_manager_id int8 NULL,
	phone_number text NULL,
	company_identifier text NULL,
	age_number int4 NULL,
	termination_type_description text NULL,
	contact_name text NULL,
	contact_number text NULL,
	personal_email text NULL,
	seniority_calculation_date date NULL,
	pronouns text NULL,
	active bool NULL,
	disability_percentage_cents int4 NULL,
	identifier_expiration_date date NULL,
	attendable bool NULL,
	country_of_birth text NULL,
	birthplace text NULL,
	raw_json jsonb NULL,
	CONSTRAINT empleados_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE public.empleados OWNER TO appuser;
GRANT ALL ON TABLE public.empleados TO appuser;


-- public.ficheros_exportados definition

-- Drop table

-- DROP TABLE public.ficheros_exportados;

CREATE TABLE public.ficheros_exportados (
	id serial4 NOT NULL,
	nombre_fichero text NULL,
	fecha_exportacion timestamp DEFAULT now() NOT NULL,
	CONSTRAINT ficheros_exportados_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE public.ficheros_exportados OWNER TO appuser;
GRANT ALL ON TABLE public.ficheros_exportados TO appuser;


-- public.indice_texto definition

-- Drop table

-- DROP TABLE public.indice_texto;

CREATE TABLE public.indice_texto (
	id serial4 NOT NULL,
	nombre_archivo text NULL,
	num_linea int4 NULL,
	contenido text NULL,
	CONSTRAINT indice_texto_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE public.indice_texto OWNER TO appuser;
GRANT ALL ON TABLE public.indice_texto TO appuser;


-- public.indice_texto_detalle definition

-- Drop table

-- DROP TABLE public.indice_texto_detalle;

CREATE TABLE public.indice_texto_detalle (
	id serial4 NOT NULL,
	nombre_archivo text NULL,
	num_linea int4 NULL,
	datetime text NULL,
	dni text NULL,
	num_empleado text NULL,
	maquina text NULL,
	codigo text NULL,
	codificado text NULL,
	exportado int4 DEFAULT 0 NOT NULL,
	CONSTRAINT indice_texto_detalle_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE public.indice_texto_detalle OWNER TO appuser;
GRANT ALL ON TABLE public.indice_texto_detalle TO appuser;




-- Permissions

GRANT ALL ON SCHEMA public TO pg_database_owner;
GRANT USAGE ON SCHEMA public TO public;