import smtplib
from datetime import datetime

# from bs4 import BeautifulSoup
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
# from selenium.webdriver.chrome.service import Service

from myapp.models import *
from readnews import get_news


def login(request):
    return render(request,"loginindex.html")
    # return render(request,"User/lindex.html")


def login_post(request):
    username=request.POST['textfield']
    password=request.POST['textfield2']

    L=Login.objects.filter(username=username,password=password)
    if L.exists():
        L2 = Login.objects.get(username=username, password=password)
        request.session['lid']=L2.id
        if L2.type=='admin':
            return HttpResponse('''<script>alert('login successfully');window.location="/myapp/adminlink/"</script>''')
        if L2.type=='user':
            return HttpResponse('''<script>alert('login successfully');window.location="/myapp/userlink/"</script>''')


        else:
            return HttpResponse('''<script>alert('Invalid username or password');window.location="/myapp/login/"</script>''')
    else:
        return HttpResponse('''<script>alert('Invalid username or password');window.location="/myapp/login/"</script>''')

def adminlink(request):
    return render(request,"Admin/MAINS.html")

def userlink(request):
    return render(request,"User/MAINS.html")

def signup(request):
    return  render(request,"newsign.html")
def signup_post(request):
    Name=request.POST['textfield']
    Email=request.POST['textfield1']
    age=request.POST['textfield2']
    gender=request.POST['RadioGroup1']
    phno=request.POST['textfield4']
    password=request.POST['textfield3']
    confirm_password=request.POST['textfield5']


    log=Login()
    log.username=Email
    log.password=confirm_password
    log.type='user'
    log.save()
    obj=User()
    obj.name=Name
    obj.age=age
    obj.gender=gender
    obj.phno=phno
    obj.email=Email
    obj.LOGIN=log
    obj.save()
    return HttpResponse('''<script>alert('Registered Successfully');window.location="/myapp/login/"</script>''')


def changepassword(request):
    return render(request,"admin/chngpasswd.html")

def changepassword_post(request):
    currentpassword=request.POST['textfield']
    newpassword=request.POST['textfield2']
    confirmpassword=request.POST['textfield3']
    L2 = Login.objects.get(id=request.session['lid'])
    if L2.password==currentpassword:
        if newpassword==confirmpassword:
            L2.password=newpassword
            L2.save()
            return HttpResponse('''<script>alert('New password Created');window.location="/myapp/login/"</script>''')
        else:
            return HttpResponse('''<script>alert('Invalid');window.location="/myapp/changepassword/"</script>''')
    else:
        return HttpResponse('''<script>alert('Invalid');window.location="/myapp/changepassword/"</script>''')

def uchangepassword(request):
        return render(request,"User/uchngpasswd.html")

def uchangepassword_post(request):
        currentpassword = request.POST['textfield']
        newpassword = request.POST['textfield2']
        confirmpassword = request.POST['textfield3']
        L2 = Login.objects.get(id=request.session['lid'])
        if L2.password == currentpassword:

            L2.password = newpassword
            L2.save()
            return HttpResponse(
                '''<script>alert('New password Created');window.location="/myapp/login/"</script>''')

        else:
            return HttpResponse('''<script>alert('Invalid');window.location="/myapp/uchangepassword/"</script>''')


def addcategory(request):

    json_file_path = 'fg.json'

    # Read the JSON file into a pandas DataFrame
    import pandas as pd
    data = pd.read_json(json_file_path, lines=True)

    # Extract text and labels
    labels = data['category']
    a = []
    for i in labels:
        if i in a:
            continue
        a.append(i)

    return render(request,"admin/catadd.html",{"data":a})

def addcategory_post(request):
    category=request.POST['textfield']
    # image=request.FILES['fileField']

    if not Category.objects.filter(cat_name=category):

        c=Category()
        c.cat_name=category
    # f=FileSystemStorage()
    # date=datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg"
    # f.save(date,image)
    # path=f.url(date)
    # c.photo=path
        c.save()
    return HttpResponse('''<script>alert('category added');window.location="/myapp/viewcategory/"</script>''')

def updatecategory(request,id):
    json_file_path = 'fg.json'

    # Read the JSON file into a pandas DataFrame
    import pandas as pd
    data = pd.read_json(json_file_path, lines=True)

    # Extract text and labels
    labels = data['category']
    a = []
    for i in labels:
        if i in a:
            continue
        a.append(i)
    res=Category.objects.get(id=id)
    return render(request,"admin/catupdt.html",{'data':a,'data1':res})

def updatecategory_post(request):
    category=request.POST['textfield']
    id=request.POST['id']

    obj=Category.objects.get(id=id)

    if 'fileField' in request.FILES:
        image = request.POST['fileField']
        f = FileSystemStorage()
        date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
        f.save(date, image)
        path = f.url(date)
        obj.photo=path
        obj.save()

    obj.cat_name=category
    obj.save()
    return HttpResponse('''<script>alert('category updated');window.location="/myapp/viewcategory/"</script>''')

def viewcategory(request):
    res=Category.objects.all()
    return render(request,"admin/viewcategory.html",{"data":res})
def viewcategory_POST(request):
    search=request.POST['textfield']
    res = Category.objects.filter(cat_name__icontains=search)
    return render(request,"admin/viewcategory.html",{"data":res})

def deletecategory(request,id):
    res=Category.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('category deleted');window.location="/myapp/viewcategory/"</script>''')



def viewuserpreference(request):
    res=Preference.objects.filter(USER__LOGIN_id=request.session['lid'])
    return render(request,"user/viewuserpreference.html",{"data":res})
def viewuserpreference_POST(request):
    search=request.POST['textfield']
    res = Preference.objects.filter(name__icontains=search)
    return render(request,"user/viewuserpreference.html",{"data":res})

def deletepreference(request,id):
    res=Preference.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Preference deleted');window.location="/myapp/viewuserpreference/"</script>''')


# def preference(request):
#     return render(request,"User/preference.html")
# def preference_post(request):
#     entertainment=request.POST['checkbox']
#     sports=request.POST['checkbox1']
#     politics=request.POST['checkbox2']
#     businesseconomy=request.POST['checkbox3']
#     nationalinternational=request.POST['checkbox4']
#     editorial=request.POST['checkbox5']
#     return HttpResponse('''<script>alert('preferences are selected');window.location="/myapp/"</script>''')
#

def preference(request):
    a=Category.objects.all()
    return render(request,"User/addpreferences.html",{"data":a})

def preference_post(request):
    c=request.POST.getlist('ss')
    for i in c:
        if Preference.objects.filter(USER=User.objects.get(LOGIN_id=request.session['lid']), CATEGORY_id=i):
            continue
        obj=Preference()
        obj.USER=User.objects.get(LOGIN_id=request.session['lid'])
        obj.CATEGORY_id=i
        obj.save()
    return HttpResponse('''<script>alert('preferences are selected');window.location="/myapp/viewusernews/"</script>''')

def selectpreference(request):
    a=Category.objects.all()
    return render(request,"User/preference.html",{"data":a})

def selectpreference_post(request):
    c=request.POST['ss']
    pref=request.POST['textfield']

    obj=Preference()
    obj.USER=User.objects.get(LOGIN_id=request.session['lid'])
    obj.name=pref
    obj.CATEGORY_id=c
    obj.save()
    return HttpResponse('''<script>alert('preferences are selected');window.location="/myapp/viewusernews/"</script>''')


def reviews(request):
    return  render(request,"User/review.html")
def reviews_post(request):
    review=request.POST['textfield']
    from datetime import datetime
    date=datetime.now().date().today()
    obj=Review()
    obj.review=review
    obj.date=date
    obj.USER=User.objects.get(LOGIN=request.session['lid'])
    obj.save()
    return HttpResponse('''<script>alert('Review Submitted');window.location="/myapp/reviews/"</script>''')


def viewadminnews(request):
    import numpy as np
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    model = load_model('lstm_classifier_model.h5')

    # Load the label encoder
    label_encoder = np.load('label_encoder.npy', allow_pickle=True)

    # Example news data
    news = []
    title = []
    # author = []
    url = []
    urlToImage = []
    content = []
    publishedAt = []
    import requests
    r = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=d3dba61c5eaa40fba333738622785cc9")
    import json
    d = json.loads(r.content)
    for i in d['articles']:
        if str(i['description']) == 'None' \
                or str(i['title']) == 'None' \
                or str(i['url']) == 'None' \
                or str(i['urlToImage']) == 'None' \
                or str(i['content']) == 'None' \
                or str(i['publishedAt']) == 'None':
            continue
        publishedAt.append(i['publishedAt'])
        news.append(i['description'])
        title.append(i['title'])
        url.append(i['url'])
        # author.append(i['author'])
        urlToImage.append(i['urlToImage'])
        content.append(i['content'])

    # news = ["Health experts said it is too early to predict whether demand would match up with the 171 million doses of the new boosters the U.S. ordered for the fall.", "A political event occurred yesterday.", "The latest technology breakthrough was announced."]

    # Tokenize news text
    max_words = 1000  # Maximum number of words to tokenize
    # tokenizer = Tokenizer()
    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(news)
    sequences = tokenizer.texts_to_sequences(news)

    # Pad sequences to have uniform length
    maxlen = 50  # Maximum length of sequences
    # data = pad_sequences(sequences)
    data = pad_sequences(sequences, maxlen=maxlen)

    # Make predictions
    predictions = model.predict_classes(data)

    # print(predictions)

    json_file_path = 'fg.json'

    # Read the JSON file into a pandas DataFrame
    import pandas as pd
    data = pd.read_json(json_file_path, lines=True)
    ms = []
    l = []
    for i, index in zip(predictions, range(len(news))):
        from datetime import datetime, timezone
        timestamp = publishedAt[index]
        dt_object = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        local_dt_object = dt_object.astimezone()
        combined_date = local_dt_object.date()
        combined_time = local_dt_object.time()

        l.append({
            'description': news[index],
            'title': title[index],
            # 'author':author[index],
            'urlToImage': urlToImage[index],
            'url': url[index],
            'content': content[index],
            'combined_date': combined_date,
            'combined_time': combined_time,
        })
        print(l)
    return render(request, "designnews.html", {"data": l})
def viewadminnews_post(request):
    import numpy as np
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    model = load_model('lstm_classifier_model.h5')

    # Load the label encoder
    label_encoder = np.load('label_encoder.npy', allow_pickle=True)

    # Example news data
    news = []
    title = []
    # author = []
    url = []
    urlToImage = []
    content = []
    publishedAt = []
    import requests
    r = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=d3dba61c5eaa40fba333738622785cc9")
    import json
    d = json.loads(r.content)
    for i in d['articles']:
        if str(i['description']) == 'None' \
                or str(i['title']) == 'None' \
                or str(i['url']) == 'None' \
                or str(i['urlToImage']) == 'None' \
                or str(i['content']) == 'None' \
                or str(i['publishedAt']) == 'None':
            continue
        publishedAt.append(i['publishedAt'])
        news.append(i['description'])
        title.append(i['title'])
        url.append(i['url'])
        # author.append(i['author'])
        urlToImage.append(i['urlToImage'])
        content.append(i['content'])

    # news = ["Health experts said it is too early to predict whether demand would match up with the 171 million doses of the new boosters the U.S. ordered for the fall.", "A political event occurred yesterday.", "The latest technology breakthrough was announced."]

    # Tokenize news text
    max_words = 1000  # Maximum number of words to tokenize
    # tokenizer = Tokenizer()
    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(news)
    sequences = tokenizer.texts_to_sequences(news)

    # Pad sequences to have uniform length
    maxlen = 50  # Maximum length of sequences
    # data = pad_sequences(sequences)
    data = pad_sequences(sequences, maxlen=maxlen)

    # Make predictions
    predictions = model.predict_classes(data)

    # print(predictions)

    json_file_path = 'fg.json'

    # Read the JSON file into a pandas DataFrame
    import pandas as pd
    data = pd.read_json(json_file_path, lines=True)
    ms = []
    l = []
    for i, index in zip(predictions, range(len(news))):

            from datetime import datetime, timezone
            timestamp = publishedAt[index]
            dt_object = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            local_dt_object = dt_object.astimezone()
            combined_date = local_dt_object.date()
            combined_time = local_dt_object.time()

            l.append({
                'description': news[index],
                'title': title[index],
                # 'author':author[index],
                'urlToImage': urlToImage[index],
                'url': url[index],
                'content': content[index],
                'combined_date': combined_date,
                'combined_time': combined_time,
            })
            print(l)
    return render(request, "designnews.html", {"data": l})






def viewuserprofile(request):
    res =User.objects.all()
    return render(request,"admin/viewuserpro.html",{"data":res})
def viewuserprofile_post(request):
    search=request.POST['textfield']
    res = User.objects.filter(name__icontains=search)
    return render(request,"admin/viewuserpro.html",{"data":res})


import requests

def fetch_news(api_key, tags, page=1, page_size=100):
    api_key="42a175d5-75d6-4b11-af6e-e6e65b869837"
    mss=[]
    # print(tags,"Hurarrarararaaai")
    for tag in tags:
        # print(tag)
        # API endpoint URL with pagination parameters
        url = f"https://content.guardianapis.com/search?section={tag}&api-key={api_key}&page={page}&page-size={page_size}"

        # Send GET request to the API endpoint
        response = requests.get(url)


        # print(response,"huiihihihi")

        # Check if request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # print(data)

            # Extract relevant information from the response
            articles = data['response']['results']

            # Display the extracted information
            for article in articles:
                # print("sectionName:", article['sectionName'])
                # print("Title:", article['webTitle'])
                # print("URL:", article['webUrl'])
                # print("Section:", article['sectionName'])
                # print("Publication Date:", article['webPublicationDate'])
                # print("---------------------------")

                from datetime import datetime, timezone
                timestamp = article['webPublicationDate']
                dt_object = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                local_dt_object = dt_object.astimezone()
                combined_date = local_dt_object.date()
                combined_time = local_dt_object.time()

                mss.append(
                    {
                        'description': '',
                        'title': article['webTitle'],
                        # 'author':author[index],
                        'urlToImage': "/media/a.jpeg",
                        'url': article['webUrl'],
                        'content':article['webTitle'],
                        'combined_date':str(article['webPublicationDate']).split('T')[0],
                        'combined_time':combined_time,
                    'newsby': 'The Guardian News',
                    })


        else:
            print(f"Failed to fetch news for tag '{tag}':", response.status_code)
    return mss
# Example usage:



def viewusernews(request):
    # res =News.objects.all()
    import numpy as np
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    model = load_model('lstm_classifier_model.h5')

    # Load the label encoder
    label_encoder = np.load('label_encoder.npy', allow_pickle=True)

    # Example news data
    news = []
    title = []
    # author = []
    url = []
    urlToImage = []
    content = []
    publishedAt = []


    ress = Preference.objects.filter(USER__LOGIN__id=request.session['lid'])
    tags = []
    ntas = ''
    for j in ress:
        cat = j.CATEGORY.cat_name.lower()
        if cat == 'sports':
            cat = 'sport'
        tags.append(str(cat).lower())
        ntas = ntas+ ' OR '+cat
        # tags.append(str(j.CATEGORY.cat_name).lower())

    import requests
    # r = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=d3dba61c5eaa40fba333738622785cc9")
    r = requests.get("https://newsdata.io/api/1/news?apikey=pub_4168327df559976a0e9986d8b5305938780a8&q=" + ntas[3:])
    import json
    d = json.loads(r.content)
    for i in d['results']:

        if i['description'] in news:
            continue
        if str(i['description']) == 'None' \
                or str(i['title']) == 'None'\
                or str(i['link']) == 'None'\
                or str(i['image_url']) == 'None'\
                or str(i['content']) == 'None'\
                or str(i['pubDate']) == 'None'\
                or str(i['language']) != 'english':
            continue

        publishedAt.append(i['pubDate'])
        news.append(i['description'])
        title.append(i['title'])
        url.append(i['link'])
        # author.append(i['author'])
        urlToImage.append(i['image_url'])
        content.append(i['description'])

    # news = ["Health experts said it is too early to predict whether demand would match up with the 171 million doses of the new boosters the U.S. ordered for the fall.", "A political event occurred yesterday.", "The latest technology breakthrough was announced."]

    # Tokenize news text
    max_words = 1000  # Maximum number of words to tokenize
    # tokenizer = Tokenizer()
    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(news)
    sequences = tokenizer.texts_to_sequences(news)

    # Pad sequences to have uniform length
    maxlen = 50  # Maximum length of sequences
    # data = pad_sequences(sequences)
    data = pad_sequences(sequences, maxlen=maxlen)

    # Make predictions
    predictions = model.predict_classes(data)

    # for i in range(0,len(predictions)):
    #     print("==========================")
    #     print(news[i])
    #     print(predictions[i])
    #     print("===========================++++++++++++++++++")


    # print(predictions)

    json_file_path = 'fg.json'

    # Read the JSON file into a pandas DataFrame
    import pandas as pd
    data = pd.read_json(json_file_path, lines=True)

    # Extract text and labels
    labels = data['category']

    # print(labels)
    ms = []
    for i in labels:
        ms.append(i)

    # print(ms)


    l = []
    ns = []
    nns = []
    print(predictions)

    for i,index in zip(range(len(news)), range(len(news))):
        ress=Preference.objects.filter(USER__LOGIN__id=request.session['lid'])
        # for j in ress:
            # print(ms[i - 1], "res", j.CATEGORY.cat_name)
            # if str(ms[i-1]).lower() == j.CATEGORY.cat_name.lower():
                # l.append(news[index])

        from datetime import datetime, timezone
        timestamp = publishedAt[index]
        dt_object = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        local_dt_object = dt_object.astimezone()
        combined_date = local_dt_object.date()
        combined_time = local_dt_object.time()


        l.append({
            'description':str(news[index]),
            'title':title[index],
            # 'author':author[index],
            'urlToImage':urlToImage[index],
            'url':url[index],
            'content':content[index],
            'combined_date':combined_date,
            'combined_time':combined_time,
            'newsby': 'Indian News',
        })
        nns.append(news[index])


    # print("tags",tags)
    api_key = "42a175d5-75d6-4b11-af6e-e6e65b869837"
    # List of tags (sections)
    mss=fetch_news(api_key, tags)

    # print(mss)
    for i in mss:
        nns.append(i['title'])



    nlist= l+mss
    print(nlist)
    return render(request,"designnews.html",{"data":mss+l, 'news': nns})
    # return render(request,"designnews.html",{"data":l, 'news': news})

def viewusernews_post(request):
    search = request.POST['textfield']
    res =News.objects.filter(CATEGORY__cat_name__icontains=search)
    return render(request,"User/viewusernews.html",{"data":res})


def viewreviews(request):
    res = Review.objects.all()
    return render(request,"admin/viewuserreview.html",{"data":res})
def viewreviews_post(request):
    fromdate=request.POST['textfield']
    Todate=request.POST['textfield2']
    res=Review.objects.filter(date__range=[fromdate,Todate])

    return render(request,"admin/viewuserreview.html",{"data":res})

# def userlink(request):
#     return render(request,"User/userlink.html")

def forgotpassword(request):
    return render(request,"fgtpwd.html")

def forgotpassword_post(request):
    email = request.POST['textfield']
    res = Login.objects.filter(username=email)
    if res.exists():
        import random
        new_pass = random.randint(0000, 9999)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("shiblaj32000@gmail.com", "ndsg wada ilhm yddk")  # App Password
        to = email
        subject = "Test Email"
        body = "Your new password is " + str(new_pass)
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail("s@gmail.com", to, msg)
        # Disconnect from the server
        server.quit()
        ress = Login.objects.filter(username=email).update(password=new_pass)
        return HttpResponse(            '''<script>alert('New password added.Please check your email..');window.location='/myapp/login/'</script>''')
    else:
        return HttpResponse('''<script>alert('Invalid...');window.location='/myapp/forgotpassword/'</script>''')

def getscrapedcontent(request):
    import requests
    from bs4 import BeautifulSoup

    # Making a GET request
    r = requests.get('https://www.bbc.com/news/')

    # check status code for response received
    # success code - 200
    print(r)

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    s = soup.find('div', class_='sc-4fedabc7-0 kZtaAl')
    content = s.find_all('h2')
    x=soup.prettify()


    print(content)
    print (type(content))
    l  =[]
    for i in content:
        print(i)
        l.append(i)
    return render(request,"scraping.html",{"content":content})

def getcontentbbc(request):
    from selenium import webdriver


    page_url = "https://www.bbc.com/news/"
    service = Service(executable_path='chromedriver.exe')
    options=webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(page_url)
    rendered_html=driver.page_source
    soup=BeautifulSoup(rendered_html, "html.parser")
    divs = soup.find_all('div', class_="sc-b8778340-0 kFuHJG")

    h2s = []
    for i in divs:
        a = i.find('h2', class_="sc-4fedabc7-3 zTZri")
        b= i.find('img', class_="sc-a898728c-0 kbvxap")
        c= i.find('p', class_="sc-b8778340-4 kYtujW")
        d= i.find('span', class_="sc-df20d569-1 eGdGwi")
        e= i.find('span', class_="sc-ec7fe2bd-2 bLHjE")


        if a == None or d == None or d==None:
            continue
        h2s.append({
            'heading':a.text,
            'imgsrc':b['src'],
            'imgsrcset':b['srcset'],
            'content':c.text,
            'time':d.text,
            'place':e.text
        })
    driver.quit()

    return render(request,"scraping.html",{"divs":divs,'h2s':h2s})

def getcontenttoi(request):
    from selenium import webdriver


    page_url = "https://www.news18.com/"
    service = Service(executable_path='chromedriver.exe')
    options=webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(page_url)
    rendered_html=driver.page_source
    soup=BeautifulSoup(rendered_html, "html.parser")
    divs = soup.find_all('a', class_="jsx-d3ac634130accaec bell_wrpapper")

    h2s = []
    for i in divs:
        a = i.find('h1', class_="jsx-926f17af57ac97dc article_heading")
        b= i.find('img', class_="jsx-926f17af57ac97dc")
        c= i.find('div', class_="jsx-926f17af57ac97dc")
        d= i.find('time', class_="jsx-926f17af57ac97dc")
        e= i.find('p', class_="jsx-926f17af57ac97dc")

        print(b)


        if a == None or d == None or d==None:
            continue
        h2s.append({
            'heading':a.text,
            'imgsrc':b['src'],
            'imgsrcset':b['srcset'],
            'content':c.text,
            'time':d.text,
            'place':e.text,
        })
    driver.quit()

    return render(request,"scraping1.html",{"divs":divs,'h2s':h2s})




def viewusernewsog(request):
    # res =News.objects.all()
    import numpy as np
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    model = load_model('lstm_classifier_model.h5')

    # Load the label encoder
    label_encoder = np.load('label_encoder.npy', allow_pickle=True)

    # Example news data
    news = []
    title = []
    # author = []
    url = []
    urlToImage = []
    content = []
    publishedAt = []


    ress = Preference.objects.filter(USER__LOGIN__id=request.session['lid'])
    tags = []
    ntas = ''
    for j in ress:
        cat = j.CATEGORY.cat_name.lower()
        if cat == 'sports':
            cat = 'sport'
        tags.append(str(cat).lower())
        ntas = ntas+ ' OR '+cat
        # tags.append(str(j.CATEGORY.cat_name).lower())

    import requests
    r = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=d3dba61c5eaa40fba333738622785cc9")
    # r = requests.get("https://newsdata.io/api/1/news?apikey=pub_4168327df559976a0e9986d8b5305938780a8&q=" + ntas[3:])
    import json
    d = json.loads(r.content)
    for i in d['articles']:
        if str(i['description']) == 'None' \
                or str(i['title']) == 'None'\
                or str(i['url']) == 'None'\
                or str(i['urlToImage']) == 'None'\
                or str(i['content']) == 'None'\
                or str(i['publishedAt']) == 'None':
            continue
        publishedAt.append(i['publishedAt'])
        news.append(i['description'])
        title.append(i['title'])
        url.append(i['url'])
        # author.append(i['author'])
        urlToImage.append(i['urlToImage'])
        content.append(i['content'])

    # news = ["Health experts said it is too early to predict whether demand would match up with the 171 million doses of the new boosters the U.S. ordered for the fall.", "A political event occurred yesterday.", "The latest technology breakthrough was announced."]

    # Tokenize news text
    max_words = 1000  # Maximum number of words to tokenize
    # tokenizer = Tokenizer()
    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(news)
    sequences = tokenizer.texts_to_sequences(news)

    # Pad sequences to have uniform length
    maxlen = 50  # Maximum length of sequences
    # data = pad_sequences(sequences)
    data = pad_sequences(sequences, maxlen=maxlen)

    # Make predictions
    predictions = model.predict_classes(data)

    # for i in range(0,len(predictions)):
    #     print("==========================")
    #     print(news[i])
    #     print(predictions[i])
    #     print("===========================++++++++++++++++++")


    # print(predictions)

    json_file_path = 'fg.json'

    # Read the JSON file into a pandas DataFrame
    import pandas as pd
    data = pd.read_json(json_file_path, lines=True)

    # Extract text and labels
    labels = data['category']

    # print(labels)
    ms = []
    for i in labels:
        ms.append(i)

    # print(ms)


    l = []
    ns = []
    nns = []
    print(predictions)
    for i,index in zip(predictions, range(len(news))):
        ress=Preference.objects.filter(USER__LOGIN__id=request.session['lid'])
        for j in ress:
            # print(ms[i - 1], "res", j.CATEGORY.cat_name)
            if str(ms[i-1]).lower() == j.CATEGORY.cat_name.lower():
                # l.append(news[index])

                from datetime import datetime, timezone
                timestamp = publishedAt[index]
                dt_object = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                local_dt_object = dt_object.astimezone()
                combined_date = local_dt_object.date()
                combined_time = local_dt_object.time()


                l.append({
                    'description':str(news[index]),
                    'title':title[index],
                    # 'author':author[index],
                    'urlToImage':urlToImage[index],
                    'url':url[index],
                    'content':content[index],
                    'combined_date':combined_date,
                    'combined_time':combined_time,
                    'newsby': 'Indian News',
                })
                nns.append(news[index])

    # print(l)

    # print("tags",tags)
    api_key = "42a175d5-75d6-4b11-af6e-e6e65b869837"
    # List of tags (sections)
    mss=fetch_news(api_key, tags)

    # print(mss)
    for i in mss:
        nns.append(i['title'])




    return render(request,"designnews.html",{"data":mss+l, 'news': nns})
    # return render(request,"designnews.html",{"data":l, 'news': news})

def readnews(request):
    link=request.GET['link']
    a=get_news(link)
    print('Done')
    return JsonResponse({"data":str(a)})
    # return render(request,"designnews.html",{"data":res})