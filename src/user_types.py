user_types = {
    "Lurker": {
        "follower_range": (0.001, 0.005),  # 0.1% to 0.5% of the network size
        "following_range": (0.005, 0.01),  # 0.5% to 1% of the network size
        "post_frequency_range": (0.02, 0.08),  # Lurkers rarely post
        "engagement_range": (0.1, 0.3), 
        "network_building_range": (0.05, 0.1),
        "follow_back_prob": 0.05,
        "unfollow_prob": 0.05,  # Low chance of unfollowing
        "distribution": 0.4, # Percentage of population
        "color": "gray"
    },
    
    "Casual": {
        "follower_range": (0.005, 0.01),  # 0.5% to 1% of the network size
        "following_range": (0.01, 0.015),  # 1% to 1.5% of the network size
        "post_frequency_range": (0.2, 0.4),  # Casual users post occasionally
        "engagement_range": (0.3, 0.5), 
        "network_building_range": (0.1, 0.3),
        "follow_back_prob": 0.20, 
        "unfollow_prob": 0.1,  # Moderate chance of unfollowing inactive users
        "distribution": 0.3,  
        "color": "cyan"
    },
    
    "Active": {
        "follower_range": (0.01, 0.02),  # 1% to 2% of the network size
        "following_range": (0.015, 0.025),  # 1.5% to 2.5% of the network size
        "post_frequency_range": (0.5, 0.7),  # Posts frequently
        "engagement_range": (0.5, 0.7), 
        "network_building_range": (0.3, 0.5),
        "follow_back_prob": 0.30, 
        "unfollow_prob": 0.15,  # Higher chance of unfollowing based on engagement
        "distribution": 0.2, 
        "color": "green"
    },
    
    "Influencer": {
        "follower_range": (0.5, 0.1),  # 5% to 10% of the network size
        "following_range": (0.03, 0.07),  # 1% to 3% of the network size
        "post_frequency_range": (0.8, 1.0),  # Posts very frequently
        "engagement_range": (0.7, 0.9), 
        "network_building_range": (0.5, 0.8),
        "follow_back_prob": 0.05, 
        "unfollow_prob": 0.05,  # Rarely unfollows unless inactive
        "distribution": 0.015, 
        "color": "gold"
    },
    
    "Bot": {
        "follower_range": (0.001, 0.01),  # 0.1% to 1% of the network size
        "following_range": (0.02, 0.05),  # 2% to 5% of the network size
        "post_frequency_range": (0.4, 0.7),  # Bots post frequently but with low engagement content
        "engagement_range": (0.4, 0.6), 
        "network_building_range": (0.6, 1.0),
        "follow_back_prob": 0.60,  # High follow-back probability to gain credibility
        "unfollow_prob": 0.2,  # Bots may unfollow users often
        "distribution": 0.085,
        "color": "red"
    }
}


