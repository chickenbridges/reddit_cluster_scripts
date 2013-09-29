##What each file is:
* collect_data.py - collects data for random users and stores in *user_dict.dat* pickle file. Run using 'python collect_data.py'
* user_dict.dat - pickle file containing dictionary used in collect_data.py. It currently contains data for over 5000 users
* extract_data.py - script for extracting data from user_dict.dat and writing it as a .csv file. Open script, select how many top subreddits you want to extract, then execute with 'python extract_data.py'
* clustering.R - commands used to cluster and plot data using R
* make_GEXF.py - a script I started making which turns the .csv into a .gexf file based on a correlation threshold. But I got bored and gave up. It works but its of no interest to me.