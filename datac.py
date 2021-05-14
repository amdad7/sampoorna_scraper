from bs4 import BeautifulSoup
import sqlite3
import re
import requests
import time
conn=sqlite3.connect('8Bdatabase.sqlite3')
cur=conn.cursor()
cur.executescript('''

DROP TABLE IF EXISTS data;
CREATE TABLE data (
   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
   name TEXT NOT NULL ,
   admission_no INTEGER,
   gender TEXT,
   uid INTEGER,
   mothers_name TEXT,
   fathers_name TEXT,
   occupation TEXT,
   rationcard TEXT,
   address ,
   phone_no ,
   dob ,
   religion TEXT,
   caste TEXT,
   category TEXT,
   blood_group
);
''')
headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}
login_data={
'user[username]': 'jdt8b',
'user[password]': 'jdteightb',
'commit': 'Login'
}
with requests.session() as s:
    url='https://sampoorna.kite.kerala.gov.in:446/'
    r=s.get(url, headers=headers)
    soup=BeautifulSoup(r.content,'html5lib')
    login_data['authenticity_token']=soup.find('input', attrs={'name':'authenticity_token'})['value']
    r=s.post(url, data=login_data , headers=headers)
    list=[]
    for _ in range(2):
        ur=input('url:  ')
        r=s.get(ur, headers=headers)
        soup=BeautifulSoup(r.content,'html.parser')
        tags=soup('div')
        for tag in tags:
            attr=tag.attrs
            try:
                if attr['class'][0]=='category-full-name':
                    lin=tag.a.get('href')
                    lin= 'https://sampoorna.kite.kerala.gov.in:446'+str(lin)
                    list.append(lin)
            except:
                pass
    print('*****student url collected succesfully*******')
    print('******number of students***** :>>',len(list))
    h=0
    print('------initiating data collection------')
    time.sleep(5)
    for i in list:
        r=s.get(i,headers=headers)
        data=r.content
        soup=BeautifulSoup(data,"html.parser")
        tags=soup('div')
        lis,count=[],0
        for i in tags:
            att=i.attrs
            try:
                if att['class'][0]=="attribute-value":
                    count+=1
                    b=i.contents
                    if len(b)==0:
                        con='-'
                    else:
                        con=b[0]
                    lis.append(con)
            except:
                pass
        print(len(lis))
        if len(lis)!=70 and len(lis)!=71:
            address=lis[24]+ ' ' +lis[25]+' '+lis[27]+' '+lis[28]+' '+lis[30]+'po'+' '+lis[29]+(' ')+lis[26]+(',')+lis[29]
            pn=re.findall('[0-9]+',lis[31])
            if len(pn)==0:
                pn='-'
            else :
                pn=pn[0]
            db=re.findall('[0-9 or /]+',lis[40])
            db=db[0]

            cur.execute('''
            INSERT INTO data (name,admission_no,gender,uid,mothers_name,fathers_name,occupation,rationcard,
            address,phone_no,dob,religion,caste,category,blood_group) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(lis[0],int(lis[2]),lis[4],int(lis[8]),lis[15],lis[17],lis[21],lis[23],address,pn,db,lis[43],lis[44],lis[45],lis[46]))
            conn.commit()
            print('done')
            h+=1
        else:
            address=lis[24]+ ' ' + lis[25]+ ' ' +lis[30]+' '+lis[30]+' '+lis[29]+' '+lis[32]+'po'+' '+lis[28]+' '+lis[26]+ ' '+lis[31]
            pn=re.findall('[0-9]+',lis[33])
            if len(pn)==0:
                pn='-'
            else :
                pn=pn[0]
            db=re.findall('[0-9 or /]+',lis[42])
            db=db[0]

            cur.execute('''
            INSERT INTO data (name,admission_no,gender,uid,mothers_name,fathers_name,occupation,rationcard,
            address,phone_no,dob,religion,caste,category,blood_group) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(lis[0],int(lis[2]),lis[4],int(lis[8]),lis[15],lis[17],lis[21],lis[23],address,pn,db,lis[45],lis[46],lis[47],lis[48]))
            conn.commit()
            print('--student-',h,'  ','**uploaded**')
            h+=1
        print('--student-',h,'  ','**uploaded**')
    print('### database_compiled_succesfully')
    print('---acces database via sqlite3--' )
    print('%% database location is same folder as datacprogram %%')
