from lxml import etree
import argparse
import os
import sys
import re
import unicodedata
import Stemmer
from string import digits

#load abbreviations
abbr = {}
with open('legabbr.csv','r') as abf:
    
    for l in abf.readlines():
        if l.split(',')[0] not in abbr.keys():
            abbr[l.split(',')[0]] = l.split(',')[1]

#load stopwords
stopw = []
with open('stopwords_it.txt', 'r') as f:
    for l in f.readlines():
        stopw.append(l[:-1])
      
def parseXML(xmlfile):
    
    tree = etree.parse(xmlfile)
    pt = tree.getroot()[1]  #pronuncia_testo
    
    text = ''
    for c in pt:
        if c.tag == 'epigrafe' or c.tag == 'testo' or c.tag == 'dispositivo':
            text += str(etree.tostring(c))
    
    text = re.sub('<[^>]*>', ' ', text) #remove tags
    text = text.replace('\\n', '\n').replace('&#13;', '\r') #newline, carriage return
    
    text = text.replace('&#224;', 'à').replace('&#232;', 'è').replace('&#233;', 'é').replace('&#236;','ì').replace('&#242;', 'ò').replace('&#249;', 'ù').replace('&#200;', 'È') #accented letters   
    
    text = text.replace('\t',' ').replace('  ', ' ') #remove multiple spaces
    #text = text.replace(r"\'"," ") #single quote
    
    
    #uncomment for topic modelling
    #remove digits
    remove_digits = str.maketrans('', '', digits)
    text = text.translate(remove_digits)

    #replace abbreviations
    for a in abbr.keys():
        if ' ' + a + ' ' in text or \
            '('+ a + ' ' in text or \
            "'"+ a + " " in text or \
            " "+ a + "." in text or \
            " "+ a + ")" in text:
            text = text.replace(a,abbr[a])
     
    text = text.lower() #to lowercase
    text = re.sub(r'[^\w\s]', '', text) #remove punctuation   

    #stemming
    stemmer = Stemmer.Stemmer('italian')
    wlist = stemmer.stemWords(text.split())

    #remove stopwords
    for s in stopw:
        for tk in wlist:
            if s == tk:
                wlist.remove(tk)
    
    text = ''
    for w in wlist:
        text += w+' '
    
    return text
    
def main():

    parser = argparse.ArgumentParser(description='Preprocess for Akoma Ntoso xml documents')
    parser.add_argument('-d', '--datadir', 
            action='store',
            default='test')
    parser.add_argument('-o', '--outdir',
            action='store',
            default='parsed')
    args = parser.parse_args()

    if os.path.exists(args.datadir):
        files = os.listdir(args.datadir)
    else:
        print('Invalid data directory')
        sys.exit()
    
    try:
        os.mkdir(args.outdir)
    except FileExistsError:
        print('Directory', args.outdir, 'already exists')
    except:
        print('Failed while creating directory', args.outdir)

    for f in files:
        try:
            
            parsed = parseXML(os.path.join(args.datadir,f))
            
            fname = f.split('/')[-1][:-3]
            with open(os.path.join(args.outdir, fname+'txt'), 'w') as of:
                of.write(parsed)
        
        except:
            print('failed while parsing file', f)
        
       
if __name__ == '__main__':
    main()
