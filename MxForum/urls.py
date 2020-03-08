from apps.users import urls as user_urls
from apps.community import urls as community_urls
url_pattern = []

url_pattern += user_urls.url_pattern
url_pattern += community_urls.url_pattern
