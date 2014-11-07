import os
import sys
import urllib

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
    
    pre="http://www.webservicex.net/WS/WSDetails.aspx?CATID=1&WSID="
    for i in range(1,79) :
	link=pre + str(i)
	print link
	page = br.open(link)
        html_code = page.read()
        soup = BeautifulSoup(html_code)
	try:        
		name_of_service = soup.find("font",{"face":"Arial"}).string.strip();
	except:
		print "NOT PRESENT"
		continue	
	print name_of_service
	file_name = "./wsdl_file/" + name_of_service + ".xml"
        wsdl_file = soup.find_all("font",{"face":"Verdana","color":"#000000"})	
	wsdl_file_link=wsdl_file[2].string	
	print wsdl_file_link
	try:	
		testfile = urllib.URLopener()
	except:
		print "error\n" 
		continue
	try:        
		testfile.retrieve(wsdl_file_link,file_name)
        except:
		print "errorX\n" 
		continue
	print("done with "+str(x))
    
	
