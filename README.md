# VERM: VRC Event calendar Registration Manager

**本システムはVRCイベントカレンダーに自動でイベントを登録するシステムです**  
**開発者は、本システムを利用する上で発生したいかなる問題についても責任を負いません**  
**利用者は自己責任の範疇で利用するようお願いします**

**※ 本ツールは Windows 環境向けです。**

## 前提
- **Pythonバージョン3.12以降インストール済み**
- **gitインストール済み**

## インストール方法

### ダウンロード
コマンドプロンプトで以下を実行
```bash
git clone https://github.com/gerusura-dev/VERM.git
```

### 環境構築
cloneしてきたフォルダ内の「setup_env」をダブルクリックする  
（拡張子が表示される設定の場合、「setup_env.bat」を探してダブルクリック）

### タスクスケジューラーにタスクを登録
cloneしてきたフォルダ内の「task_register」を管理者権限で実行する  
（拡張子が表示される設定の場合、「task_register.bat」を探して実行）

### タスクスケジューラーからタスクを削除（もし定期実行が不要になった場合に実行）
cloneしてきたフォルダ内の「task_delete」を管理者権限で実行する  
（拡張子が表示される設定の場合、「task_delete.bat」を探して実行）

### config.iniファイルを設定
cloneしてきたフォルダ内にある「config.ini.sample」を説明に従って記載し、「config.ini」に名前を変える

### アップデート
本プロジェクトのアップデートを適用するには、コマンドプロンプトでcloneしたフォルダ内から以下を実行
```bash
git pull
```
