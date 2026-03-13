from typing import List, Dict, Set, Deque
from collections import defaultdict, deque


class Twitter:
    """
    A simplified Twitter system that supports posting tweets, following/unfollowing users,
    and retrieving news feeds.
    """
    
    MAX_FEED_SIZE = 10
    
    def __init__(self):
        """Initialize the Twitter system with empty data structures."""
        self.tweet_counter: int = 0  # Global counter for tweet ordering
        self.user_tweets: Dict[int, Deque[tuple]] = defaultdict(deque)  # userId -> deque of (timestamp, tweetId)
        self.following_graph: Dict[int, Set[int]] = defaultdict(set)  # userId -> set of followeeIds
    
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
        self.user_tweets[userId].appendleft((self.tweet_counter, tweetId))
    
    def getNewsFeed(self, userId: int) -> List[int]:
        """
        Retrieve the 10 most recent tweet IDs in the user's news feed.
        
        Args:
            userId: The ID of the user requesting the news feed
            
        Returns:
            List of up to 10 most recent tweet IDs from user and followees
        """
        if userId < 0:
            raise ValueError("User ID must be non-negative")
            
        # Collect all relevant users (self + followees)
        relevant_users = self._get_relevant_users_for_feed(userId)
        
        # Merge tweets from all relevant users
        all_tweets = self._merge_tweets_from_users(relevant_users)
        
        # Return top 10 most recent tweets
        return [tweet_id for _, tweet_id in all_tweets[:self.MAX_FEED_SIZE]]
    
    def follow(self, followerId: int, followeeId: int) -> None:
        """
        Make followerId follow followeeId.
        
        Args:
            followerId: The ID of the user who wants to follow
            followeeId: The ID of the user to be followed
        """
        if followerId < 0 or followeeId < 0:
            raise ValueError("Follower ID and Followee ID must be non-negative")
            
        if followerId != followeeId:  # User cannot follow themselves
            self.following_graph[followerId].add(followeeId)
    
    def unfollow(self, followerId: int, followeeId: int) -> None:
        """
        Make followerId unfollow followeeId.
        
        Args:
            followerId: The ID of the user who wants to unfollow
            followeeId: The ID of the user to be unfollowed
        """
        if followerId < 0 or followeeId < 0:
            raise ValueError("Follower ID and Followee ID must be non-negative")
            
        self.following_graph[followerId].discard(followeeId)
    
    def _get_relevant_users_for_feed(self, user_id: int) -> Set[int]:
        """
        Get all users whose tweets should appear in the given user's feed.
        
        Args:
            user_id: The ID of the user requesting the feed
            
        Returns:
            Set of user IDs including the user and their followees
        """
        relevant_users = {user_id}  # Include user's own tweets
        relevant_users.update(self.following_graph[user_id])  # Add followees
        return relevant_users
    
    def _merge_tweets_from_users(self, user_ids: Set[int]) -> List[tuple]:
        """
        Merge and sort tweets from multiple users by timestamp (most recent first).
        
        Args:
            user_ids: Set of user IDs whose tweets should be included
            
        Returns:
            List of (timestamp, tweetId) tuples sorted by timestamp descending
        """
        all_tweets = []
        
        for user_id in user_ids:
            if user_id in self.user_tweets:
                all_tweets.extend(self.user_tweets[user_id])
        
        # Sort by timestamp descending (most recent first)
        all_tweets.sort(key=lambda x: x[0], reverse=True)
        return all_tweets