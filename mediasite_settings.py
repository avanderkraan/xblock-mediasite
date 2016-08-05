# productieserver:
server_root = 'https://collegerama.tudelft.nl/Mediasite'
api_path = '/Api/v1/'
# timeout is timeout for the mediasite server in seconds
timeout = 300

# url is the place where to get the data for the API credentials
#
# with server_root = 'http://collegerama-vs-accept.tudelft.net/Mediasite7',
# the url will be:
# 'http://handlero.tudelft.nl/mediasite/collegerama-vs-accept.tudelft.net/'
url = 'https://handlero.tudelft.nl/mediasite/<api_server>/'

# display_name is shown on top of the course unit and in the Advanced Unit List
display_name = 'Collegerama Video'

# Maximum items requested from the server
# In the case of more items available on the server, the program should
# return a warning
maximum_items = 50

# date format as shown in the list, see C standard (1989 version)
date_format = '%Y-%m-%d'
