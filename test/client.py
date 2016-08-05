'''
@author: aamvanderkraan

Just checking credential server, mediasite server and some filters
'''
import unittest
from mediasite.client import Client


class Test(unittest.TestCase):
    def testCredentialServerConnection(self):
        client = Client()
        result = client._get_home('Home')
        self.assertIn('ActiveCustomMetadata',
                      result,
                      'Cannot get data from the credential server')

    def testQuery(self):
        client = Client()
        result = client.get_resource('Presentations')
        self.assertIn('odata.count',
                      result,
                      'Cannot get data from the mediasite server')

    def testFilterStartswith(self):
        client = Client()
        result = client.get_resource('Presentations',
                                     query_options=""
                                     "$filter=startswith(Title,'AB')")
        self.assertIn('odata.count',
                      result,
                      'Cannot get data from the mediasite server')

    def testFilterTitleEquals(self):
        client = Client()
        result = client.get_resource('Presentations',
                                     query_options="$filter=Title eq 'bk'")
        self.assertIn('odata.count',
                      result,
                      'Cannot get data from the mediasite server')

if __name__ == "__main__":
    import sys
    sys.argv = ['',
                'Test.testCredentialServerConnection',
                'Test.testQuery',
                'Test.testFilterStartswith',
                'Test.testFilterTitleEquals'
                ]
    unittest.main()
