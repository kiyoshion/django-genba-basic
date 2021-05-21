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

### ☺️ベストプラクティス　ープロジェクト構成ー

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

### ☺️ベストプラクティス　ーurls.pyはアプリ毎に作成するー

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

### ☺️ベストプラクティス　ーUser Modelの拡張ー

AbstractBaseUser > ガラッと拡張したい場合

AbstractUser > ちょろっと拡張したい場合

を継承する。上記を継承した場合、settings.pyでAUTH_USER_MODELを「accounts.CustomUser」に変更する。

### ☺️ベストプラクティス　ー発行されるクエリを確認するー

```python
>>>print(Book.objects.filter(title_icontains='Django').query)
SELECT "book"."id", "book"."title", "book"."image_path", "book"."publisher_id",  "book"."price", "book"."description", "book"."publish_date", "book"."created",  "book"."modified" FROM "book" WHERE "book"."title" LIKE %Django% ESCAPE'\'
```

### ☺️ベストプラクティス　ークエリ本数を減らすー

forで回すときなど、select_related()やprefetch_related()メソッドが使えないか検討する。

select_related() > 一や多　＞　一のリレーションをJOINで取得する

prefetch_related() > 一や多　＞　多のリレーションをJOINで取得する

## Template

HTMLファイルに変数を入れたり、フィルタしたりテンプレートの機能を拡張したりできる。


