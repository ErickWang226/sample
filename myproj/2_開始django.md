建立第一個project
===
現在要來正式建立第一個project，首先確認是在虛擬環境env裡面，然後在human_design這個資料夾底下，確認無誤之後，在終端機下輸入這個指令
````
django-admin startproject myweb
````
顧名思義，建立一個叫做myweb的project，這樣取名是因為在django裡，一個project很像是一個網站的定位。完成時，會發現資料夾結構變成這樣
````
myproj
|--- myweb
|    |--- myweb
|    |    |--- __init__.py
|    |    |--- settings.py
|    |    |--- urls.py
|    |    |--- wsgi.py
|    |--- manage.py
|--- env (這裡面就是虛擬環境）
````
外層的myweb就是剛剛建立的主要project，要有個概念，之後寫的主要程式，都是發生在這個裡面，未來需要docker化，或是用git傳到github都是打包這裡就好。裡面那層hd_web則是django預設建立的，裡面會擺放了一些必要的程式，大概解釋一下：
>\_\_init\_\_.py : 在這個目錄裡面有這個檔案，代表django會把這裡當作是一個module，之後隨時可以用import把它叫出來，其他的我也不知道...抱歉

>settings.py : 這是這個專案的設定檔，很重要，在開發過程常常會需要來這裡改東西

>urls.py : 裡面擺了很多路徑，當伺服器接收到要求的時候，會看對方是要求哪個路徑，然後選用那個路徑對應的函數來執行

>wsgi.py : 等於是網頁伺服器跟程式之間的接口，想像成，網頁程式和python程式互相不熟，所以需要wsgi這個翻譯，當網頁請求過來的時候，wsgi.py就會啟動，然後把這個請求連接到django的設定檔settings.py，讓django開始跑  

可以稍微測試一下django的運作，先進入myweb
````
cd myweb
````
輸入以下指令
````
python manage.py runserver
````
進入提示的網址，應該可以看到django正在work。

安裝第一個app
-
再來安裝app，在django裡面，app可以把它想像成網站的某個功能，先輸入
````
python manage.py startapp myapp
````
這表示建立一個叫做myapp的app，通常會根據想要的功能取名，但這裡沒有這樣做。完成後資料結構變成
````
myproj
|--- myweb
|    |
|    |--- myweb
|    |    |--- __init__.py
|    |    |--- settings.py
|    |    |--- urls.py
|    |    |--- wsgi.py
|    |
|    |--- myapp
|    |    |--- migrations (資料相關)
|    |    |--- __init__.py
|    |    |--- admin.py
|    |    |--- apps.py
|    |    |--- models.py（些資料庫結構的地方)
|    |    |--- tests.py
|    |    |--- views.py (寫個個函數的地方）
|    |
|    |--- db.sqlite3 (這是資料庫的檔)
|    |--- manage.py
|
|--- hdenv (這裡面就是虛擬環境）
````
在django裡面，建立了一個app之後，需要去settings.py那裡宣告一下，也順便把其他要做的設定一起弄一弄，打開在myweb裡面的settings.py，增加以下


````
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
````
````
'DIRS': [TEMPLATE_DIR],
````
````
ALLOWED_HOSTS = ['*',]
````
````
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
]
````
然後在hd_app裡面新增一個資料夾templates，並且在裡面新增一個home.html檔案
````
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>
        test
    </h1>

</body>
</html>
````
到urls.py裡面，我們要新增一個路徑
````
from django.conf.urls import url
from django.contrib import admin
from myapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home')
]
````
到views.py去定義這個home函數
````
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')
````
上面的行動表示，當使用者輸入DNS，後面沒有加任何路徑的時候，url會去呼叫views裡面的home函數，根據home的功能，就會回應一個home.html的頁面。

可以執行一下
````
python manage.py runserver
````

發現頁面上出現test了，成功！

測試Docker
-
根據教學，每次都失敗，這次決定完成一小個步驟，就測試一次docker，來確認整體的過程中到底哪裡出錯。自己先google怎麼下載Docker。

在根目錄myweb底下（以後外層的myweb會另外說是根目錄）新增一個Dokerfile
>對於什麼是Dockerfile，現在是這樣理解的，每個Dockerfile都是一個container的製造說明書，之後可以用docker run來執行，或是用docker-compose up來把多個container製造且串起來
````
FROM python:3.6.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /docker_web
WORKDIR /docker_web
COPY ./ ./
RUN pip install -r requirements.txt
````
簡述內容:
1. 這個container是用python3.6.5為基底
2. 這個設定是讓我們容易偵錯？！不太確定
3. 建立名為docker_web資料夾
4. 指定進入到docker_web
5. 把Dockerfile檔案所在資料夾(myweb根目錄)的內容，複製一份去目前指定資料夾(docker_web)
6. 最後安裝requirements裡面的東西。

所以現在來製作一個requirements.txt
````
pip freeze > requirements.txt
````
順便補一下psycopg2，雖然在本機是用sqlite，但我打算在docker裡面要用postgres。

然後先到settings.py底下去改資料庫，增加下面這段，註解掉原本的
````
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'password123',
        'HOST': 'db',
        'PORT': 5432,
    }
}
````

接下來在myproj資料夾底下新增一個docker-compose.yml檔
````
version: '3'

services:

  db:
    container_name: db-container
    image: postgres
    environment:
      POSTGRES_PASSWORD: password123
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data/

  web:
    container_name: web-container
    build: ./myweb
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - web_data:/docker_web
    ports:
      - "8000:8000"
    depends_on:
      - db

volumes:
  pg_data:
  web_data:
````
稍微解釋一下:

1. 建立且連結兩個container，分別是db跟web。
2. db是直接去抓現有的image來做container
3. web則用myweb裡面的Dockerfile來建立的。
4. 分別給這兩個container一個volume，這個東西可以放想要永久保存的資料，不會因為重啟container就不見。其實不太懂。

好了之後，在終端機執行
````
docker-compose up
````
應該網頁還是看得到，代表docker這樣設定ok

>不過不明白為啥要用0.0.0.0:8000，試過不要這行失敗，改成127.0.0.1:8000也失敗。另外一開始還是沒成功，後來根據報錯，在docker_web裡面執行了
>```
>pip install psycopg2-binary
>```
>才成功，目前還不知道原因...

現在來再看一次資料結構，現在變成這樣
````
myproj
|--- myweb
|    |
|    |--- my_web
|    |    |--- __pycache__ (應該是python快取)
|    |    |--- __init__.py
|    |    |--- settings.py
|    |    |--- urls.py
|    |    |--- wsgi.py
|    |
|    |--- my_app
|    |    |--- __pycache__
|    |    |--- migrations (資料相關)
|    |    |--- templates (放html的地方）
|    |    |--- __init__.py
|    |    |--- admin.py
|    |    |--- apps.py
|    |    |--- models.py（些資料庫結構的地方)
|    |    |--- tests.py
|    |    |--- views.py (寫個個函數的地方）
|    |
|    |--- db.sqlite3 (這是資料庫的檔)
|    |--- manage.py
|    |--- requirements.txt
|    |--- Dockerfile
|
|--- env (這裡面就是虛擬環境）
|--- docker-compose.yml
````
接下來加上uWSGI來測試Docker
-
先在requirements.txt裡面增加uwsgi，當web-container啟動的時候就會安裝。
> 這裡卡很久，一開始直接加uwsgi，但再跑docker-compose的時候，發現一直沒有安裝uwsgi，後來把image刪除之後，才能順利跑起來，不曉得原因

然後稍微改一下docker-compose.yml裡面的一句
````
...
  web:
    container_name: web-container
    build: ./docker_web
    command: uwsgi --http :8000 --module myweb.wsgi
    ...
````
改成執行uwsgi，當有人呼叫8000端口，uwsgi就會跑去myweb裡面的wsgi呼叫django。

接著
````
docker-compose up
````
沒問題的話應該還是成功，現在運作方式如下
> web <---> uWSGI <---> django

> 記錄一下一個不確定的想法，在dockerfile裡面做了改變之後，最好刪掉image重新做一次，做得更動才會生效

用下面指令找出image的id，然後刪掉，或者可以全刪

````
docker images
````
````
docker rmi [id]
````
````
docker rmi $(docker images -q)
````
>後來發現好像除了container，image，其他還有像是volume，network也可以刪一刪，發生過我刪掉image，重新建立的時候，拷貝的檔案還是舊的，完全不知道怎麼回事。

下面是用來刪除volume的
````
docker volume prune
````

加上nginx來測試
-
先前的步驟已經完成了兩個單元，web單元(包含django+uwsgi)，database單元，現在要多加一個nginx單元，因為nginx主要處理靜態的東西，我們先把靜態的處理好，先在settings.py加上這一行
````
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
````
在myproj目錄底下新增一個資料夾nginx，要新增三個檔案，Dockerfile，my_nginx.conf，nginx.conf

先講Dockerfile
````
FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

COPY my_nginx.conf /etc/nginx/sites-available/
RUN mkdir -p /etc/nginx/sites-enabled/\
    && ln -s /etc/nginx/sites-available/my_nginx.conf /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]
````
簡述內容：
1. 會先去抓一個最新版nginx的image當做基底建立container
2. 會拷貝在當前nginx資料夾裡的nginx.conf執行檔，到container裡面的etc/nginx資料夾取代原始nginx.conf，新的nginx.conf只會修改兩個地方
3. 把新增的my_nginx.conf放到available裏，再用ln跟enabled連結
4. 用CMD執行nginx，原因不太懂，跟著做而已

先看一下更改過的nginx.conf，user改成root，最後一行改路徑去連接等等我們要改的my_nginx.conf
````
user  root;
# user  nginx;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    # include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-available/*;
}

````

再來是my_nginx.conf
````
# the upstream component nginx needs to connect to
upstream uwsgi {
    # server api:8001; # use TCP
    server unix:/docker_web/app.sock; # for a file socket
}

# configuration of the server
server {
    # the port your site will be served on
    listen    80;
    # index  index.html;
    # the domain name it will serve for
    # substitute your machine's IP address or FQDN
    server_name  localhost;
    charset     utf-8;

    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /media  {
        alias /docker_web/static/media;  # your Django project's media files - amend as required
    }

    location /static {
        alias /docker_web/static; # your Django project's static files - amend as required
    }

    location / {
        uwsgi_pass  uwsgi;
        include     /etc/nginx/uwsgi_params; # the uwsgi_params file you installed
    }

}
````
稍微解釋一下，用localhost開80端口，當使用者造訪 /，走動態路徑給uwsgi處理，這裡是用Unix sockets，接到uwsgi再給django。uwsgi和nginx之間的轉譯檔uwsgi_params應該是會內建在etc/nginx/裡面。

如果是造訪static，media，靜態頁面就直接nginx處理。這裡先在myweb根目錄底下建立static資料夾，在static裡面再建立子資料夾media，到時django+uwsgi那個container容器建立的時候也會把這兩個資料夾拷貝到docker_web底下，先拷貝一個圖片檔到media裏，等等測試

再來要設立一個ini啟動檔，通常直接取名uwsgi.ini，這個檔案也放在myweb根目錄下面

````
[uwsgi]

socket=app.sock
master=true
# maximum number of worker processes
processes=4
threads=2
# Django's wsgi file
module=myweb.wsgi:application

# chmod-socket=664
# uid=www-data
# gid=www-data

# clear environment on exit
vacuum          = true
````
最後要修正myproj底下的docker-compose.yml檔案，把這三個container串起來
````
version: '3'

services:

  db:
    container_name: db-container
    image: postgres
    environment:
      POSTGRES_PASSWORD: password123
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data/

  nginx:
    container_name: ng-container
    build: ./nginx
    restart: always
    ports:
      - "8080:80"
    volumes:
      - web_data:/docker_web
      - ./log:/var/log/nginx
    depends_on:
      - web

  web:
    container_name: web-container
    build: ./myweb
    # command: python manage.py runserver 0.0.0.0:8000
    # command: uwsgi --http :8000 --module myweb.wsgi
    command: uwsgi --ini uwsgi.ini
    volumes:
      - web_data:/docker_web
    ports:
      - "8002:8000"
    depends_on:
      - db

volumes:
  pg_data:
  web_data:
````
到此配置應該都完成了，可以看一下資料結構
````
myproj
|--- myweb
|    |
|    |--- my_web
|    |    |--- __pycache__ (應該是python快取)
|    |    |--- __init__.py
|    |    |--- settings.py
|    |    |--- urls.py
|    |    |--- wsgi.py
|    |
|    |--- my_app
|    |    |--- __pycache__
|    |    |--- migrations (資料相關)
|    |    |--- templates (放html的地方）
|    |    |--- __init__.py
|    |    |--- admin.py
|    |    |--- apps.py
|    |    |--- models.py（些資料庫結構的地方)
|    |    |--- tests.py
|    |    |--- views.py (寫個個函數的地方）
|    |
|    |--- static
|    |    |--- media
|    |
|    |--- uwsgi.ini
|    |--- .DS_Store (應該是postgres的資料檔)
|    |--- db.sqlite3 (這是資料庫的檔)
|    |--- manage.py
|    |--- requirements.txt
|    |--- Dockerfile
|   
|--- nginx
|    |--- Dockerfile
|    |--- my_nginx.conf
|    |--- nginx.conf
|
|--- env (這裡面就是虛擬環境）
|--- .DS_Store (應該是postgres的資料檔)
|--- docker-compose.yml
````
可以試看看了，localhost:8080，應該可以看到東西了，但進入/media/media.jpg卻還沒有東西。因為資料庫都還沒migrate，也要順便搜集一下靜態檔，用kitematic進入container(也可以用指令，自行google)，然後執行以下
````
python manage.py makemigrations myapp
````
````
python manage.py migrate
````
````
python manage.py collectstatic
````
現在再登入
````
http://localhost:8080/media/media.jpg
````
可以看到圖片了！爽！光是卡uwsgi+nginx+django+progres，差不多快一個月...有點想哭。

現在也體會一件事情：當初在查看教學的時候，總是很不解為什麼大家都不把教學寫得詳細一點，每次在閱讀，不同的教學都有不同的地方難以理解，但在經過一個月的碰壁後，可以理解，有些內容因為在碰壁的過程中漸漸地理解，變成知識，後來有點變成常識，所以後來當自己在寫的時候，會覺得因為是常識而省略，忘記當時什麼都不懂的自己...

目前整個網站收到request的流程圖
--
