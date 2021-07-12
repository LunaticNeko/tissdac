# tissdac - Thai Secondary School Data Cleanup Project

## Introduction

We need some data from Thai secondary schools, but the Education Management
Information System isn't very cooperative in coughing up employment data, which
is actually public but isn't in any sort of open data tables.

The employment data is necessary for determining the number of sample size for
subsequent projects. We need to know exactly how many executive administrators
(principals, etc.) each school has.

Hence the scrapefest.

Furthermore, the school area system has recently changed from the old 42 area
system into the new 62 area system. EMIS however hasn't updated its internal
database to the new system yet, so we also need to do the mapping.

## Usage Instructions

FOR DATA USERS: JUST GO TO data OR reports DIRECTORIES.

You probably don't need to run any of this.

This repo is a bunch of scripts that should be executed in order.

We have designed this project so that the data processing is as transparent as
possible. We try to retain the original blobs of data whenever possible and
programmatically process from it.

1. generate\_province\_codes.py
2. generate\_old\_area\_code\_list.py
3. generate\_school\_table.py
4. generate\_revised\_school\_table.py (this maps the data from old to new
   school area system)
5. scrape\_school\_data.py (this is the fun part, requires Internet connection)
6. summarize\_data.py

## Author

* Chawanat Nakasan, Kanazawa University [Corresponding Author]  
  firstname@staff.kanazawa-u.ac.jp (GitHub: @LunaticNeko)
* Suthon Wongdaeng, Chandrakasem Rajabhat University
* Nataya Nakasan, Chandrakasem Rajabhat University [Principal Investigator]

## Funding

This dataset was created as part of the Specialized Project to Study and Store
Education Management Data of Middle School Teachers to Update and Maintain the
Database and Data Analysis System towards Education and Human Development
Strategy.

Funding Provider (employer): Office of the Education Council (ONEC), Thailand.

Contract Number 18/2564, signed 28 June, 2564 B.E.

## License & Legals

Code is released under MIT License. See LICENSE file for details.

School data was pulled from the Education Management Information System (EMIS),
which is operated by the Office of the Basic Education Commission (OBEC),
Ministry of Education. EMIS itself is maintained by Sumphan Phanphim, Specialist
Analyst affiliated with Nongkhai Primary Educational Service Area Office 2. This
dataset is not endorsed by officials at EMIS, OBEC, or Nongkhai PESA 2.

Provice and district codes come from Bank of Thailand data. (C.N. attempted to
find Ministry of Interior data, but could not find one.)

## Disclaimer

Kanazawa University does not have administrative oversight over this project and
does not endorse the academic views of C.N.

C.N. attests that there is no confidential information in this dataset.

