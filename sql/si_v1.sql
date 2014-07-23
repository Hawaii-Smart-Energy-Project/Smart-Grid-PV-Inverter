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
    meter_name text
);


ALTER TABLE public."Meters" OWNER TO sepgroup;

--
-- Data for Name: MeterData; Type: TABLE DATA; Schema: public; Owner: sepgroup
--

COPY "MeterData" (meter_id, time_utc, error, lowalarm, highalarm, "Accumulated Real Energy Net (kWh)", "Real Energy Quadrants 1 & 4, Import (kWh)", "Real Energy Quadrants 2 & 3, Export (kWh)", "Reactive Energy Quadrant 1 (VARh)", "Reactive Energy Quadrant 2 (VARh)", "Reactive Energy Quadrant 3 (VARh)", "Reactive Energy Quadrant 4 (VARh)", "Apparent Energy Net (VAh)", "Apparent Energy Quadrants 1 & 4 (VAh)", "Apparent Energy Quadrants 2 & 3 (VAh)", "Total Net Instantaneous Real Power (kW)", "Total Net Instantaneous Reactive Power (kVAR)", "Total Net Instantaneous Apparent Power (kVA)", "Total Power Factor", "Voltage, L-L, 3p Ave (Volts)", "Voltage, L-N, 3p Ave (Volts)", "Current, 3p Ave (Amps)", "Frequency (Hz)", "Total Real Power Present Demand (kW)", "Total Reactive Power Present Demand (kVAR)", "Total Apparent Power Present Demand (kVA)", "Total Real Power Max Demand, Import (kW)", "Total Reactive Power Max Demand, Import (kVAR)", "Total Apparent Power Max Demand, Import (kVA)", "Total Real Power Max Demand, Export (kW)", "Total Reactive Power Max Demand, Export (kVAR)", "Total Apparent Power Max Demand, Export (kVA)", "Accumulated Real Energy, Phase A, Import (kW)", "Accumulated Real Energy, Phase B, Import (kW)", "Accumulated Real Energy, Phase C, Import (kW)", "Accumulated Real Energy, Phase A, Export (kW)", "Accumulated Real Energy, Phase B, Export (kW)", "Accumulated Real Energy, Phase C, Export (kW)", "Accumulated Q1 Reactive Energy, Phase A, Import (VARh)", "Accumulated Q1 Reactive Energy, Phase B, Import (VARh)", "Accumulated Q1 Reactive Energy, Phase C, Import (VARh)", "Accumulated Q2 Reactive Energy, Phase A, Import (VARh)", "Accumulated Q2 Reactive Energy, Phase B, Import (VARh)", "Accumulated Q2 Reactive Energy, Phase C, Import (VARh)", "Accumulated Q3 Reactive Energy, Phase A, Export (VARh)", "Accumulated Q3 Reactive Energy, Phase B, Export (VARh)", "Accumulated Q3 Reactive Energy, Phase C, Export (VARh)", "Accumulated Q4 Reactive Energy, Phase A, Export (VARh)", "Accumulated Q4 Reactive Energy, Phase B, Export (VARh)", "Accumulated Q4 Reactive Energy, Phase C, Export (VARh)", "Accumulated Apparent Energy, Phase A, Import (VAh)", "Accumulated Apparent Energy, Phase B, Import (VAh)", "Accumulated Apparent Energy, Phase C, Import (VAh)", "Accumulated Apparent Energy, Phase A, Export (VAh)", "Accumulated Apparent Energy, Phase B, Export (VAh)", "Accumulated Apparent Energy, Phase C, Export (VAh)", "Real Power, Phase A (kW)", "Real Power, Phase B (kW)", "Real Power, Phase C (kW)", "Reactive Power, Phase A (kVAR)", "Reactive Power, Phase B (kVAR)", "Reactive Power, Phase C (kVAR)", "Apparent Power, Phase A (kVA)", "Apparent Power, Phase B (kVA)", "Apparent Power, Phase C (kVA)", "Power Factor, Phase A", "Power Factor, Phase B", "Power Factor, Phase C", "Voltage, Phase A-B (Volts)", "Voltage, Phase B-C (Volts)", "Voltage, Phase A-C (Volts)", "Voltage, Phase A-N (Volts)", "Voltage, Phase B-N (Volts)", "Voltage, Phase C-N (Volts)", "Current, Phase A (Amps)", "Current, Phase B (Amps)", "Current, Phase C (Amps)") FROM stdin;
\.


--
-- Data for Name: Meters; Type: TABLE DATA; Schema: public; Owner: sepgroup
--

COPY "Meters" (meter_id, meter_name) FROM stdin;
\.


--
-- Name: meter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sepgroup
--

SELECT pg_catalog.setval('meter_id_seq', 1, false);


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

