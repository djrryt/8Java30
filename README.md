<div id="top"></div>

## 使用技術一覧

<p style="display: inline">
  <!-- フロントエンドのフレームワーク一覧 -->
  <img src="https://img.shields.io/badge/-Node.js-339933.svg?logo=node.js&style=for-the-badge">
  <img src="https://img.shields.io/badge/-Gulp-DA4648.svg?logo=gulp&style=for-the-badge">
  <img src="https://img.shields.io/badge/-Sass-CC6699.svg?logo=sass&style=for-the-badge">
  <img src="https://img.shields.io/badge/-Npm-CB3837.svg?logo=npm&style=for-the-badge">
  <!-- フロントエンドの言語一覧 -->
  <img src="https://img.shields.io/badge/-Html5-E34F26.svg?logo=html5&style=for-the-badge">
  <img src="https://img.shields.io/badge/-Css3-1572B6.svg?logo=css3&style=for-the-badge">
  <img src="https://img.shields.io/badge/-Javascript-F7DF1E.svg?logo=javascript&style=for-the-badge">
  <!-- バックエンドのフレームワーク一覧 -->
  <img src="https://img.shields.io/badge/-Flask-000000.svg?logo=flask&style=for-the-badge">
  <!-- バックエンドの言語一覧 -->
  <img src="https://img.shields.io/badge/-Python-3776AB.svg?logo=python&style=for-the-badge">
  <img src="https://img.shields.io/badge/-Cplusplus-00599C.svg?logo=cplusplus&style=for-the-badge">
  <img src="https://img.shields.io/badge/-Powershell-5391FE.svg?logo=powershell&style=for-the-badge">
  <!-- インフラ一覧 -->
  <img src="https://img.shields.io/badge/-Docker-1488C6.svg?logo=docker&style=for-the-badge">
  <img src="https://img.shields.io/badge/-Ubuntu-E95420.svg?logo=ubuntu&style=for-the-badge">
</p>

## 目次

1. [プロジェクトについて](#プロジェクトについて)
2. [環境](#環境)
3. [ディレクトリ構成](#ディレクトリ構成)
4. [開発環境構築](#開発環境構築)

## ジョブラウザ

ジョブリッジ専用ブラウザ

## プロジェクトについて

ジョブリッジ内での利用を想定した専用ブラウザの開発

## 環境

<!-- 言語、フレームワーク、ミドルウェア、インフラの一覧とバージョンを記載 -->

| 言語・フレームワーク  　| バージョン |
| --------------------- | ---------- |
| Python                | 3.12.8     |
| Flask                 | 3.1.0      |
| WSL                   | 2.3.26.0   |
| Ubuntu                | 22.04.0    |
| Node.js               | 22.12.0    |
| npm                   | 10.9.0     |
| Gulp                  | 5.0.0      |
| Sass                  | 1.83.0     |

## 開発環境構築

<!-- コンテナの作成方法、パッケージのインストール方法など、開発環境構築に必要な情報を記載 -->

### コンテナの作成と起動

1. Ubuntu24.04 LTSをインストール
```
wsl --install -d Ubuntu-24.04
```

2. DifyのGitHubリポジトリをクローン
```
git clone https://github.com/langgenius/dify.git
```

3. Docker Engineをインストール
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

4. Docker Packageをインストール
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

5. DifyをDockerで起動
```
cd dify/docker
copy .env.example .env
docker compose up -d
```

6. ブラウザで `http://localhost/install` にアクセスし、セットアップ

7. main.pyを実行
```
python main.py
```

### 動作確認

ブラウザを起動できたら成功

### コンテナの停止

以下のコマンドでコンテナを停止することができます
```
docker compose down
```

<p align="right">(<a href="#top">トップへ</a>)</p>
