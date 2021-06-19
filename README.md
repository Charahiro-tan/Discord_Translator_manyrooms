# Discord_Translator_manyrooms [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Charahiro-tan/Discord_Translator_manyrooms)
Discord translation bot that can be deployed on Heroku  
  
Herokuの無料枠にデプロイできる翻訳Botです。  
詳しい使い方はDiscordサーバーに書いてあります。  
  
The Bot will reply with a translation to the channel.  
このボットは翻訳結果をBotのアカウントでメッセージとして送信します。  
なので、見た目はBotのアカウントですが、見えてるチャンネル全て翻訳できます。  
サーバーの設定で適切な権限を設定してご使用ください。  

送信する際にEmbedを使うかどうか選択できます。  
![menyrooms](img/menyrooms.gif)  
## Environment variable(環境変数)
|Required(必須)||
|---|---|
|DISCORD_TOKEN|Discord bot Token|
|HOME_LANG|Any language will be translated into this language (e.g. ja)|
|HOME_TO_LANG|Translation language when posted in HOME_LANG language(e.g. en)|
  
|Options(オプション)||
|---|---|
|SEND_EMBED|If set to 1, Embed will be used when sending|
|IGNORE_ID|Author IDs to ignore (":" delimited, integers)|
|GAS_URL|Look at Discord Server|
  
## Other
- [__Discord Server__](https://discord.gg/bhpBKCJV8R)
- [Twitter](https://twitter.com/__Charahiro)
