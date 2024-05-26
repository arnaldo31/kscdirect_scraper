import requests

def Product(session:object,BSoup:object,url:str,category:str):
    
    while True:
        try:
            response = session.get(url,timeout=10)
            break
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
    soup = BSoup(response.text,'html.parser')
    
    dic = {}
    dic2 = {}
    dic['Category'] = category
    
    h2_tag = soup.find('h2')
    title = h2_tag.get_text(' ', strip=True).replace(h2_tag.find('small').get_text(' ', strip=True), '').strip()
    
    dic['Title'] = title
    
    dic2['Title'] = title
    dic2['KSCdirect Part #'] = ''
    dic2['Price'] = ''
    dic2['UPC'] = ''
    
    buy_it_now = soup.find(id='buy_it_now')
    if buy_it_now != None:
        try:
            trows = buy_it_now.find(class_='table').find_all('tr')
            for tr in trows:
                try:
                    th = tr.th.text.replace(':','').strip()
                except:
                    continue

                if 'KSCdirect Part #' in th or 'UPC' in th:
                    dic2[th] = tr.td.text.strip()
                    
                if 'On Hand' in th:
                    try:
                        td = tr.td.strong.text 
                    except:
                        td = ''
                    dic[th] = td
                    continue
                dic[th] = tr.td.text.strip()

        except:
            try:
                dic['KSCdirect Part #'] = soup.h2.small.text.replace('KSCdirect Part #:','').replace('(','').replace(')','').strip()
                dic2['KSCdirect Part #'] = dic['KSCdirect Part #']
            except:
                pass
            dic['Description'] = 'No found'
    
    try:
        extdesc = soup.find(id='extdesc')
        if extdesc != None:
            desk = extdesc.find(class_='panel-body').get_text('\n',strip=True).strip()
            dic['Details'] = desk
    except:
        dic['Details'] = ''
    
    specs = soup.find(id='specs')
    if specs != None:
        specs = specs.find_all('tr')
        for spec_tr in specs:
            try:
                th = spec_tr.th.text.strip()
                td = spec_tr.td.text.strip()
            except:
                continue
            dic[th] = td
    
    try:
        files = soup.find(id='files').a.get('href')
        dic['Supplemental Files'] = files
    except:
        pass
    
    try:
        image = soup.find(attrs={'data-toggle':'modal'}).img.get('src')
        dic['image'] = image
    except:
        pass
    
    addCart = soup.find(id='addToCart')
    if addCart != None:
        price = addCart.parent.h3.text.replace('Your Price:','').split('/')[0].strip()
        dic2['Price'] = price
        dic['Price'] = price
        
    dic['url'] = url
    return dic,dic2
            