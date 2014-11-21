import os
import sys

try:
    from bs4 import BeautifulSoup
except ImportError:
    print "BeautifulSoup is missing"
    sys.exit(1)

if __name__=="__main__":
	
	fname = "temp_owl.owls";        
	owl = open( fname ,'r').read()
        soup = BeautifulSoup(owl)
        profile_in = soup.findAll('profile:hasinput')
        profile_out = soup.findAll('profile:hasoutput')
	inp_str = []
	out_str = []         
	for inp in profile_in : 
	   in_attrs = dict(inp.attrs)
	   try:
           	inp_str.append(in_attrs['rdf:resource'][2:] + " ")
	   except:             
		break    
        for out in profile_out :
           out_attrs = dict(out.attrs)
           try :   
                out_str.append(out_attrs['rdf:resource'][2:] + " ")
           except:
                break 
 	inp_string = "".join(set(inp_str))
	out_string = "".join(set(out_str))
	print inp_string.strip() + ":" + out_string.strip()
