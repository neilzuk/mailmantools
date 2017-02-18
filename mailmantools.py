from lxml import html
import requests


class MailmanTools:
    __headers = {'User-Agent': 'mailmantools/0.0.1'}
    MEMBERS_LIST_URL_FORMAT = '{0}/mailman/admin/{1}/members/list'
    ADD_MEMBERS_URL_FORMAT = '{0}/mailman/admin/{1}/members/add'
    REMOVE_MEMBERS_URL_FORMAT = '{0}/mailman/admin/{1}/members/remove'

    def __init__(self, url, listname, adminpw):
        self.url = url
        self.listname = listname
        self.__adminpw = adminpw
        self.__cachedmembers = []

    def getmembers(self, refresh=False):
        if refresh or len(self.__cachedmembers) == 0:
            params = {'adminpw': self.__adminpw}
            page = requests.post(self.MEMBERS_LIST_URL_FORMAT.format(self.url, self.listname), headers=self.__headers,
                                 params=params)
            pagetree = html.fromstring(page.content)
            members = pagetree.xpath('//td/a/text()')
            self.__cachedmembers = members
            return members
        else:
            return self.__cachedmembers

    def hasmember(self, member):
        return member in self.__cachedmembers

    def addmember(self, member):
        if member not in self.__cachedmembers:
            params = {'adminpw': self.__adminpw, 'subscribe_or_invite': 0, 'send_welcome_msg_to_this_batch': 0,
                      'send_notifications_to_list_owner': 0, 'subscribees': member}
            page = requests.post(self.ADD_MEMBERS_URL_FORMAT.format(self.url, self.listname), headers=self.__headers,
                                 params=params)
            success = 'Successfully subscribed' in page.text
            if success:
                self.__cachedmembers.append(member)
            return success

    def removemember(self, member):
        if member in self.__cachedmembers:
            params = {'adminpw': self.__adminpw, 'send_unsub_ack_to_this_batch': 0,
                      'send_unsub_notifications_to_list_owner': 0, 'unsubscribees': member}
            page = requests.post(self.REMOVE_MEMBERS_URL_FORMAT.format(self.url, self.listname), headers=self.__headers,
                                 params=params)
            success = 'Successfully unsubscribed' in page.text
            if success:
                self.__cachedmembers.remove(member)
            return success

    def getcache(self):
        return self.__cachedmembers
