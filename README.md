# gcloud_tts
Generate speech via Google cloud TTS

## Install requirements
`pip install -r requirements.txt`

## Generate speech
For testing text to convert, execute the bellow command without "-e" option.  
`python gcloud_tts.py -c config.yaml {any text file} [-n target_section] [-e]`

The speech will be generated as multiple mp3 files.  
To sectioning sentences, insert `####` line between blocks.

## Example

<sample.txt>
```
Hello.
####
Goodbye.
```

`python gcloud_tts.py -c config.yaml sample.txt -e`

After executing this command with sample.txt, two mp3 voice files are generated into
`sample/0000.mp3` and `sample/0001.mp3` 
