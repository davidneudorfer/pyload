# -*- coding: utf-8 -*-

from pyload.utils import json_loads
from pyload.plugin.Account import Account


class SimplyPremiumCom(Account):
    __name    = "SimplyPremiumCom"
    __type    = "account"
    __version = "0.01"

    __description = """Simply-Premium.com account plugin"""
    __license     = "GPLv3"
    __authors     = [("EvolutionClip", "evolutionclip@live.de")]


    def loadAccountInfo(self, user, req):
        json_data = req.load('http://www.simply-premium.com/api/user.php?format=json')
        self.logDebug("JSON data: " + json_data)
        json_data = json_loads(json_data)

        if 'vip' in json_data['result'] and json_data['result']['vip'] == 0:
            return {"premium": False}

        #Time package
        validuntil = float(json_data['result']['timeend'])
        #Traffic package
        # {"trafficleft": int(traffic), "validuntil": -1}
        #trafficleft = int(json_data['result']['traffic'])

        #return {"premium": True, "validuntil": validuntil, "trafficleft": trafficleft}
        return {"premium": True, "validuntil": validuntil}


    def login(self, user, data, req):
        req.cj.setCookie("simply-premium.com", "lang", "EN")

        if data['password'] == '' or data['password'] == '0':
            post_data = {"key": user}
        else:
            post_data = {"login_name": user, "login_pass": data['password']}

        html = req.load("http://www.simply-premium.com/login.php", post=post_data)

        if 'logout' not in html:
            self.wrongPassword()