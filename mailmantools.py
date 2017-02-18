from lxml import html
import requests


class MailmanTools:
    __headers = {'User-Agent': 'mailman-tools/0.1'}
    membersListUrlFormat = '{0}/mailman/admin/{1}/members/list'

    def __init__(self, url, listname, adminpw):
        self.url = url
        self.listname = listname
        self.__adminpw = adminpw
        self.__cachedmembers = []

    def getmembers(self, refresh=False):
        if refresh or len(self.__cachedmembers) == 0:
            params = self.__getbasequeryparams()
            page = requests.post(self.membersListUrlFormat.format(self.url, self.listname), headers=self.__headers,
                                 params=params)
            pagehtml = html.fromstring(page.content)
            members = pagehtml.xpath('//td/a/text()')
            self.__cachedmembers = members
            return members
        else:
            return self.__cachedmembers

    def getcache(self):
        return self.__cachedmembers

    def __getbasequeryparams(self):
        return {'adminpw': self.__adminpw}
