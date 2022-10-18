
--
-- TABLE flights
-- Stores flight information
--
CREATE TABLE flights
(
  flight_id SERIAL PRIMARY KEY,
  root_folder text,
  location text,
  srid integer NOT NULL,
  date_time timestamp with time zone
);
ALTER TABLE flights OWNER TO arcstandard;

--
-- TABLE images
-- Stores image information
--
CREATE TABLE images
(
  image_id SERIAL PRIMARY KEY,
  flight_id integer REFERENCES flights(flight_id),
  path text,
  low_quality_jpg text,
  high_quality_jpg text,
  date_time timestamp with time zone,
  nadir boolean,
  geom geometry,
  -- Ensure that one of the paths is set
  CONSTRAINT enforce_some_path CHECK (path is not null or
    low_quality_jpg is not null or high_quality_jpg is not null),
  CONSTRAINT enforce_dims_geom CHECK (st_ndims(geom) = 2),
  CONSTRAINT enforce_type_geom CHECK (st_geometrytype(geom) = 'ST_Polygon')
  -- There can be multiple SRIDs in this table.  You must be sure to limit
  -- queries to records with the same SRID to avoid 'mixed SRID' errors.
);
ALTER TABLE images OWNER TO arcstandard;

--
-- TABLE targets
-- Stores target geom and caracteristics
-- Child tables dynamically created for each SRID
--
CREATE TABLE targets
(
  target_id SERIAL PRIMARY KEY,
  flight_id integer REFERENCES flights(flight_id),
  image_id integer REFERENCES images(image_id),
  target_type integer,
  letter text,
  shape text,
  background_color text,
  letter_color text,
  orientation integer,
  notes text,
  geom geometry,
  thumbnail text,
  manual boolean,
  CONSTRAINT enforce_dims_geom CHECK (st_ndims(geom) = 2),
  CONSTRAINT enforce_type_geom CHECK (st_geometrytype(geom) = 'ST_MultiPoint')
  -- There can be multiple SRIDs in this table.  You must be sure to limit
  -- queries to records with the same SRID to avoid 'mixed SRID' errors.
);
ALTER TABLE targets OWNER TO arcstandard;

ALTER TABLE geometry_columns OWNER TO arcstandard;
ALTER TABLE spatial_ref_sys OWNER TO arcstandard;

--
-- TABLE target_regions
-- Stores target regions inside individual images
--
CREATE TABLE target_regions
(
  target_region_id SERIAL PRIMARY KEY,
  flight_id integer REFERENCES flights(flight_id),
  image_id integer REFERENCES images(image_id),
  target_id integer REFERENCES targets(target_id),
  point1 integer[],
  point2 integer[],
  manual boolean
);
ALTER TABLE target_regions OWNER TO arcstandard;
