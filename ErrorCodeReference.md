# エラーコード一覧

## 分類
- Error系(1000000 ~ 1999999) ... 処理停止
- Warning系(2000000 ~ 2999999) ... 処理継続

## 索引

### Error系
| Module      | File            | Codes             |
|-------------|-----------------|-------------------|
| Utils       | DataParser.py   | 1000001 ~ 1000003 |
| GoogleForms | FormsRequest.py | 1010001           |
| Data        | Payload.py      | 1020001 ~ 1020003 |
| Utils       | EventManager.py | 1030001           |

### Warning系
| Module | File             | Codes             |
|--------|------------------|-------------------|
| Utils  | DataParser.py    | 2000001           |
| VRCAPI | CookieManager.py | 2010001 ~ 2010002 |
| Data   | Category.py      | 2020001 ~ 2020002 |
| Data   | Platform.py      | 2030001           |
| Data   | Visibility.py    | 2040001           |

## Error系

- 1000000番台  

  | Error Code | Module | File          | Summary                  |
  |------------|--------|---------------|--------------------------|
  | 1000001    | Utils  | DataParser.py | config.iniに設定項目がない       |
  | 1000002    | Utils  | DataParser.py | config.iniに必須項目が入力されていない |
  | 1000003    | Utils  | DataParser.py | config.iniの設定値の形式が不正     |

- 1010000番台

  | Error Code | Module      | File            | Summary    |
  |------------|-------------|-----------------|------------|
  | 1010001    | GoogleForms | FormsRequest.py | イベントの登録に失敗 |
  
- 1020000番台

  | Error Code | Module | File       | Summary           |
  |------------|--------|------------|-------------------|
  | 1020001    | Data   | Payload.py | イベント開始日時が不正       |
  | 1020002    | Data   | Payload.py | イベント終了日時が不正       |
  | 1020003    | Data   | Payload.py | イベント終了日時が開始日時より過去 |

- 1030000番台

  | Error Code | Module | File            | Summary          |
  |------------|--------|-----------------|------------------|
  | 1030001    | Utils  | EventManager.py | config.iniの書式が不正 |

- 1040000番台

## Warning系

- 2000000番台  

  | Warning Code | Module | File          | Summary           |
  |--------------|--------|---------------|-------------------|
  | 2000001      | Utils  | DataParser.py | config.iniの設定値が不正 |

- 2010000番台

  | Warning Code | Module | File             | Summary       |
  |--------------|--------|------------------|---------------|
  | 2010001      | VRCAPI | CookieManager.py | Cookieが見つからない |
  | 2010002      | VRCAPI | CookieManager.py | Cookieデータが不正  |

- 2020000番台

  | Warning Code | Module | File        | Summary          |
  |--------------|--------|-------------|------------------|
  | 2020001      | Data   | Category.py | イベントカテゴリーの設定値が不正 |
  | 2020002      | Data   | Category.py | グループカテゴリーの設定値が不正 |

- 2030000番台

  | Warning Code | Module | File      | Summary         |
  |--------------|--------|-----------|-----------------|
  | 2030001      | Data   | Params.py | プラットフォームの設定値が不正 |

- 2040000番台

  | Warning Code | Module | File          | Summary     |
  |--------------|--------|---------------|-------------|
  | 2040001      | Data   | Visibility.py | 公開範囲の設定値が不正 |

- 2050000番台