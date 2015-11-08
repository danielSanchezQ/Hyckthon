__author__ = 'Netwave'


import whois
from pprint import pprint
class HythonTools(object):
    def __init__(self):
        self.whoisinfo = None

    def whois(self, url):
        self.whoisinfo = whois.query(domain=url)
        pprint(self.whoisinfo)
        return self.whoisinfo

    def nmap(self):
        pass


class MainApp(object):
    def __init__(self):
        self.tools = HythonTools()

    def userwhois(self):
        url = raw_input("Input url to get info: ")
        self.tools.whois(url)


if __name__ == "__main__":
    app = MainApp()
    optionlst = ["Whois query", "Exit"]
    options = {"Whois query":app.userwhois}
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
