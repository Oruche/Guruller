# info_collecter_from_gurunavi

- 飲食店情報の検索

## 準備
- ぐるなびAPIのアカウントを作成し、アクセスキーを環境変数に設定する。.bash_profileに書いてもよし
```
export GURUNAVI_API_KEY='自分のアクセスキー'
``` 

## 使用方法
- import
```
from get_info_from_gurunavi import info_collecter_from_gurunavi
```

- info_collecter_from_gurunaviクラスのインスタンスを作成
```
ic = info_collecter_from_gurunavi()
```

- リクエストURLを作成
    - リクエストパラメータはhttp://api.gnavi.co.jp/api/manual/restsearch/
```
ic.create_request_url('address=山梨県笛吹市境川町')
```

- リクエストを送る
```
ic.send_request()
```

- 通信が成功すると、info_collecter_from_gurunaviインスタンスのrest_dfのプロパティに、検索結果がpandasのDataFrameとして格納される。例えば、飲食店名を抽出する際は以下のようにアクセス。
```
ic.rest_df.loc[:,'name']
```

- データフレームをcsvファイルに書き出したいときは以下。(ファイル名はデフォルトで'rest.csv')
```
ic.write_to_csv('data.csv')
```

- 改めてリクエストを送りたい際は、以下のように改めてcreate_request_urlを呼び出す
```
ic.create_request_url('latitude=35.659272', 'longitude=139.697958','range=1')
ic.send_request()
```

# review_collecter_from_gurunavi

- レビュー情報の検索

## 準備
- ぐるなびAPIのアカウントを作成し、アクセスキーを環境変数に設定する。.bash_profileに書いてもよし
```
export GURUNAVI_API_KEY='自分のアクセスキー'
```

## 使用方法
- import
```
from get_review_from_gurunavi import review_collecter_from_gurunavi
```

- review_collecter_from_gurunaviクラスのインスタンスを作成
```
rc = review_collecter_from_gurunavi()
```

- リクエストURLを作成
    - リクエストパラメータはhttp://api.gnavi.co.jp/api/manual/photosearch/
```
rc.create_request_url('shop_id=g581402,g581405,a491700,a919400')
```

- リクエストを送る
```
rc.send_request()
```

- 通信が成功すると、review_collecter_from_gurunaviインスタンスのreview_dfのプロパティに、検索結果がpandasのDataFrameとして格納される。例えば、レビューのコメントを抽出する際は以下のようにアクセス。
```
rc.review_df.loc[:,'comment']
```

- データフレームをcsvファイルに書き出したいときは以下。(ファイル名はデフォルトで'review.csv')
```
rc.write_to_csv('shop_review.csv')
```

- 改めてリクエストを送りたい際は、以下のように改めてcreate_request_urlを呼び出す
```
rc.create_request_url('latitude=35.659272', 'longitude=139.697958','range=1')
rc.send_request()
```


