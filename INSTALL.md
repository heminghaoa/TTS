* requirement
  ```
  python <= 3.9
  ```

* Install
  ```
  $ sudo apt install tts
  $ git clone https://github.com/coqui-ai/TTS.git TTS
  $ copy YourTTSService.py to TTS/TTS/server/
  $ copy SteveJobs.wav to /opt/voices/.
  $ cd TTS
  $ python3 TTS/server/YourTTSService.py

* API
  * /api/tts
    * method
      * POST
    * request body
      ```
      {
        "text": 音声に生成しようテキスト,
        "language": "en", /* 現状は、enのみサポート */
        "speaker_wav": "path or uri to speaker sample voice, default: /opt/voices/SteveJobs.wav"
      }
     ```
    * response
      * error
      * success
        ```
        生成した音声データ
        ```
* memo
  * サンプル音声
    サンプル音声の保存先を /opt/voices
    変更したい場合、 YourTTSService.pyに default_speaker_wavの値を変更してください
  * サンプルコード
    test.htmlにご参照
    
