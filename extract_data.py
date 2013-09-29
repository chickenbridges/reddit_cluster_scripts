import os
import random
import shelve
import praw

# Define variables
top_num = 300 # Number of top subreddits to extract, None for all
sub_dict_file = 'user_dict.dat' # .dat in file containing raw data
out_file = 'data.csv' # File to write csv to


def write_subreddits(sub_list):
    with open('subreddits.txt', 'w') as out_handle:
        for sub in sub_list:
            out_handle.write('{0}\n'.format(sub))

def list_of_subreddits(user_sub_dict, top_num):
    """Given a dict of key:user value:[list of subreddits], it sum how many 
       users are in each subreddit and return the top one in size order
    """
    all_sub_dict = {}
    
    for user in user_sub_dict:
        for sub in user_sub_dict[user]:
            try:
                all_sub_dict[sub] += 1
            except KeyError:
                all_sub_dict[sub] = 1
            
    all_sub_list = sorted(all_sub_dict.keys(),
                          key=lambda x: all_sub_dict[x],
                          reverse=True)
    print 'Total subreddits: {0}'.format(len(all_sub_list))
    #~ write_subreddits(all_sub_list)
    
    return all_sub_list[:top_num]

def write_data_csv(user_sub_dict, out_file, top_num=None):
    """Writes data to file. Threshold will only write to file if sub has that
       many users or more.
    """
    
    # Get list of all subs
    sub_list = list_of_subreddits(user_sub_dict, top_num)
    
    # Sorted list of all users
    users = sorted(user_sub_dict.keys())
    
    with open(out_file, 'w') as out_handle:
        
        # Write header
        line = '\t' + '\t'.join(sub_list) + '\n'
        out_handle.write(line)
        
        # For each sub write 1 or 0 if user posts there
        for user in users:
            # Make list of 1 and 0 for each user
            binary_list = []
            for sub in sub_list:
                if sub in user_sub_dict[user]:
                    binary_list.append(1)
                else:
                    binary_list.append(0)
            # Write entry for sub if above threshold
            list_string = [str(entry) for entry in binary_list]
            line = str(user)+ '\t' + '\t'.join(list_string) + '\n'
            out_handle.write(line)


def retrieve_data(r):
    pass

def main():

    # Load dictionary    
    user_sub_dict = shelve.open(sub_dict_file)
    
    # Write data to CSV
    write_data_csv(user_sub_dict, out_file, top_num)
    
    user_sub_dict.close()

if __name__ == '__main__':
	main()
