'''
@author: aamvanderkraan
'''
from requests import request
import json


class Handler(object):
    '''
    Handles API requests
    The method handle makes classes ResourceDispatcher and Resource unnecessary
    '''
    def __init__(self, config={}):
        self.timeout = 10
        self.base_url = '%s%s' % ('https://collegerama.tudelft.nl/Mediasite',
                                  '/api/v1/')
        data = 'data' in config.keys() and config['data'] or None
        if data:
            self.timeout = 'timeout' in data.keys() and data['timeout'] or 30
            self.base_url = 'base_url' in data.keys() and data['base_url'] or \
                '%s%s' % ('https://collegerama.tudelft.nl/Mediasite',
                          '/api/v1/')

    def handle(self,
               headers={},
               resource='',
               method='GET',
               **kwargs):
        '''
        Example url:
        http://collegerama.tudelft.net/Mediasite7/Api/v1/Presentations \
            ('000e4e3c9fc44640ac59d216d97d1a3e1d')/CopyPresentation"
        method = GET, POST, ...
        '''
        properties = kwargs.pop('properties', {})
        resource_id = kwargs.pop('resource_id', '')
        link = kwargs.pop('link', '')
        link_id = kwargs.pop('link_id', '')
        query_options = kwargs.pop('query_options', '')

        url = '%s%s%s%s%s%s' % (self.base_url,
                                resource,  # e.g. 'Presentations',
                                resource_id and '''('%s')''' % resource_id,
                                link and '/%s' % link,
                                link_id and '(%s)' % link_id,
                                query_options and '?%s' % query_options)

        # properties MUST be valid JSON format
        jproperties = json.dumps(properties)
        j2properties = jproperties.replace("""'""", '''"''')
        j3properties = json.loads(j2properties)
        response = ''
        try:
            response = request(method.upper(),
                               url,
                               json=j3properties,
                               headers=headers,
                               timeout=(float(self.timeout)))
            return response.json()
        except Exception as inst:
            return "{'error': 'No proper response. Response was: %s\n%s'}" % \
                 (inst, response)


if __name__ == '__main__':
    from config import Config
    c = Config().get_data()
    h = Handler(c)
    print h.base_url
