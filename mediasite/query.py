'''
@author: aamvanderkraan
'''


class Query(object):
    '''
    Dispatches the query to the valid method. In the method the
    The return value can be filtered in the dispatched methods
    The calling command is something like:
    Client = Client()
    client.get_resource('Players', resource_id='', properties={}, link='',
                        link_id='', query_options='')
    Only the first parameter, the so called resource, is mandatory
    '''
    def __init__(self):
        pass

    def get_resource(self, resource, **kwargs):
        try:
            method = getattr(self, '_%s_%s' % ('get', resource.lower()))
            return method(resource, **kwargs)
        except Exception, inst:
            return {'error': {'message from Query': '%s' % inst}}

    def _get_players(self, resource, **kwargs):
        result = self.do(resource, 'GET', **kwargs)
        return result

    def _get_catalogs(self, resource, **kwargs):
        result = self.do(resource, 'GET', **kwargs)
        return result

    def _get_folders(self, resource, **kwargs):
        result = self.do(resource, 'GET', **kwargs)
        return result

    def _get_presentations(self, resource, **kwargs):
        result = self.do(resource, 'GET', **kwargs)
        return result

    def _get_modules(self, resource, **kwargs):
        result = self.do(resource, 'GET', **kwargs)
        return result

    def _get_home(self, resource, **kwargs):
        '''
        Returns information about the mediasite itself
        '''
        result = ''
        try:
            result = self.do(resource, 'GET', **kwargs)
        except Exception, inst:
            result = inst
        return result

if __name__ == '__main__':
    from mediasite.client import Client
    client = Client()
    print client._get_home('Home')
    pass
