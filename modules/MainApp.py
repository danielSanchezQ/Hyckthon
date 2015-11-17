__author__ = 'Netwave'


import requests
import nmap
import re
from pprint import pprint
class HythonTools(object):
    def __init__(self):
        self.whoisinfo = None
        self.portScaner = nmap.PortScanner()
        self.ips = None

    def whois(self, url):
        request_str = "http://api.hackertarget.com/whois/?q={}".format(url)
        response = requests.get(request_str)
        self.whoisinfo = response.content
        return self.whoisinfo

    def loadIps(self):
        ipregex = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
        if self.whoisinfo:
            self.ips = re.findall(ipregex, self.whoisinfo)
        return self.ips

    def nmap(self, ip_url):
        self.portScaner.scan(ip_url,  arguments="--top-ports 25",sudo=False)
        return self.portScaner



class MainApp(object):
    def __init__(self):
        self.tools = HythonTools()
        self.optionlst  = ["Whois query", "Nmap", "Exit"]
        self.options    = { "Whois query":self.userwhois,
                            "Nmap"       :self.usernmap}
    def userwhois(self):
        url = raw_input("Input url to get info: ")
        pprint(self.tools.whois(url).split("\n"))

    def usernmap(self):
        ip = raw_input("Input ip to get info: ")
        pprint(self.tools.nmap(ip)[ip])

    def userIpsRange(self):
        pprint(self.tools.loadIps())


    def main(self):
        while True:
            print "Choose an option"
            for i,l in enumerate(self.optionlst):
                print str(i) + ": " + l
            option = int(raw_input("Wanna use (please input a number between 0 and " + str(len(self.optionlst)-1) + "): "))
            if option >= 0 and option < len(self.optionlst)-1:
                f = self.options[self.optionlst[option]]
                f()
                continue
            elif option == len(self.optionlst)-1:
                print "Bye!!"
                break
            else:
                print "Incorrect option, please try again"
                continue

if __name__ == "__main__":
    app = MainApp()
    app.main()
