# 現場で使えるDjangoの教科書（基礎編）

やりなおし。

## Djangoの処理の流れ

1. middleware
2. URLdispatcher > URLconfに登録されたURLパターンにマッチするViewを探して呼ぶ
3. view > リクエストから取得した入力値をフォームオブジェクトに変換してバリデーションを行う。
4. form
5. model > DB モデルオブジェクトを取得してビジネスロジックを実行する。
6. template > 取得したモデルオブジェクトやフォームオブジェクト、変数の内容をテンプレートにレンダリングしてレスポンスを作成する。
7. URL dispatcher > レスポンスや例外をハンドリングする。
8. middleware > レスポンスに後処理を行い、ブラウザに返す。

## Djangoの構成

Project Project modules App modules

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

### プロジェクト構成のベストプラクティス

project名をconfigやdefault,rootなど別名にしておくと良い。

```sh
mkdir mysite
cd mysite
django-admin startproject config .
```
