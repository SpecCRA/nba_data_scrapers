# Basketball-Reference Data Webscraper

## Summary

* This script scrapes datafrom [basketball-reference.com](https://www.basketball-reference.com/). The script outputs data with at start year to an end year of the user's choice in a `csv` file. 

## Use

* Run the `.py` script in console or `.ipynb` notebook file in Jupyter Notebook and proceed to enter your start and end years in `YYYY` format. 
* `player_data_1981-2017.csv` is an example file for data ranging from 1981 to 2017. 

## Things that still require attention
* Players on different teams in one season are listed as TOT (Tm). Separations have not been addressed, and I do not intend to address them right now. I do not have a good way to address this right now as it affects querying. 
* Players who have played an equal number of two positions only get one. I have not worked out a way to resolve this yet. For example, if Tim Duncan plays 9 seasons at PF and 9 seasons at C, I don't know how to properly address this yet.
* An updater script to add to csv files would be nice.

## Notes
* Please see [this page](https://www.basketball-reference.com/about/glossary.html) for a glossary of terms. 
* Tim Duncan will be considered a center depending on your time frame. He has 10 entries at C and 9 at PF. This should be addressed because the Spurs adamently refused to list him at center for the longest time.
* Rounded_Pos equates PG:1, SG:2, SF:3, PF:4, C:5. The column takes the most commonly played position by the player in your year range and assigns a 1-5 value.  
* I have chosen to keep asterisks in player names to maintain a notation for Hall of Fame players. 