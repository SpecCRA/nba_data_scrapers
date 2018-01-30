# NBA Data IPython Notebook 

## Summary

* All data scraped from basketball-reference.com. The script outputs data with at start year to an end year of the user's choice. 

## Use

* Opening `bref_player_stats_scraper.py` file, go to line 233. 
* Change the years according to the seasons range you desire. For instance, inputting 2012, 2015 will output data starting in the 2011-12, 2012-13, 2013-14, and 2014-15 seasons.
* `bref_1981_2017_player_data.csv` is an example csv file with data starting in the 1980-81 season up until the 2016-17 season.

## Things that still require attention
* Combination positions need to be addressed. Example: Cliff Robinson has some listed as C and some listed as C-PF.
* Some players have different positions in different years. I plan on giving them a new column with a rounded position (1-5), preserving different positions played in different seasons and combination positions.
* Players on different teams in one season are listed as TOT (Tm). Separations have not been addressed, and I do not intend to address them right now. I may create a different version for this feature if I need it later.
* An updater script to add to csv files would be nice.
* Start and end years should be inputted 