from collections import defaultdict, deque
from typing import List, Set, Dict
from heapq import heappush, heappop

class Twitter:
    """
    A simplified Twitter system that supports posting tweets, following/unfollowing users,
    and retrieving news feeds.
    """
    
    def __init__(self) -> None:
        """
        Initialize the Twitter system with empty data structures.
        """
        self.tweet_counter: int = 0  # Global counter for tweet ordering
        self.user_tweets: Dict[int, deque] = defaultdict(deque)  # userId -> tweets
        self.following_map: Dict[int, Set[int]] = defaultdict(set)  # userId -> set of followees
        self.MAX_FEED_SIZE: int = 10  # Maximum tweets in news feed

    def postTweet(self, userId: int, tweetId: int) -> None:
        """
        Post a new tweet by the given user.
        
        Args:
            userId: The ID of the user posting the tweet
            tweetId: The ID of the tweet being posted
        """
        self.tweet_counter += 1
        tweet_data = (self.tweet_counter, tweetId)  # Store with timestamp for ordering
        self.user_tweets[userId].appendleft(tweet_data)  # Most recent tweets first

    def getNewsFeed(self, userId: int) -> List[int]:
        """
        Retrieve the 10 most recent tweets in the user's news feed.
        News feed includes tweets from the user and their followees.
        
        Args:
            userId: The ID of the user requesting the news feed
            
        Returns:
            List of tweet IDs in reverse chronological order (most recent first)
        """
        # Collect all relevant users (self + followees)
        relevant_users = set(self.following_map[userId])
        relevant_users.add(userId)  # User sees their own tweets
        
        # Use min heap to get top 10 most recent tweets
        tweet_heap = []
        
        for user_id in relevant_users:
            user_tweet_list = self.user_tweets[user_id]
            # Add up to 10 most recent tweets from each user
            for i, (timestamp, tweet_id) in enumerate(user_tweet_list):
                if i >= self.MAX_FEED_SIZE:  # Limit tweets per user for efficiency
                    break
                # Use negative timestamp for max heap behavior with min heap
                heappush(tweet_heap, (-timestamp, tweet_id))
        
        # Extract top 10 tweets
        news_feed = []
        for _ in range(min(self.MAX_FEED_SIZE, len(tweet_heap))):
            if tweet_heap:
                _, tweet_id = heappop(tweet_heap)
                news_feed.append(tweet_id)
        
        return news_feed

    def follow(self, followerId: int, followeeId: int) -> None:
        """
        Make one user follow another user.
        
        Args:
            followerId: The ID of the user who wants to follow
            followeeId: The ID of the user to be followed
        """
        if followerId != followeeId:  # Prevent self-following
            self.following_map[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        """
        Make one user unfollow another user.
        
        Args:
            followerId: The ID of the user who wants to unfollow
            followeeId: The ID of the user to be unfollowed
        """
        if followeeId in self.following_map[followerId]:
            self.following_map[followerId].remove(followeeId)