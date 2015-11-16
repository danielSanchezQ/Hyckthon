__author__ = 'Netwave'


import requests
import nmap
from pprint import pprint
class HythonTools(object):
    def __init__(self):
        self.whoisinfo = None
        self.portScaner = nmap.PortScanner()

    def whois(self, url):
        request_str = "http://api.hackertarget.com/whois/?q={}".format(url)
        response = requests.get(request_str)
        self.whoisinfo = response.content
        pprint(self.whoisinfo.split("\n"))
        return self.whoisinfo

    def nmap(self, ip_url):
        self.portScaner.scan(ip_url,  arguments="--top-ports 25",sudo=False)
        pprint(self.portScaner[ip_url])
        return self.portScaner



class MainApp(object):
    def __init__(self):
        self.tools = HythonTools()

    def userwhois(self):
        url = raw_input("Input url to get info: ")
        self.tools.whois(url)

    def usernmap(self):
        ip = raw_input("Input ip to get info: ")
        self.tools.nmap(ip)

if __name__ == "__main__":
    app = MainApp()
    optionlst = ["Whois query", "Nmap", "Exit"]
    options = {"Whois query":app.userwhois,
               "Nmap"       :app.usernmap}
    while True:
        print "Choose an option"
        for i,l in enumerate(optionlst):
            print str(i) + ": " + l
        option = int(raw_input("Wanna use (please input a number between 0 and " + str(len(optionlst)-1) + "): "))
        if option >= 0 and option < len(optionlst)-1:
            f = options[optionlst[option]]
            f()
            continue
        elif option == len(optionlst)-1:
            print "Bye!!"
            break
        else:
            print "Incorrect option, please try again"
            continue
