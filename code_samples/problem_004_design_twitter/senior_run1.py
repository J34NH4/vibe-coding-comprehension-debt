from typing import List, Set, Dict, Deque
from collections import defaultdict, deque

class Twitter:
    """
    A simplified Twitter implementation supporting posting tweets, following/unfollowing users,
    and retrieving news feeds.
    """
    
    MAX_FEED_SIZE = 10
    
    def __init__(self):
        """
        Initialize the Twitter data structure.
        """
        self.tweet_counter: int = 0  # Global timestamp for tweets
        self.user_tweets: Dict[int, Deque[tuple]] = defaultdict(deque)  # userId -> deque of (timestamp, tweetId)
        self.following_graph: Dict[int, Set[int]] = defaultdict(set)  # userId -> set of followeeIds
    
    def postTweet(self, userId: int, tweetId: int) -> None:
        """
        Post a new tweet by the given user.
        
        Args:
            userId: The ID of the user posting the tweet
            tweetId: The ID of the tweet being posted
        """
        self.tweet_counter += 1
        self.user_tweets[userId].appendleft((self.tweet_counter, tweetId))  # Most recent first
        
        # Keep only the 10 most recent tweets per user for efficiency
        if len(self.user_tweets[userId]) > self.MAX_FEED_SIZE:
            self.user_tweets[userId].pop()
    
    def getNewsFeed(self, userId: int) -> List[int]:
        """
        Retrieve the 10 most recent tweet IDs in the user's news feed.
        
        Args:
            userId: The ID of the user requesting the news feed
            
        Returns:
            List of tweet IDs ordered from most recent to least recent
        """
        all_relevant_tweets = []
        
        # Add user's own tweets
        all_relevant_tweets.extend(self.user_tweets[userId])
        
        # Add tweets from followed users
        for followee_id in self.following_graph[userId]:
            all_relevant_tweets.extend(self.user_tweets[followee_id])
        
        # Sort by timestamp (descending) and take top 10
        all_relevant_tweets.sort(key=lambda x: x[0], reverse=True)
        
        return [tweet_id for _, tweet_id in all_relevant_tweets[:self.MAX_FEED_SIZE]]
    
    def follow(self, followerId: int, followeeId: int) -> None:
        """
        Make follower follow followee.
        
        Args:
            followerId: The ID of the user who wants to follow
            followeeId: The ID of the user to be followed
        """
        if followerId != followeeId:  # User cannot follow themselves
            self.following_graph[followerId].add(followeeId)
    
    def unfollow(self, followerId: int, followeeId: int) -> None:
        """
        Make follower unfollow followee.
        
        Args:
            followerId: The ID of the user who wants to unfollow
            followeeId: The ID of the user to be unfollowed
        """
        self.following_graph[followerId].discard(followeeId)  # discard won't raise error if not present