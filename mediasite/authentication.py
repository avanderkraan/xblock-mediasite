'''
@author: aamvanderkraan
'''
import base64
from handler import Handler


class Authentication:
    BASIC = 'Basic'
    AUTHORIZATION = 'AuthTicket'
    IDENTITY = 'IdentTicket'

    def __init__(self,
                 hostname='',
                 sf_apikey='',
                 username='',
                 password='',
                 impersonation_username=''):
        '''
        @param sf_apikey: a sonicfoundry key which allows access to a
                          mediasite API, this key is provided by the
                          administrator of a mediasite
        @param username: used for Basic and SfIdentTicket
        @param password: used for Basic and SfIdentTicket
        @param impersonation_username: used for SfIdentTicket (optional)
        @param sf_apikey: sonicfoundry apikey for accessing a mediasite API
        '''

        self.hostname = hostname,
        self.sf_apikey = sf_apikey
        self.username = username
        self.password = password
        self.impersonation_username = impersonation_username
        self.tkt = None

    def _get_access_headers(self,
                            authentication_method='Basic'):
        '''
        Basic authentication can set a cookie
        SfAuthTicket gives a authorization ticket using an Identity Ticket
        SfIdentTicket gives a identification ticket
        @param authorization_type: Basic, AuthTicket or IdentTicket
        '''
        headers = {}
        if authentication_method == self.AUTHORIZATION:
            # one parameter needed!
            headers = self.authorization_ticket_header(self.tkt)
        elif authentication_method == self.IDENTITY:
            headers = self.identity_ticket_header()
        else:
            headers = self.basic_header()
        return headers

    def get_token(self,
                  config={},
                  ticket_username='',
                  resource_id='',
                  minutes_to_live=0,
                  **kwargs):
        '''
        @param ticket_username: can be any name - ticket will be issued with
               this username attached
        @param resource_id: ID of the resource in URL string format
               e.g. "21a7a4520b75404dbc1be3b223c6612a1d"
        @param minutes_to_live: number of minutes after creation that the
               ticket will be valid for
        @return: the SfAuthTicket
        '''
        identity_ticket_headers = self._get_access_headers(
            authentication_method=self.BASIC)
        authentication_handler = Handler(config)
        result = authentication_handler.handle(
            headers=identity_ticket_headers,
            resource='AuthorizationTickets',
            method='POST',
            properties={
                        "Username": ticket_username,
                        "ResourceId": resource_id,
                        "MinutesToLive": minutes_to_live
                        }
            )
        self.tkt = result['TicketId']
        return result

        '''
        if result.find('error') < 0:
            authorization_ticket_headers = self._get_access_headers(
                authentication_method=self.AUTHORIZATION)
            authentication_handler = Handler(config)
            result2 = authentication_handler.handle(
                headers=authorization_ticket_headers,
                resource='AuthorizationTickets',
                method='POST',
                properties={'Username': ticket_username,
                            'ResourceId': resource_id,
                            'MinutesToLive': minutes_to_live
                            },

                )
            return result2
        else:
            return result
        '''

    def basic_header(self):
        '''
        @return: a basic login header

        Example:
        Basic Authentication
            GET https://mysite.mediasite.com/Mediasite/
                                api/v1/Presentations HTTP/1.1
            Host: dev.mediasite.com
            Accept: text/html,application/xhtml+xml,
                              application/xml;q=0.9,image/webp,*/*;q=0.8
            sfapikey: <your api key>
            Accept-Encoding: gzip,deflate,sdch
            Accept-Language: en-US,en;q=0.8
            Authorization: Basic <base64 encoded username:password>
        '''
        headers = {
            "Host": "%s" % self.hostname,
            "sfapikey": self.sf_apikey,
            "Accept": "text/html,application/xhtml+xml,application/xml;"
                      "q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "Content-Type": "application/json",
            "Authorization": self._get_basic_authorization_header_value()}
        return headers

    def _get_basic_authorization_header_value(self):
        encoded_credential = base64.encodestring('%s:%s' % (self.username,
                                                            self.password))
        value = '%s%s' % ('Basic ', encoded_credential)
        return value[:-1]  # removes last character which is a \n

    def identity_ticket_header(self):
        '''
        An identity ticket is used to give access to the
        Mediasite REST API
        Example:
        Identity Ticket
            GET https://mysite.mediasite.com/Mediasite/
                            api/v1/Presentations HTTP/1.1
            sfapikey: <your api key>
            Host: dev.mediasite.com
            Accept: text/html,application/xhtml+xml,
                              application/xml;q=0.9,image/webp,*/*;q=0.8
            Accept-Encoding: gzip,deflate,sdch
            Accept-Language: en-US,en;q=0.8
            Authorization: SfIdentTicket
            <base64 encoded username:password:ImpersonationUsername(optional)>
        '''
        headers = {
            "Host": "%s" % self.hostname,
            "sfapikey": self.sf_apikey,
            "Accept": "text/html,application/xhtml+xml,application/xml;"
                      "q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "Content-Type": "application/json",
            "Authorization":
                self._get_identity_authorization_header_value()}
        return headers

    def _get_identity_authorization_header_value(self):
        encoded_credential = base64.encodestring(
            '%s:%s:%s' % (self.username,
                          self.password,
                          self.impersonation_username))
        value = '%s%s' % ('SfIdentTicket ', encoded_credential)
        return value[:-1]  # removes last character which is a \n

    def authorization_ticket_header(self, sf_auth_ticket):
        '''
        An authorization ticket is used to give access to the
        Mediasite REST API
        @param sf_auth_ticket: sonicfoundry authorization ticket which is
                               created using the identity_ticket_header

        Example:
        Authorization Ticket
            GET https://mysite.mediasite.com/Mediasite/
                            api/v1/Presentations('<presentationId>') HTTP/1.1
            sfapikey: <your api key>
            Host: dev.mediasite.com
            Accept: text/html,application/xhtml+xml,
                              application/xml;q=0.9,image/webp,*/*;q=0.8
            Accept-Encoding: gzip,deflate,sdch
            Accept-Language: en-US,en;q=0.8
            Authorization: SfAuthTicket <authorization ticket>
        '''
        headers = {
            "Host": "%s" % self.hostname,
            "sfapikey": self.sf_apikey,
            "Accept": "text/html,application/xhtml+xml,application/xml;"
                      "q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "Content-Type": "application/json",
            "Authorization": "%s %s" % ("SfAuthTicket", sf_auth_ticket)}
        return headers

if __name__ == '__main__':
    pass
