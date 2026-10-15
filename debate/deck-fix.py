import re,sys,zipfile,shutil
src,dst=sys.argv[1],sys.argv[2]
zin=zipfile.ZipFile(src); zout=zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED)
def strip(m):
    b=m.group(0)
    b=re.sub(r'<a:hlinkClick[^>]*/>','',b)
    b=re.sub(r'<a:hlinkClick[^>]*>.*?</a:hlinkClick>','',b,flags=re.S)
    b=b.replace(' u="sng"','')
    return b
for it in zin.infolist():
    data=zin.read(it.filename)
    if re.match(r'ppt/slides/slide\d+\.xml$',it.filename):
        x=data.decode('utf8')
        x=re.sub(r'<a:rPr\b[^>]*[^/]>.*?</a:rPr>',strip,x,flags=re.S)
        x=x.replace(' u="sng"','')
        data=x.encode('utf8')
    zout.writestr(it,data)
zout.close()
