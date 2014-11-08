import os
import sys

try:
    from bs4 import BeautifulSoup
except ImportError:
    print "BeautifulSoup is missing"
    sys.exit(1)

if __name__=="__main__":
	
    x=0
    fin = open('HasInput.txt','a+')
    fout = open('HasOutput.txt','a+')
    for name in sys.argv[1:] :	
        fname = "OWL-S 1.1/" + name        
	try:
           owl = open( fname ,'r').read()
        except IOError:
           print fname + " !!Open Error"
	   x = x + 1
        soup = BeautifulSoup(owl)
        profile_in = soup.findAll('profile:hasinput')
        profile_out = soup.findAll('profile:hasoutput')
        if profile_in is not None:
	   for inp in profile_in : 
	      in_attrs = dict(inp.attrs)
	      try:
                fin.write(in_attrs['rdf:resource'][2:] + "\n")
              except:
                print fname + " !!In format"
                x = x+1    
        if profile_out is not None:
    	   for out in profile_out :
              out_attrs = dict(out.attrs)
              try :   
                fout.write(out_attrs['rdf:resource'][2:] + "\n")
              except:
                print fname + "!!Out format" 
    print x
	
