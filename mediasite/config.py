'''
@author: aamvanderkraan
'''
import urllib
import json
import ConfigParser
import mediasite_settings


class Config():
    def __init__(self, config_file=None):
        self.service_root = 'https://collegerama.tudelft.nl/mediasite'
        self.api_path = '/api/v1/'  # AuthorizationTickets
        self.timeout = 5  # timeout for the server in seconds
        self.base_url = '%s%s' % (self.service_root, self.api_path)
        self.data = {}
        if config_file:
            self.data = self._config(config_file)
        else:
            self.data = self._config(None)
        self.base_url = '%s%s' % (self.service_root, self.api_path)
        # data should come from the server with credential information
        if 'data' in self.data.keys():
            self.data['data']['timeout'] = self.timeout
            self.data['data']['base_url'] = self.base_url
            hostname = self.base_url.split('//')[1].split('/')[0]
            self.data['data']['hostname'] = hostname

    def get_data(self):
        '''
        Example:
        {'data':{'base_url': 'http://collegerama.tudelft.nl/Mediasite/api/v1/',
                 'timeout': 30,
                  u'error': u'Origin 145.94.222.172 is not allowed to access '
                            'handlero.tudelft.nl'}
                  }
        '''
        return self.data

    def _config(self, filename):
        '''
        You could make your own configuration file in the form of
        [server]
        server_root = <server_root>
        api_path = <api_path>
        timeout = <timeout>
        url = <url>

        # for server with api credentials:
        [api_credentials]
        url = <url>

        but default the mediasite_settings.py file is used
        '''
        try:
            raw_url = ''
            if filename:
                filename = filename or '../mediasite.conf'
                mediasite_config = ConfigParser.ConfigParser()
                mediasite_config.read(filename)
                self.service_root = mediasite_config.get('server',
                                                         'server_root')
                self.api_path = mediasite_config.get('server', 'api_path')
                self.timeout = int(mediasite_config.get('server', 'timeout'))
                raw_url = mediasite_config.get('api_credentials', 'url')
            else:
                self.service_root = mediasite_settings.server_root
                self.api_path = mediasite_settings.api_path
                self.timeout = int(mediasite_settings.timeout)
                raw_url = mediasite_settings.url
            api_server = self.service_root.split('//')[1].split('/')[0]
            url = raw_url.replace('<api_server>', api_server)
            api_access = self._api_access(url)
            data = 'data' in api_access.keys() and api_access or None
            if not data:
                data = 'error' in api_access.keys() and api_access or \
                    {'error': 'Sorry, could not find any configuration data '
                     'in %s' % filename}
            return data
        except Exception, inst:
            return {'error': 'Error while trying to get configuration data '
                    'from file %s. Message: %s' % (filename, inst)}

    def _api_access(self, url):
        try:
            response = urllib.urlopen(url)
            data = response.read()
            data = json.loads(data)
            return data
        except:
            return {'error': 'Sorry, could not find configuration data on '
                    'server %s' % url}

if __name__ == '__main__':
    config = Config().get_data()
    data = 'data' in config.keys() and config['data'] or None
    if data:
        timeout = 'timeout' in data.keys() and data['timeout'] or 32
        base_url = 'base_url' in data.keys() and data['base_url'] or \
            '%s%s' % ('https://collegerama.tudelft.nl/Mediasite', '/api/v1/')
    else:
        print 'no data'
