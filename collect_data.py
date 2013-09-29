import os
import time
import random
import shelve
import praw

def get_random_user(r):
    """Will select a random sub select a random user from the latest 25
       comments.
    """
    # Get random sub
    randsubreddit = r.get_random_subreddit()
    
    # Get latest comments for sub
    comments = randsubreddit.get_comments(limit=25)
    
    # Make list of authors and select one randomly.
    authors = [str(comment.author) for comment in comments]
    
    if len(authors) > 0:
        author = random.choice(authors)
        return author

def get_user_sublist(r, user_name, comment_limit=1000):
    """Given a username, it will go through all their comments and create a
       set of all active subs.
    """
    subreddit_set = set([])
    
    # Get user and comments
    user = r.get_redditor(user_name)
    comments = user.get_comments(limit=comment_limit)
    
    # Add subreddit to set for each comment
    for comment in comments:
        sub = str(comment.subreddit)
        subreddit_set.add(sub)
    
    return subreddit_set

def retrieve_data(r):
    pass

def main():
    # Variables
    num_comments = 1000
    sub_dict_file = 'user_dict.dat'
    
    # Initiate reddit
    r = praw.Reddit('Subreddit map builder by u/chicken_bridges')
    #~ r.login('<REDACTED>', '<REDACTED>')
    
    # Load dictionary
    user_sub_dict = shelve.open(sub_dict_file)
    
    # Continously collect data
    while True:
        try:
            print 'Got data for {0} users...'.format(len(user_sub_dict))
            random_user = get_random_user(r)
            if random_user not in user_sub_dict:
                subreddit_set = get_user_sublist(r, random_user, num_comments)
                user_sub_dict[random_user] = subreddit_set
                user_sub_dict.sync()
        except:
            print 'Error connecting to reddit. Will sleep for 10 secs...'
            time.sleep(10)
    
    user_sub_dict.close()

if __name__ == '__main__':
	main()
