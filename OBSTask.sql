--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1
-- Dumped by pg_dump version 14.1

-- Started on 2022-01-01 13:27:30

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3318 (class 1262 OID 16394)
-- Name: orange; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE orange WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_United States.1252';


ALTER DATABASE orange OWNER TO postgres;

\connect orange

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 212 (class 1259 OID 16407)
-- Name: ip; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ip (
    ip_id integer NOT NULL,
    ip_address text,
    ip_name text,
    is_available smallint,
    subnet_id integer
);


ALTER TABLE public.ip OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 16406)
-- Name: ip_ip_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.ip ALTER COLUMN ip_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.ip_ip_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 209 (class 1259 OID 16400)
-- Name: subnet; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subnet (
    subnet_id integer NOT NULL,
    subnet_value integer NOT NULL,
    vlan integer NOT NULL,
    min integer,
    max integer,
    subnet_name text
);


ALTER TABLE public.subnet OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 16405)
-- Name: subnet_subnet_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.subnet ALTER COLUMN subnet_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.subnet_subnet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 3172 (class 2606 OID 16413)
-- Name: ip ip_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ip
    ADD CONSTRAINT ip_pkey PRIMARY KEY (ip_id);


--
-- TOC entry 3170 (class 2606 OID 16404)
-- Name: subnet subnet_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subnet
    ADD CONSTRAINT subnet_pkey PRIMARY KEY (subnet_id);


--
-- TOC entry 3173 (class 2606 OID 16438)
-- Name: ip ip_subnet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ip
    ADD CONSTRAINT ip_subnet_id_fkey FOREIGN KEY (subnet_id) REFERENCES public.subnet(subnet_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


-- Completed on 2022-01-01 13:27:30

--
-- PostgreSQL database dump complete
--

