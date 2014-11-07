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
    
    x = 0
    for link in sys.argv :
        if x == 0 :
            x = 1
            continue
        page = br.open(link)
        html_code = page.read()
        soup = BeautifulSoup(html_code)
        name_of_service = soup.h2.span.string
	file_name = "./wsdl_files/" + name_of_service + ".xml"
        wsdl_file_link = soup.find("a",{"id":"WSDLURL"}).string
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
	
	
