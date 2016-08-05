'''
@author: aamvanderkraan
client for mediasite by sonicfoundry
'''
from authentication import Authentication
from handler import Handler
from config import Config
from query import Query


class Client(Query):
    def __init__(self):
        # init Query
        super(Client, self).__init__()

        self.token = None
        self.server_info = None
        self.headers = {}
        self.config = Config().get_data()
        self.authentication = None

        data = 'data' in self.config.keys() and self.config['data'] or None
        if data:
            self.hostname = 'hostname' in data.keys() and \
                data['hostname'] or ''
            self.sf_apikey = 'apikey' in data.keys() and \
                data['apikey'] or ''
            self.username = 'username' in data.keys() and \
                data['username'] or ''
            self.password = 'password' in data.keys() and \
                data['password'] or ''
            self.impersonation_username = \
                'impersonation_username' in data.keys() and \
                data['impersonation_username'] or ''
            self.token_life_time = 'token_life_time' in data.keys() and \
                data['token_life_time'] or 0
            self.handler = Handler(self.config)
            self.authentication = Authentication(
                hostname=self.hostname,
                sf_apikey=self.sf_apikey,
                username=self.username,
                password=self.password,
                impersonation_username=self.impersonation_username)

    def is_authenticated(self):
        if self.token:
            return True
        return False

    def get_server_info(self):
        '''
        Server information after an API call with Home as a resource
        This resource should return information without extra header settings
        '''
        return self._get_home('Home')

    def get_token(self,
                  ticket_username='',
                  resource_id='',
                  ):
        '''
        Get token if self.authentication is not None, which means that the
        configuration file is successfully parsed
        @param ticket_username: can be any name - ticket will be issued with
               this username attached
        @param resource_id: ID of the resource in URL string format
               e.g. "21a7a4520b75404dbc1be3b223c6612a1d"
        @param minutes_to_live: number of minutes after creation that the
               ticket will be valid for
        '''
        try:
            self.token = self.authentication.get_token(
                config=self.config,
                ticket_username=ticket_username,
                resource_id=resource_id,
                minutes_to_live=self.token_life_time)
            return self.token
        except:
            self.token = None
        return self.token

    def do(self, resource='', method='GET', **kwargs):
        '''
        Checks the availability of a access token and does the request via
        the resource_dispatcher to the right resource with the correct
        request-headers.
        The final goal is something like:
            GET /api/v1/Presentations('id1')/Presenters(id2)
        @param resource: Resource name as mentioned in the API documentation
                         http://demo7.mediasite.com/mediasite/api/v1/$metadata
        @param **kwargs: Valid keyword arguments are
                         properties: Properties of the resource
                         resource_id: resource identifier
                         link_id: resource_link identifier
                         link: dictionary, contains resource-specific
                               options. The resource_link itself is
                               a dictionary (see: CatalogSettings)
                         query_options: odata query_options, (e.g. $filter=)
                                        (http://www.odata.org/documentation)
                         sf_apikey: string, necessary for every request in the
                                    header, comes from the application that
                                    uses this Client class
        '''
        if self.authentication:
            if not self.token:
                # create token with Basic access
                self.headers = self.authentication.basic_header()
            else:
                sf_auth_ticket = self.token  # authentication.get_token()
                self.headers = self.authentication.authorization_ticket_header(
                    sf_auth_ticket)
            result = self.handler.handle(headers=self.headers,
                                         resource=resource,
                                         method=method,
                                         **kwargs)
        else:
            error_message = ''
            try:
                error_message = 'error' in self.config.keys() and \
                    self.config['error']
            except:
                error_message = 'Configuration module failed'
            raise Exception('Authentication failed: %s' % error_message)
        return result
