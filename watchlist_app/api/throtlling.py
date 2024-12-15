from rest_framework.throttling import UserRateThrottle

# Create a custom throttle class that limits the number of requests per user to 50 per minute

class ReviewCreateThrottle(UserRateThrottle):
    scope='review_create'

class ReviewListThrottle(UserRateThrottle):
    scope='review_list'