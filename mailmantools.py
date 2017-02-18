from lxml import html
import requests


class MailmanTools:
    __headers = {'User-Agent': 'mailman-tools/0.1'}
    membersListUrlFormat = '{0}/mailman/admin/{1}/members/list'

    def __init__(self, url, listname, adminpw):
        self.url = url
        self.listname = listname
        self.__adminpw = adminpw

    def getmembers(self):
        params = self.__getbasequeryparams()
        page = requests.post(self.membersListUrlFormat.format(self.url, self.listname), headers=self.__headers,
                             params=params)
        pagehtml = html.fromstring(page.content)
        emailaddresses = pagehtml.xpath('//td/a/text()')
        return emailaddresses

    def __getbasequeryparams(self):
        return {'adminpw': self.__adminpw}
