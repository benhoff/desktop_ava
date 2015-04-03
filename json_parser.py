import json
import urllib.request

class JSONParser(object):
    def __init__(self, url=None):
        if url is not None:
            self.data = self.get_data(url)
        else:
            self.data = None


    def get_data(self, url=None):
        if url is not None:
            request = urllib.request.urlopen(url)
            encoding = request.headers.get_content_charset()
            if encoding is None:
                encoding = 'utf-8'
            return json.loads(request.read().decode(encoding))
        else:
            return self.data
