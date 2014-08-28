Smart-Grid-PV-Inverter
======================

Data Science Software for the Smart Grid PV Inverter Project.

Source data is at one-second resolution measuring at least 58 different values
over 21 separate meters.

This software provides loading of this data to a PostgreSQL database using
multicore insertion to a set of table partitions where one partition is assigned
to each meter.
