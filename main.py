import requests,json,hashlib

if __name__=='__main__':
    
    phonenum=input("Phonenumber:")
    passwd=input("Share password:")
    phonenum_md5=hashlib.md5((phonenum).encode()).hexdigest()
    x="https://rcopy.nikola-lab.cn/server2/user-panel/user-tag-data-manager/index.html#/login?uuid="+str(phonenum_md5)
    headers={
        'Accept': 'application/json, text/plain, */*',
        'Content-Type':'application/json;charset=UTF-8'
    }
    req1=requests.post(headers=headers,url="https://rcopy.nikola-lab.cn/server2/thinkphp/public/index.php/api/Importexport/userLogin",data=json.dumps({"username":phonenum_md5,"password":passwd}))
    data={}
    if req1.status_code==200:
        data={}
        token=""
        try:
            data=json.loads(req1.text)
            token=data.get('data')
        except:
            if(req1.text=="0"):
                print("password error")
            else:
                print(req1.text)
            exit(0)
        req2=requests.post(headers=headers,url="https://rcopy.nikola-lab.cn/server2/thinkphp/public/index.php/api/Importexport/pullCardBagData",data=json.dumps({"token":token,"phone":phonenum_md5}))
        data2=json.loads(req2.text)
        x=data2.get("data")
        for Card in x:
            id=str(Card.get('id'))
            CardData=Card.get('data')
            taginfo=CardData.get('tag_info')
            nick_name=Card.get('nick_name')
            tagtype=taginfo.get('tag_type')
            sak=taginfo.get('sak_hex')
            Carduid=taginfo.get('uid_hex')
            atqa=taginfo.get('atqa_hex')
            print("-------")
            print("Card id:"+id)
            print("Card nickname:"+nick_name)
            print("Card tag type:"+tagtype)
            print("Card sak:"+sak)
            print("Card uid:"+Carduid)
            print("Card atqa:"+atqa)
            print("-------")
            tag_data=CardData.get('tag_data')
            writedata=[]
            for dict in tag_data:
                for hexx in dict:
                    writedata.append(hexx.to_bytes(1,'big'))
            with open(Carduid+"_"+id+"_"+nick_name+"_"+tagtype+"_"+atqa+".dump","wb") as f:
                for x in writedata:
                    f.write(x)
    else :
        print("network error")