from collections import defaultdict
from mesa.datacollection import DataCollector


# POSTING

def compute_post_frequency_per_step(model):
    # Count posts added to the content pool during the current step
    posts_this_step = len([content
                           for content in model.content_pool
                              if content["timestamp"] == model.current_step])
    return posts_this_step / len(model.agents)  # Average posts per agent

def compute_rolling_post_frequency(model, window=10):
    # Get recent posts from the last `window` steps
    recent_posts = [content for content in model.content_pool if model.current_step - content["timestamp"] < window]
    return len(recent_posts) / (len(model.agents) * window)  # Average posts per agent per step


def compute_posts_by_user_type(model):
    posts_by_user_type = defaultdict(int)
    for content in model.content_pool:
        posts_by_user_type[content["user_type"]] += 1
    return posts_by_user_type



# Engagement
def compute_avg_engagement_per_step(model):
    # Get engagement for content posted in the current step only
    current_step_content = [
        content for content in model.content_pool if content['timestamp'] == model.current_step
    ]
    total_engagement = sum(content['engagement_count'] for content in current_step_content)
    return total_engagement / len(current_step_content) if len(current_step_content) > 0 else 0


def compute_post_freq_by_user_type_per_step(model):
    """Calculate post frequency for each user type per step."""
    post_freq_by_user_type = defaultdict(int)
    total_users_by_type = defaultdict(int)

    # Count posts added in the current step for each user type
    for agent in model.agents:
        total_users_by_type[agent.user_type] += 1
        # Count posts added to the agent's content pool during the current step
        posts_this_step = [
            content_id
            for content_id in agent.agent_content_pool
            if content_id.split('_')[-1] == str(model.current_step)
        ]
        post_freq_by_user_type[agent.user_type] += len(posts_this_step)

    # Calculate average post frequency per user type
    for user_type in post_freq_by_user_type:
        post_freq_by_user_type[user_type] /= total_users_by_type[user_type]

    return post_freq_by_user_type



def compute_avg_engagement_by_user_type_per_step(model):
    """Calculate average engagement per user type per step."""
    engagement_by_user_type = defaultdict(int)
    post_count_by_user_type = defaultdict(int)

    # Filter content by posts created in the current step
    for content in model.content_pool:
        if content['timestamp'] == model.current_step:
            engagement_by_user_type[content['user_type']] += content['engagement_count']
            post_count_by_user_type[content['user_type']] += 1

    # Calculate average engagement per post for each user type
    for user_type in engagement_by_user_type:
        if post_count_by_user_type[user_type] > 0:
            engagement_by_user_type[user_type] /= post_count_by_user_type[user_type]

    return engagement_by_user_type

