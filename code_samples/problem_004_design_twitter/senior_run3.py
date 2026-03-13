from collections import defaultdict, deque
from typing import List, Set, Dict
import heapq

class Twitter:
    """
    A simplified Twitter implementation supporting posting tweets, following users,
    and retrieving news feeds.
    """
    
    MAX_FEED_SIZE = 10
    
    def __init__(self):
        """Initialize the Twitter data structure."""
        self.tweet_counter: int = 0  # Global counter for tweet ordering
        self.user_tweets: Dict[int, List[tuple]] = defaultdict(list)  # userId -> [(timestamp, tweetId)]
        self.following_map: Dict[int, Set[int]] = defaultdict(set)  # userId -> set of followed userIds
    
    def postTweet(self, userId: int, tweetId: int) -> None:
        """
        Post a new tweet by the given user.
        
        Args:
            userId: The ID of the user posting the tweet
            tweetId: The ID of the tweet being posted
        """
        if userId < 0 or tweetId < 0:
            raise ValueError("User ID and Tweet ID must be non-negative")
            
        self.tweet_counter += 1
        self.user_tweets[userId].append((self.tweet_counter, tweetId))
    
    def getNewsFeed(self, userId: int) -> List[int]:
        """
        Retrieve the 10 most recent tweets in the user's news feed.
        
        Args:
            userId: The ID of the user requesting their news feed
            
        Returns:
            List of tweet IDs in reverse chronological order (most recent first)
        """
        if userId < 0:
            raise ValueError("User ID must be non-negative")
            
        # Collect all relevant users (self + following)
        relevant_users = self._get_relevant_users_for_feed(userId)
        
        # Use max heap to get most recent tweets
        tweet_heap = []
        
        for user_id in relevant_users:
            user_tweet_list = self.user_tweets[user_id]
            for timestamp, tweet_id in user_tweet_list:
                if len(tweet_heap) < self.MAX_FEED_SIZE:
                    heapq.heappush(tweet_heap, (timestamp, tweet_id))
                elif timestamp > tweet_heap[0][0]:  # Current tweet is more recent
                    heapq.heapreplace(tweet_heap, (timestamp, tweet_id))
        
        # Extract tweets and sort by timestamp (most recent first)
        sorted_tweets = sorted(tweet_heap, key=lambda x: x[0], reverse=True)
        return [tweet_id for _, tweet_id in sorted_tweets]
    
    def follow(self, followerId: int, followeeId: int) -> None:
        """
        Make followerId follow followeeId.
        
        Args:
            followerId: The ID of the user who wants to follow
            followeeId: The ID of the user to be followed
        """
        if followerId < 0 or followeeId < 0:
            raise ValueError("Follower ID and Followee ID must be non-negative")
            
        if followerId == followeeId:
            return  # User cannot follow themselves
            
        self.following_map[followerId].add(followeeId)
    
    def unfollow(self, followerId: int, followeeId: int) -> None:
        """
        Make followerId unfollow followeeId.
        
        Args:
            followerId: The ID of the user who wants to unfollow
            followeeId: The ID of the user to be unfollowed
        """
        if followerId < 0 or followeeId < 0:
            raise ValueError("Follower ID and Followee ID must be non-negative")
            
        if followerId == followeeId:
            return  # User cannot unfollow themselves
            
        self.following_map[followerId].discard(followeeId)
    
    def _get_relevant_users_for_feed(self, user_id: int) -> Set[int]:
        """
        Get all users whose tweets should appear in the given user's feed.
        
        Args:
            user_id: The ID of the user requesting the feed
            
        Returns:
            Set of user IDs whose tweets should be included in the feed
        """
        relevant_users = {user_id}  # Always include own tweets
        relevant_users.update(self.following_map[user_id])  # Add followed users
        return relevant_users