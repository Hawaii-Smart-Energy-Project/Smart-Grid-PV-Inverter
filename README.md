Smart-Grid-PV-Inverter
======================

Data Science Software for the Smart Grid PV Inverter Project.

Source data is at one-second resolution measuring at least 58 different values
over 21 separate meters.

This software provides loading of this data to a PostgreSQL database using
parallel insertion to a set of table partitions where one partition is assigned
to each meter.

The source data contains

* duplicate records
* incomplete records
* corrupted values

These items are not loaded to the production data set. In the case of duplicate
records, the last occurring record, in a source data set, is retained.

## Installation

TBW

### External Dependencies

* [Smart Energy Kit](https://github.com/Hawaii-Smart-Energy-Project/Smart-Energy-Kit)

## Configuration

TBW

## Data Loading

Data loading is accomplished using

    $ python insertMultiMeterDataFile.py --basepath ${FULL_PATH_TO_DATA}

### Debugging Data Loading Problems

The most likely reason for data loading to fail is when an exception occurs
within the worker process for loading a single file. Another possibility is
that bad data cannot be determined by `SIDataUtil.badData`.

A count of the exceptions that have occurred during loading is maintained in the
multi file loader.
