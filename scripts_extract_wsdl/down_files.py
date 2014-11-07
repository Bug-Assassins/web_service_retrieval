import os
import sys
import urllib

if __name__=="__main__": 
     x = 0
     for link in sys.argv :
     	if x == 0 :
         x = 1
         continue
	z=link.split("/"); 	
	y=z[5].split(".");
	file_name = "./wsdl_files/" + y[0] + ".xml"
     	try:	
	 	testfile = urllib.URLopener()
	except:
	 	print "error\n" 
	 	continue
	try:        
	 	testfile.retrieve(link,file_name)
        except:
	 	print "errorX\n" 
	 	continue
	print("done with "+str(x))
	
