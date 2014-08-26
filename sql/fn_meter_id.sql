-- @author Daniel Zhang (張道博)
CREATE OR REPLACE FUNCTION meter_id (name text)
RETURNS integer AS $$
declare
	id integer;
BEGIN
   SELECT meter_id into id FROM "Meters" where meter_name = name;
   RETURN id;
END;
$$ LANGUAGE plpgsql;
