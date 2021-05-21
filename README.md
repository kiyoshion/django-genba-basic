# 現場で使えるDjangoの教科書（基礎編） Django 3.2

Django 3.2で再会。

## Djangoの処理の流れ

1. middleware
2. URLdispatcher > URLconfに登録されたURLパターンにマッチするViewを呼び出す
3. view > リクエストから取得した入力値をフォームオブジェクトに変換してバリデーションを行う
4. form
5. model > DB モデルオブジェクトを取得してビジネスロジックを実行する。
6. template > 取得したモデルオブジェクトやフォームオブジェクト、変数の内容をテンプレートにレンダリングしてレスポンスを作成する。
7. URL dispatcher > レスポンスや例外をハンドリングする。
8. middleware > レスポンスに後処理を行い、ブラウザに返す。

## Djangoの構成

モジュール　＝　再利用できるファイル

### django-adminとmanage.py

Djangoには2種類の管理コマンドユーティリティがある。

#### django-admin

Djangoをインストールすると使える。どこからでも利用できる。

```buildoutcfg
django-admin startproject PrjName
```
#### manage.py

startprojectでプロジェクトを作成した際に自動で作成されるモジュール。

## DockerでDjangoをはじめる

See Docker document.

[Quickstart: Compose and Django](https://docs.docker.com/samples/django/)

```sh
docker-compose up
docker-compose run web django-admin startproject config .
```

### プロジェクト構成例

```sh
django-admin startproject mysite

mysite
  L manage.py
  L mysite
      L __init__.py
      L settings.py
      L urls.py
      L wsgi.py
cd mysite/
python3 manage.py startapp accounts

mysite
  L accounts
    L __init__.py
    L admin.py
    L apps.py
    L migrations
        L __init__.py
    L models.py
    L static
        L accounts
            L images
                L no-image.png
    L templates
        L accounts
            L login.html
    L tests.py
    L views.py
  L manage.py
  L mysite
      L __init__.py
      L settings.py
      L urls.py
      L wsgi.py
```

### ☺️ベストプラクティス　プロジェクト構成

project名をconfigやdefault,rootなど別名にしておくと良い。

```sh
mkdir mysite
cd mysite
django-admin startproject config .
```
## URLdispatcherとURLconf(Controller)

「正引き」・・・URLから対応するViewを取得する
「逆引き」・・・名前からURLを取得する

### URLconfを設定する

confgi/settings.py

```python
ROOT_URLCONF = 'config.urls'
```

### エラーハンドリング

URLdispatcherがマッチするView関数が見つからなかった場合、handler404というViewを介して404.htmlを返却する。

### ☺️ベストプラクティス　urls.pyはアプリ毎に作成する

django.urlsのinclude関数で各アプリのurls.pyを読み込む。django-admin startappではurls.pyファイルは作成されないので、自分で作る。docker-composeにbashでログインしてコマンドを実行する。

```sh
docker-compose exec web bash
django-admin startapp accounts
django-admin startapp shop
```

## View

Viewはリクエストオブジェクトを受け取ってレスポンスオブジェクトを返す役割。django.shotcutsパッケージにいろいろなレスポンスを作る関数がある。

### View関数　関数ベース vs クラスベース

View関数には関数ベースとクラスベースがあるが、Generic Viewという汎用性のあるクラスが用意されているのでクラスベースの方が恩恵を受けられる。

### django.views.generic.base

Viewには3つの汎用的なView関数がある。

1. django.views.generic.base.View
2. django.views.generic.base.TemplateView
3. django.views.generic.base.RedirectView

TemplateViewを使う場合は、プロジェクト直下にtemplatesディレクトリを作成してhtmlファイルを作成しておく。

config/settings.pyでTEMPLATEの'DIRS': [os.path.join(BASE_DIR, 'templates')],を設定しておく。

## model

ORMapper(Object-relational-mapper)。DBのテーブルとカラムの定義を、DjangoのModelクラスとクラス属性に対応させ、DBの差異を吸収する。

### Relation

一対一・・・OneToOneField
一対多・・・ForeignKey
多対多・・・ManyToManyField

### 単一のオブジェクトを取得する

Object.get()メソッドを使う。

### 複数件取得する

Object.all()もしくはObject.filter()メソッドを使う。

### オブジェクトの保存・更新

Object.save()メソッドを使う。

### オブジェクトの削除

Object.delete()メソッドを使う。

### ☺️ベストプラクティス　User Modelの拡張

AbstractBaseUser > ガラッと拡張したい場合

AbstractUser > ちょろっと拡張したい場合

を継承する。上記を継承した場合、settings.pyでAUTH_USER_MODELを「accounts.CustomUser」に変更する。

### ☺️ベストプラクティス　発行されるクエリを確認する

```python
>>>print(Book.objects.filter(title_icontains='Django').query)
SELECT "book"."id", "book"."title", "book"."image_path", "book"."publisher_id",  "book"."price", "book"."description", "book"."publish_date", "book"."created",  "book"."modified" FROM "book" WHERE "book"."title" LIKE %Django% ESCAPE'\'
```

### ☺️ベストプラクティス　クエリ本数を減らす

forで回すときなど、select_related()やprefetch_related()メソッドが使えないか検討する。

select_related() > 一や多　＞　一のリレーションをJOINで取得する

prefetch_related() > 一や多　＞　多のリレーションをJOINで取得する

## Template

DjangoはDTL(Django Template Language)というテンプレートエンジンが使える。HTMLファイルに変数を入れたり、フィルタしたりテンプレートの機能を拡張したりできる。

テンプレートにはコンテキスト(変数と値がマッピングされたオブジェクト)が渡されるので、テンプレートからはコンテキストに格納されている変数を使う。

context_processorsではデフォルトでいくつかの変数が使える。グローバル変数のようなもの。

|変数|用途|
|---|---|
|request|リクエストオブジェクト|
|user|サイトにアクセスしているユーザ|
|parms|サイトにアクセスしているユーザのパーミッション|
|messages|フラッシュメッセージ|

### ☺️ベストプラクティス　ベーステンプレートを用意する

headタグなど共通する部分はベーステンプレートを用意し、各テンプレートでextendsする。

## Form

Formは以下の機能を持つ。

1. ユーザの入力データを保持
2. 入力データのバリデーションを行い、検証済みのデータやエラ〜メッセージを保持

### Viewで使う

```python
form = LoginForm(request.POST)
is_valid = form.is_valid()
```

### Templateで使う

```python
{{ form }}
```

もしくはformをforで回す。

```python
{% for field in form%}
    <div class="field">
        <div class="ui input">{{field}}</div>
        {% if field.errors%}
            <p class="red message">{{ field.errors.0 }}</p>
        {% endif%}
    </div>
{% endfor%}
{% if form.non_field_errors%}
    <div class="ui red message">
        <ul class="list">
            {% for non_field_error in form.non_field_errors%}
                <li>{{ non_field_error }}</li>
            {% endfor%}
        </ul>
    </div>
{% endif%}
```

### CSRF対策

```python
{% csrf_token %}
```

### ☺️ベストプラクティス　ModelFormを継承する

Formの内容がモデルと重複する場合は、ModelFormを継承する。モデルのバリデーション処理が追加される。

```python
from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
```

## Middleware

MiddlewareはViewを出入りする、リクエストとレスポンスをフックすることができる。設定ファイルのMIDDLEWAREで記述した順に実行される。順番大事。

### デフォルトのMiddleware

#### SecurityMiddleware

リクエストとレスポンスをセキュリティ強化する。HTTPをHTTPSにリダイレクトしたり。

#### SessionMiddleware

sessionを有効にする。

#### CommonMiddleware

ユーザーエージェントのアクセス制限やURLリライティングなどを提供。デフォルトでURLの末尾に/を入れてくれる。

#### CsrfViewMiddleware

CSRFトークンを検証してくれる。POSTリクエストに送られてきたCSRFトークンの値を検証し、Cookieの値と異なるときは403エラーを返す。

 #### AuthenticationMiddleware

 リクエストのたびに、リクエストオブジェクトの中のuser属性にユーザ情報をセットする。ログイン済みの場合は、セッションに保管されているUserモデルのインスタンスをセットする。未ログインの場合は、AnymousUserクラスのオブジェクトをセットする。

 #### MessageMiddleware

 フラッシュメッセージを使えるようにする。

 #### XFrameOptionsMiddleware

クリックジャッキング対策する。

### ☺️ベストプラクティス　メッセージフレームワークを使う

デフォルトではCookieを使っている。リダイレクトしとき表示されない場合があるので、セッションに変更しておく。

```python
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
```

## 設定オブジェクトとsettings.py

See document

[Settings](https://docs.djangoproject.com/en/3.2/ref/settings/)

### INSTALLED_APPS

プロジェクトにappを追加したら、settings.pyにAppConfigクラスのサブクラスを追加する。

### Debug

開発中はデバッグしておく。

```python
DEBUG = True
```

### Static File

静的ファイルをブラウザへ返すだけなら、前段のNginxに任せる。

```python:settings.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_NAME = os.path.basename(BASE_DIR)

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = '/var/www/{}/static'.format(PROJECT_NAME)
```

|変数|説明|
|---|---|
|STATIC_URL|静的ファイル配信⽤のディレクトリで、 URL の⼀部になる。  設定値はデフォルトの 「/static/」 のままでよい|
|STATICFILES_DIRS|アプリケーションに紐付かない静的ファイルの置き場所|
|STATIC_ROOT|静的ファイルの配信元。  collectstatic コマンドで静的ファイルを集約する際のコピー先でもある。  「STATICFILES_DIRS」 とは別のディレクトリを指定する必要がある|

本番環境(DEBUG=False)の場合は、collectstaticコマンドでStaticファイルを集める必要がある。開発環境ではいらない。

```sh
python3 manage.py collectstatic
```

テンプレートでStaticファイルを読み込む場合は以下のように書く。

```python
{% load static %}
<img src={% static 'images/logo.png' %}>
```

### Media File

アクセスユーザがアップロードする画像などをメディアファイルと呼ぶ。

```python:settings.py
MEDIA_URL = '/media/
MEDIA_ROOT = '/var/www/{}/media'.format(PROJECT_NAME)
```

開発時にMediaファイルを読み込めるようにurls.pyに以下を追記しておく。

```python
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### DataBase

DATABASESにはDBのコネクション関連を設定する。

### Logging

LOGGINGSでロギングの設定をする。

### その他の設定

#### TEMPLATES

TEMPLATESにDIRSを設定しておく。

```python
TEMPLATES = [
    {
        'DIRS': [ps.path.join(BASE_DIR, 'templates')],
    },
]
```

#### LANGUAGE_CODE

```python
LANGUAGE_CODE = 'ja'
```

#### TIME_ZONE

```python
TIME_ZONE = 'Asia/Tokyo'
USE_TZ = True
```

#### ALLOWED_HOSTS

Djangoを配信する時のホストを指定する。DEBUG=Falseのときは必須。開発時は以下で良い。

```python
ALLOWED_HOSTS = ['*']
```

#### SECRET_KEY

Djangoの内部で暗号署名やハッシュ生成時に利用される。以下のコマンドで生成される。

```sh
python3 manage.py shell -c "from django.core.management import utils: pring(utils.get_random_secret_key())"
```

#### SITE_ID

Djangoサイトを識別するためのID。

### ☺️ベストプラクティス　開発環境の設定はlocal_settings.pyに書く

Dockerだと本番環境と同等なのでどうすべきか。

### ☺️ベストプラクティス　シークレットな変数は.envファイルに書く

django-environをインストールする。

```sh
docker-compose exec web bash // Dockerに入る
pip3 install django-environ
```

## Migration

1. makemigrations > migrationsファイルを作成する
2. migrate > DBにテーブルを作成する

### makemigrations

app内のmodels.pyを編集してから実行する。

```sh
python3 manage.py makemigrations
```

### migrate

作成したmigrationsファイルを実行し、DBに反映する。

```sh
python3 manage.py migrate
```
