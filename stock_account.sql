--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.1
-- Dumped by pg_dump version 9.5.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

--
-- Data for Name: stock_account; Type: TABLE DATA; Schema: public; Owner: lxq
--

COPY stock_account (trading_date, personal_new, company_new, personal_total_a, personal_total_b, company_total_a, company_total_b, position_a, position_b, trading_a, trading_b) FROM stdin;
2016-03-07	46.0600000000000023	0.0700000000000000067	10097.4899999999998	238.189999999999998	26.7399999999999984	2.33999999999999986	5030.22000000000025	104.969999999999999	1773.94000000000005	7.75
2016-02-22	35.5499999999999972	0.0700000000000000067	10009.0400000000009	238.139999999999986	26.5899999999999999	2.33999999999999986	5016.92000000000007	104.849999999999994	1522.25	7.48000000000000043
2015-08-10	26.4600000000000009	0.0800000000000000017	9196.52000000000044	236.879999999999995	24.3900000000000006	2.39000000000000012	5020.84000000000015	106.290000000000006	2338.15999999999985	16.7399999999999984
2016-02-01	35.3900000000000006	0.100000000000000006	9947.25	238.080000000000013	26.4400000000000013	2.33999999999999986	5032.64999999999964	104.650000000000006	1622.78999999999996	8.76999999999999957
2016-02-29	42.2899999999999991	0.0700000000000000067	10051.3799999999992	238.169999999999987	26.6600000000000001	2.33999999999999986	5044.42000000000007	104.75	1785.20000000000005	8.80000000000000071
2016-02-08	26.1499999999999986	0.0800000000000000017	9973.45999999999913	238.110000000000014	26.5199999999999996	2.33999999999999986	5003.02000000000044	104.769999999999996	1313.52999999999997	6.25999999999999979
2016-01-25	36.240000000000002	0.0899999999999999967	9911.79000000000087	238.060000000000002	26.3299999999999983	2.35000000000000009	5044.19999999999982	104.569999999999993	1610.25999999999999	8.82000000000000028
2016-01-18	33.1300000000000026	0.0800000000000000017	9875.38999999999942	238.030000000000001	26.2399999999999984	2.35000000000000009	5041	104.290000000000006	1897.07999999999993	11.75
2016-01-11	29.9499999999999993	0.0899999999999999967	9842.20000000000073	237.960000000000008	26.1600000000000001	2.35000000000000009	5032.90999999999985	103.790000000000006	2124.4699999999998	13.1199999999999992
2016-01-04	19.3200000000000003	0.0500000000000000028	9812.13999999999942	237.849999999999994	26.0599999999999987	2.35000000000000009	5026.27999999999975	103.549999999999997	1928.63000000000011	16.129999999999999
2015-12-28	30.5599999999999987	0.0299999999999999989	9792.20999999999913	237.75	26.0100000000000016	2.35000000000000009	5026.81999999999971	103.969999999999999	2243.69999999999982	14.8200000000000003
2015-12-21	32.4500000000000028	0.0899999999999999967	9760.86000000000058	237.650000000000006	25.9299999999999997	2.39999999999999991	5022.27999999999975	104.370000000000005	2118.19999999999982	11.7899999999999991
2015-12-14	34.8800000000000026	0.100000000000000006	9728.04000000000087	237.610000000000014	25.8399999999999999	2.41000000000000014	5047.97000000000025	104.540000000000006	2057.9699999999998	11.4499999999999993
2015-12-07	33.8599999999999994	0.119999999999999996	9692.72999999999956	237.52000000000001	25.7300000000000004	2.39999999999999991	5039.46000000000004	104.769999999999996	2236.42000000000007	12.2400000000000002
2015-11-30	36	0.149999999999999994	9658.80999999999949	237.490000000000009	25.6099999999999994	2.39999999999999991	5013	104.760000000000005	2486.65999999999985	10.6400000000000006
2015-11-23	35.8200000000000003	0.110000000000000001	9622.42000000000007	237.449999999999989	25.4499999999999993	2.39999999999999991	4998.85000000000036	105.459999999999994	2381.2199999999998	8.83000000000000007
2015-11-16	35.2700000000000031	0.0899999999999999967	9586.55999999999949	237.409999999999997	25.3399999999999999	2.39999999999999991	4962.17000000000007	105.5	2555.46000000000004	10.2100000000000009
2015-11-09	29.9200000000000017	0.100000000000000006	9551.27000000000044	237.360000000000014	25.25	2.39999999999999991	4947.52000000000044	105.790000000000006	2357.61000000000013	10.0199999999999996
2015-11-02	33.6400000000000006	0.0899999999999999967	9521.30999999999949	237.310000000000002	25.1499999999999986	2.39999999999999991	4995.77000000000044	105.849999999999994	2242	9.82000000000000028
2015-10-26	32.9600000000000009	0.0700000000000000067	9487.63999999999942	237.280000000000001	25.0599999999999987	2.39999999999999991	4959.89000000000033	105.920000000000002	2330.84999999999991	10.2699999999999996
2015-10-19	29.4699999999999989	0.0800000000000000017	9454.65999999999985	237.240000000000009	24.9899999999999984	2.39999999999999991	4946.64000000000033	106.170000000000002	2194.15000000000009	9.65000000000000036
2015-10-12	10.3399999999999999	0.0200000000000000004	9425.17000000000007	237.199999999999989	24.9100000000000001	2.39999999999999991	4988.23999999999978	106.430000000000007	1266.16000000000008	4.01999999999999957
2015-10-05	13.8399999999999999	0.0299999999999999989	9414.81999999999971	237.189999999999998	24.879999999999999	2.39000000000000012	5018.07999999999993	106.409999999999997	1240.07999999999993	4.53000000000000025
2015-09-28	26.7699999999999996	0.0700000000000000067	9400.96999999999935	237.169999999999987	24.8500000000000014	2.39000000000000012	5023.05000000000018	106.430000000000007	1840.57999999999993	6.54999999999999982
2015-09-21	28.0399999999999991	0.0599999999999999978	9374.18000000000029	237.129999999999995	24.7899999999999991	2.39000000000000012	5028.69999999999982	106.560000000000002	1952.04999999999995	7.48000000000000043
2015-09-14	29.5599999999999987	0.0700000000000000067	9346.11000000000058	237.099999999999994	24.7300000000000004	2.39000000000000012	5050.32999999999993	106.650000000000006	1963.67000000000007	7.73000000000000043
2015-09-07	19.8999999999999986	0.0299999999999999989	9316.53000000000065	237.060000000000002	24.6600000000000001	2.39000000000000012	5062.31999999999971	106.569999999999993	1875.8900000000001	6.03000000000000025
2015-08-31	35.0399999999999991	0.0800000000000000017	9296.60000000000036	237.030000000000001	24.620000000000001	2.39000000000000012	5097.85999999999967	106.450000000000003	2590.26999999999998	16.2699999999999996
2015-08-24	32.8900000000000006	0.0800000000000000017	9261.54999999999927	237	24.5500000000000007	2.39000000000000012	5075.31999999999971	106.159999999999997	3368.36999999999989	25.9800000000000004
2015-08-17	32.0799999999999983	0.0800000000000000017	9228.6200000000008	236.939999999999998	24.4600000000000009	2.39000000000000012	4988.53999999999996	106.120000000000005	2796.42000000000007	17.4200000000000017
2015-06-29	49.7899999999999991	0.130000000000000004	8941.64999999999964	236.419999999999987	23.7600000000000016	2.37999999999999989	4975.77999999999975	106.450000000000003	2871.86999999999989	24.8099999999999987
2015-08-03	33.9699999999999989	0.0800000000000000017	9170.04000000000087	236.830000000000013	24.3099999999999987	2.39000000000000012	5065.22999999999956	106.150000000000006	2768.61000000000013	19.7399999999999984
2015-07-27	39.0600000000000023	0.0899999999999999967	9136.04000000000087	236.77000000000001	24.2300000000000004	2.39000000000000012	5033.97999999999956	106.099999999999994	2874.82000000000016	22.3099999999999987
2015-07-20	52.8200000000000003	0.110000000000000001	9096.95000000000073	236.699999999999989	24.1400000000000006	2.39000000000000012	4998.84000000000015	106.840000000000003	3003.13999999999987	35.1700000000000017
2015-07-13	51.1700000000000017	0.130000000000000004	9044.07999999999993	236.599999999999994	24.0300000000000011	2.39000000000000012	4948.32999999999993	106.920000000000002	2765.82000000000016	24.9100000000000001
2015-07-06	51.1499999999999986	0.140000000000000013	8992.86000000000058	236.509999999999991	23.8999999999999986	2.37999999999999989	4986.61999999999989	106.739999999999995	3020.26999999999998	34.9099999999999966
2015-06-22	99.019999999999996	0.170000000000000012	8891.80999999999949	236.310000000000002	23.6400000000000006	2.37999999999999989	4935.36999999999989	106.260000000000005	3478.59000000000015	26.4499999999999993
2015-06-15	141.189999999999998	0.160000000000000003	8792.70000000000073	236.090000000000003	23.4600000000000009	2.37999999999999989	4833.64999999999964	105.930000000000007	3539.48999999999978	26.7100000000000009
2015-06-08	149.75	0.160000000000000003	8651.3799999999992	235.75	23.3099999999999987	2.37999999999999989	4713.65999999999985	105.700000000000003	3457.17000000000007	23.4899999999999984
2015-06-01	164.280000000000001	0.160000000000000003	8501.47999999999956	235.340000000000003	23.1499999999999986	2.37000000000000011	4564.38000000000011	105.799999999999997	3470.75	24.5
2015-05-25	89.519999999999996	0.140000000000000013	8337.05999999999949	234.840000000000003	22.9899999999999984	2.37000000000000011	4484.64999999999964	105.430000000000007	2916.13999999999987	23.9499999999999993
2015-05-18	79.5799999999999983	0.119999999999999996	8247.43000000000029	234.199999999999989	22.8599999999999994	2.37000000000000011	4467.89000000000033	105.909999999999997	2707.48999999999978	23.75
2015-05-11	81.9500000000000028	0.119999999999999996	8167.75	233.849999999999994	22.7399999999999984	2.37000000000000011	4392.44999999999982	106.239999999999995	2698.17999999999984	19.4499999999999993
\.


--
-- PostgreSQL database dump complete
--
