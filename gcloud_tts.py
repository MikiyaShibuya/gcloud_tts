from pytz import timezone
from google.cloud import texttospeech
from google.oauth2 import service_account
import argparse
import yaml
import re
from tqdm import tqdm
import os

def convert_text_to_speech(text_to_speach, dest_fn):
    credentials = service_account.Credentials.from_service_account_file('credentials.json')
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    synthesis_input = texttospeech.types.SynthesisInput(
      text=text_to_speach)

    voice = texttospeech.types.VoiceSelectionParams(
      language_code='en-US',
      name="en-US-Wavenet-E",
      ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
      audio_encoding=texttospeech.enums.AudioEncoding.MP3,
      pitch = 0
    )

    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    with open(dest_fn, 'wb') as out:
      out.write(response.audio_content)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('fn', default="", type=str)
    parser.add_argument('-e', '--exec', default=False, action='store_true')
    parser.add_argument('-c', '--config', type=argparse.FileType("r"), default='-', required=True)
    parser.add_argument('-n', '--number', type=int, default=-1)

    args = parser.parse_args()

    # Load text file
    fn = args.fn

    text = ""
    with open(fn) as f:
        text = f.read()

    # Replace word (specified from / to by config)
    config = yaml.safe_load(args.config)
    replace_list = config['replace']

    for from_to in replace_list:
        regex_from = '(\W)' + from_to['from'] + '(\W)'
        regex_to = '\\1' + from_to['to'] + '\\2'
        text = re.sub(regex_from, regex_to, text)

        if text.startswith(from_to['from']):
            text = text.replace(from_to['from'], from_to['to'], 1)

    dest_dn = args.fn.replace('.txt', '')
    if not os.path.exists(dest_dn):
        os.makedirs(dest_dn)

    # Split section by #### of delimitor
    text_list = text.split('####')

    # Check text length
    over_length = False
    LENGTH_LIMIT = 5000 # Limit of the number of charactor
    for text_section in text_list:
        if len(text_section) >= LENGTH_LIMIT:
            over_length = True
            print('\n The length of the section exceeds the limit')
            print(' # charactors: {}'.format(len(text_section)))
            print('==========')
            print(text_section)
            print('==========')

    if over_length:
        print('Exitting due to the limit over')
        exit()

    if not args.exec:
        print(" -- checking the processing text --")

    for i, text_section in enumerate(tqdm(text_list)):
        if args.number >= 0 and args.number != i:
            continue
        dest_fn = os.path.join(dest_dn, '{:04}.mp3'.format(i))

        if not args.exec:
            print(' >> {} ============'.format(dest_fn))
            print(text_section)

        else:
            convert_text_to_speech(text_section, dest_fn)

