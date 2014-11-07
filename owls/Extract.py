import os
import sys
import glob
import subprocess
from os import listdir
try:
    from bs4 import BeautifulSoup
except ImportError:
    print "BeautifulSoup is missing"
    sys.exit(1)

if __name__=="__main__":
    file_count = 0
    fp = open("indexed_services","w+")
    for fname in os.listdir("docs"):
        try : 
            owl = open( "docs/" + fname ,'r').read()
        except IOError:
            print "Error Processing File : docs/" + fname
        soup = BeautifulSoup(owl)
        profile_in = soup.find_all('profile:hasinput')
        profile_out = soup.find_all('profile:hasoutput')

        in_str = []
        op_str = []

        keyerr = 0
        for inp in profile_in :
            in_attrs = dict(inp.attrs)
            try :
                in_str.append(in_attrs['rdf:resource'])
            except KeyError, e:
                keyerr = 1

        if keyerr == 1:
            process_in = soup.find_all('process:hasinput')
            in_str = []
            for inp in process_in : 
                in_attrs = dict(inp.attrs)
                try :
                    in_str.append(in_attrs['rdf:resource'])
                except KeyError, e:
                    print "Error Input (Key): " + fname

        inp_string = " ".join(set(in_str))
        inp_vec = subprocess.check_output(['bash index_unit.sh', inp_string])

        keyerr = 0
        for out in profile_out :
            out_attrs = dict(out.attrs)
            try :
                op_str.append(out_attrs['rdf:resource'])
            except KeyError, e:
                keyerr = 1

        if keyerr == 1:
            process_out = soup.find_all('process:hasoutput')
            op_str = []
            for out in process_out : 
                out_attrs = dict(out.attrs)
                try :
                    op_str.append(out_attrs['rdf:resource'])
                except KeyError, e:
                    print "Error Output (Key): " + fname

        out_string = " ".join(set(op_str))

        out_vec = subprocess.check_output(['bash index_unit.sh', out_string])
        fp.write(fname + " : " + inp_vec + " : " + out_vec)
        file_count += 1
        
    print "Total Files Processed : ", file_count