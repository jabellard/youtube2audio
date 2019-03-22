from rest_framework.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    rate = '10/minute'


class SustainedRateThrottle(UserRateThrottle):
    rate = '100/day'
