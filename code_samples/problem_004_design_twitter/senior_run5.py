from typing import List, Dict, Set
from collections import defaultdict, deque

class Twitter:
    """
    A simplified Twitter implementation supporting posting tweets, following users,
    and retrieving personalized news feeds.
    """
    
    MAX_FEED_SIZE = 10
    
    def __init__(self):
        """
        Initialize the Twitter data structure.
        """
        self.tweet_counter = 0  # Global timestamp for tweet ordering
        self.user_tweets: Dict[int, deque] = defaultdict(lambda: deque(maxlen=self.MAX_FEED_SIZE))
        self.following_graph: Dict[int, Set[int]] = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        """
        Post a tweet for the specified user.
        
        Args:
            userId: The ID of the user posting the tweet
            tweetId: The ID of the tweet being posted
        """
        self.tweet_counter += 1
        tweet_data = (self.tweet_counter, tweetId)  # Store timestamp with tweet
        self.user_tweets[userId].append(tweet_data)

    def getNewsFeed(self, userId: int) -> List[int]:
        """
        Retrieve the 10 most recent tweets in the user's news feed.
        
        Args:
            userId: The ID of the user requesting the news feed
            
        Returns:
            List of tweet IDs in reverse chronological order (most recent first)
        """
        all_relevant_tweets = []
        
        # Collect tweets from user and all followed users
        users_to_check = self.following_graph[userId] | {userId}
        
        for user_id in users_to_check:
            if user_id in self.user_tweets:
                all_relevant_tweets.extend(self.user_tweets[user_id])
        
        # Sort by timestamp in descending order and return top 10 tweet IDs
        all_relevant_tweets.sort(key=lambda tweet: tweet[0], reverse=True)
        return [tweet[1] for tweet in all_relevant_tweets[:self.MAX_FEED_SIZE]]

    def follow(self, followerId: int, followeeId: int) -> None:
        """
        Make one user follow another user.
        
        Args:
            followerId: The ID of the user who wants to follow
            followeeId: The ID of the user to be followed
        """
        if followerId != followeeId:  # User cannot follow themselves
            self.following_graph[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        """
        Make one user unfollow another user.
        
        Args:
            followerId: The ID of the user who wants to unfollow
            followeeId: The ID of the user to be unfollowed
        """
        self.following_graph[followerId].discard(followeeId)