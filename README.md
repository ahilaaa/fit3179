# fit3179
DATA SOURCES !!

main dataset #1: suburbs/geological: https://www.matthewproctor.com/

main data set #2: income : https://data.gov.au/data/dataset/taxation-statistics-2021-22/resource/9bd9d5af-2c09-405f-b484-69c862f4dc2e

main data set #3: obesity : https://www.vu.edu.au/mitchell-institute/australian-health-tracker-series/obesity-rate-depends-on-where-you-live

topojson data set #4: Victoria : https://data.gov.au/dataset/ds-dga-bdf92691-c6fe-42b9-a0e2-a4cd716fa811/details



Rough Procedure

merge suburbs with income -> income information by suburbs
retrieve all locations of fast food using google maps api, then use geocoding python api to retrieve suburb from lat,lng coordinates
then map suburbs of fast food -> income information by suburbs

etc...



DATA SCRUBBING ISSUES AND MINOR CONCERNS !!

Council - Obesity and Council - Income have SLIGHT variations in spelling (e.g Casey vs Casey - North and Casey - South). Obesity data (ABS national survey) has its own variation in council classification which is different to the Suburbs Data (mathew proctor)

Vic-Table 1 Council names have been modified slightly:
- assume Grampians = Southern Grampians and Northern Grampians (using same ASR rates)
- Colac Otaway -> Colac - Otoway
- Casey - North,Casey - South --> Casey (data has been aggregated)

- data source has different definitions of which council matches which suburb , e.g suburb ARARAT is located in council gippsland??
- Merged Council has small councils removed (population = 1000)




