# Send the class reservations calendar to the client

## Description

As an Operator, I want to send the reservations calendar to a client, for a
given range of dates.

The calendar must be in ics format, and must include all the available
reservations in the given range of dates.

The reservations in the calendar must include:

- The client's name
- The class slot name
- The class slot date
- The reserved equipment

The calendar can be downloaded as an ics file, with the file name:
cal_<client_name>_<start_date>_<end_date>.ics

Where:
client_name is the snake_case version of Client's name
start_date and end_date are formatted as YYYYMMDD
