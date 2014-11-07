import os
import sys
import eventlet
from eventlet.green import urllib2
from eventlet.timeout import Timeout
import urllib
import re

try:
    from mechanize import Browser
except ImportError:
    print "mechanize required but missing"
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print "BeautifulSoup is missing"
    sys.exit(1)

if __name__=="__main__":
    br = Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; \
              rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_handle_robots(False)
    
    x = 0
    fp = open("file_links_new.txt","a")
    for link in sys.argv :
        if x == 0 :
            x = 1
            continue
        try:
            page = br.open(link)
            html_code = re.sub('<script.*>.*</script>','',page.read())
            soup = BeautifulSoup(str(html_code))
            try :
                name_of_service = soup.find(attrs={'class':'service'}).h1.a.string
                file_name = "./wsdl_files/" + name_of_service + ".xml"
                wsdl_file_link = soup.find(attrs={'class':'tabBody'}).a.string
                fp.write(wsdl_file_link + "," + file_name + "\n")
                print("Succ="+str(x))
            except AttributeError:
                print("Att Error in " + str(x))
                ff = open("error_"+str(x)+"h","w")
                ff.write(html_code)
                ff.close()
                html_code = str(html_code).replace("&lt;","<").replace("&gt;",">")
                soup = BeautifulSoup(html_code)
                try :
                    print("\n\n\n\n\n\n\n")
                    print(soup)
                    print(soup.find(attrs={'class':'service'}))
                    name_of_service = soup.find(attrs={'class':'service'}).h1.a.string
                    file_name = "./wsdl_files/" + name_of_service + ".xml"
                    wsdl_file_link = soup.find(attrs={'class':'tabBody'}).a.string
                    fp.write(wsdl_file_link + "," + file_name + "\n")
                    print("Succ="+str(x))                    
                except :
                    print("Att Err : " + str(x))
                    ff = open("error_"+str(x), "w")
                    ff.write(soup.prettify())
                    ff.close()
            except UnicodeEncodeError:
                print("Unicode Error : \nwsdl : " + wsdl_file_link + "\nfile : " + file_name)
                file_name = "service_" + str(x)
                fp.write(wsdl_file_link + "," + file_name + "\n")
            except :
                print("Random Error in :" + str(x))
        except urllib2.URLError:
            print("URL Error in : " + str(x))
        except :
            print("Last Error in : " + str(x))
        x = x + 1

    fp.close()
