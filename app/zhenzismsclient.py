# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse


class ZhenziSmsClient(object):
    def __init__(self, apiUrl, appId, appSecret):
        self.apiUrl = apiUrl
        self.appId = appId
        self.appSecret = appSecret

    def send(self, number, message, messageId=''):
        data = {
            'appId': self.appId,
            'appSecret': self.appSecret,
            'message': message,
            'number': number,
            'messageId': messageId
        }

        data = urllib.parse.urlencode(data).encode('utf-8');
        req = urllib.request.Request(self.apiUrl + '/sms/send.do', data=data);
        res_data = urllib.request.urlopen(req);
        res = res_data.read();
        res = res.decode('utf-8');
        return res;

    def balance(self):
        data = {
            'appId': self.appId,
            'appSecret': self.appSecret
        }
        data = urllib.parse.urlencode(data).encode('utf-8');
        req = urllib.request.Request(self.apiUrl + '/account/balance.do', data=data);
        res_data = urllib.request.urlopen(req);
        res = res_data.read();
        return res;
