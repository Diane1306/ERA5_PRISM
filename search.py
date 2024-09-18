import argparse
import os  
import os.path

#Search string
search_string = "conda env"

#Search current directory
directory ='.'


parser = argparse.ArgumentParser(description='Search ipython notebooks.')
parser.add_argument('search_string',type=str, help='Our search term')
parser.add_argument('--dir',type=str,default='.')
args = parser.parse_args()

# search_string = search_string.lower()
search_string = args.search_string
directory = args.dir
links=[]

files = os.listdir(directory)
files.sort()
for fn in os.listdir(directory):
    filename = f"{directory}/{fn}"
    if 'ipynb' in fn:
        if os.path.isfile(filename):
            found = False
            with open(filename,'r', encoding="utf8") as fp:  #add ', encoding="utf8"' here
                for line in fp:
                    line = line.lower()
                    if search_string in line:
#                         links.append("<a href="+fn+" target=\"_blank\" >"+fn+"</a></br>")
                        links.append(f"{filename}\n")
                        break
if links:
    print(' '.join(links))
else:
    print('string ('+search_string+') not found.')