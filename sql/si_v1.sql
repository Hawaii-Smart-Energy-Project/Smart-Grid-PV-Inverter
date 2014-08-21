--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: MeterData; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "MeterData" (
    meter_id integer NOT NULL,
    time_utc timestamp without time zone NOT NULL,
    error integer,
    lowalarm text,
    highalarm text,
    "Accumulated Real Energy Net (kWh)" real,
    "Real Energy Quadrants 1 & 4, Import (kWh)" real,
    "Real Energy Quadrants 2 & 3, Export (kWh)" real,
    "Reactive Energy Quadrant 1 (VARh)" real,
    "Reactive Energy Quadrant 2 (VARh)" real,
    "Reactive Energy Quadrant 3 (VARh)" real,
    "Reactive Energy Quadrant 4 (VARh)" real,
    "Apparent Energy Net (VAh)" real,
    "Apparent Energy Quadrants 1 & 4 (VAh)" real,
    "Apparent Energy Quadrants 2 & 3 (VAh)" real,
    "Total Net Instantaneous Real Power (kW)" real,
    "Total Net Instantaneous Reactive Power (kVAR)" real,
    "Total Net Instantaneous Apparent Power (kVA)" real,
    "Total Power Factor" real,
    "Voltage, L-L, 3p Ave (Volts)" real,
    "Voltage, L-N, 3p Ave (Volts)" real,
    "Current, 3p Ave (Amps)" real,
    "Frequency (Hz)" real,
    "Total Real Power Present Demand (kW)" real,
    "Total Reactive Power Present Demand (kVAR)" real,
    "Total Apparent Power Present Demand (kVA)" real,
    "Total Real Power Max Demand, Import (kW)" real,
    "Total Reactive Power Max Demand, Import (kVAR)" real,
    "Total Apparent Power Max Demand, Import (kVA)" real,
    "Total Real Power Max Demand, Export (kW)" real,
    "Total Reactive Power Max Demand, Export (kVAR)" real,
    "Total Apparent Power Max Demand, Export (kVA)" real,
    "Accumulated Real Energy, Phase A, Import (kW)" real,
    "Accumulated Real Energy, Phase B, Import (kW)" real,
    "Accumulated Real Energy, Phase C, Import (kW)" real,
    "Accumulated Real Energy, Phase A, Export (kW)" real,
    "Accumulated Real Energy, Phase B, Export (kW)" real,
    "Accumulated Real Energy, Phase C, Export (kW)" real,
    "Accumulated Q1 Reactive Energy, Phase A, Import (VARh)" real,
    "Accumulated Q1 Reactive Energy, Phase B, Import (VARh)" real,
    "Accumulated Q1 Reactive Energy, Phase C, Import (VARh)" real,
    "Accumulated Q2 Reactive Energy, Phase A, Import (VARh)" real,
    "Accumulated Q2 Reactive Energy, Phase B, Import (VARh)" real,
    "Accumulated Q2 Reactive Energy, Phase C, Import (VARh)" real,
    "Accumulated Q3 Reactive Energy, Phase A, Export (VARh)" real,
    "Accumulated Q3 Reactive Energy, Phase B, Export (VARh)" real,
    "Accumulated Q3 Reactive Energy, Phase C, Export (VARh)" real,
    "Accumulated Q4 Reactive Energy, Phase A, Export (VARh)" real,
    "Accumulated Q4 Reactive Energy, Phase B, Export (VARh)" real,
    "Accumulated Q4 Reactive Energy, Phase C, Export (VARh)" real,
    "Accumulated Apparent Energy, Phase A, Import (VAh)" real,
    "Accumulated Apparent Energy, Phase B, Import (VAh)" real,
    "Accumulated Apparent Energy, Phase C, Import (VAh)" real,
    "Accumulated Apparent Energy, Phase A, Export (VAh)" real,
    "Accumulated Apparent Energy, Phase B, Export (VAh)" real,
    "Accumulated Apparent Energy, Phase C, Export (VAh)" real,
    "Real Power, Phase A (kW)" real,
    "Real Power, Phase B (kW)" real,
    "Real Power, Phase C (kW)" real,
    "Reactive Power, Phase A (kVAR)" real,
    "Reactive Power, Phase B (kVAR)" real,
    "Reactive Power, Phase C (kVAR)" real,
    "Apparent Power, Phase A (kVA)" real,
    "Apparent Power, Phase B (kVA)" real,
    "Apparent Power, Phase C (kVA)" real,
    "Power Factor, Phase A" real,
    "Power Factor, Phase B" real,
    "Power Factor, Phase C" real,
    "Voltage, Phase A-B (Volts)" real,
    "Voltage, Phase B-C (Volts)" real,
    "Voltage, Phase A-C (Volts)" real,
    "Voltage, Phase A-N (Volts)" real,
    "Voltage, Phase B-N (Volts)" real,
    "Voltage, Phase C-N (Volts)" real,
    "Current, Phase A (Amps)" real,
    "Current, Phase B (Amps)" real,
    "Current, Phase C (Amps)" real
);


ALTER TABLE public."MeterData" OWNER TO sepgroup;

--
-- Name: meter_id_seq; Type: SEQUENCE; Schema: public; Owner: sepgroup
--

CREATE SEQUENCE meter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meter_id_seq OWNER TO sepgroup;

--
-- Name: Meters; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "Meters" (
    meter_id integer DEFAULT nextval('meter_id_seq'::regclass) NOT NULL,
    meter_name text NOT NULL
);


ALTER TABLE public."Meters" OWNER TO sepgroup;

--
-- Name: MeterData_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "MeterData"
    ADD CONSTRAINT "MeterData_pkey" PRIMARY KEY (meter_id, time_utc);


--
-- Name: Meters_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "Meters"
    ADD CONSTRAINT "Meters_pkey" PRIMARY KEY (meter_id);


--
-- Name: unique_meter_name; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "Meters"
    ADD CONSTRAINT unique_meter_name UNIQUE (meter_name);


--
-- Name: Meters_meter_id_key; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX "Meters_meter_id_key" ON "Meters" USING btree (meter_id);


--
-- Name: meter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "MeterData"
    ADD CONSTRAINT meter_id_fkey FOREIGN KEY (meter_id) REFERENCES "Meters"(meter_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

