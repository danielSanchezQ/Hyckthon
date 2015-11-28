__author__ = 'Netwave'


import requests
import nmap
import re
import json
import socket
import ipwhois
from pprint import pprint
class HythonTools(object):
    whois_url   = "http://api.domaintools.com/v1/domaintools.com/whois/?q={}"
    ip_url      = "http://api.domaintools.com/v1/domaintools.com/hosting-history/?q={}"
    ipregex     = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"

    def __init__(self):
        self.whoisinfo  = None
        self.ipinfo     = None
        self.portScaner = nmap.PortScanner()
        self.ips        = None
        self.nmapinfo   = None

    def whois(self, url):
        request_str     = HythonTools.whois_url.format(url)
        response        = requests.get(request_str)
        self.whoisinfo  = json.loads(response.content)
        self.ips        = ipwhois.IPWhois(socket.gethostbyname(url)).lookup()
        iprequest_str   = HythonTools.ip_url.format(self.ips)
        ipresponse      = requests.get(iprequest_str)
        self.whoisinfo['response'].update(json.loads(ipresponse.content))
        return self.whoisinfo

    def loadIps(self):
        #if self.whoisinfo:
        #    self.ips = set(sorted(re.findall(HythonTools.ipregex, str(self.ipinfo))))
        return self.ips["asn_cidr"]

    def servers(self):
        return self.whoisinfo['response']['name_servers']

    def nmap_ping(self, ip_url):
        self.portScaner.scan(ip_url,  arguments="--top-ports 25",sudo=False)
        return self.portScaner.all_hosts()

    def nmap_ports(self, host):
        return [self.portScaner[host][prot] for prot in self.portScaner[host].all_protocols()]



class MainApp(object):
    def __init__(self):
        self.tools = HythonTools()
        self.optionlst  = ["Whois query", "Query ip ranges", "Get server names", "Nmap ping", "Get Ports", "Exit"]
        self.options    = { "Whois query"       :self.userwhois,
                            "Get server names"  :self.servernames,
                            "Nmap ping"         :self.usernmap,
                            "Get Ports"         :self.nmapports,
                            "Query ip ranges"   :self.userIpsRange}
    def userwhois(self):
        url = raw_input("Input url to get info: ")
        pprint(self.tools.whois(url))

    def servernames(self):
        pprint(self.tools.servers())

    def usernmap(self):
        ip = raw_input("Input ip to get info: ")
        pprint(self.tools.nmap_ping(ip))

    def nmapports(self):
        print 'Host scanned:'
        for i, h in enumerate(self.tools.portScaner.all_hosts()):
            print i, h
        ip = raw_input("Input index to show port info: ")
        pprint(self.tools.nmap_ports(self.tools.portScaner.all_hosts()[int(ip)]))

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
