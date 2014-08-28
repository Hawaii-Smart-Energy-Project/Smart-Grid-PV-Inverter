# Load meter data sequentially.
#
# @author Daniel Zhang (張道博)

METERS=(001EC605195B 001EC6051A10 001EC6051E14 001EC60519F6 001EC6051A1D 001EC6051A1C)

for meter in ${METERS[@]}; do
    time insertMultiMeterDataFile.py --basepath ~/smb-share/1.Projects/1.14.SmartInverter/InverterMeterData/$meter/ --process_count 2
done
