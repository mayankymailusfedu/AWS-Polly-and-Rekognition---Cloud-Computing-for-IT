import boto3

polly = boto3.client('polly')

voices = polly.describe_voices()['Voices']


# NOTE: this includes diacritics that you must replace manually

voices = [(voice['Name'], voice['LanguageName']) for voice in voices]
voices = sorted(voices, key=lambda x: x[1])

template_str = '<option value="{name}">{name} {lang}</option>'
for voice in voices:
    print(template_str.format(name=voice[0], lang=voice[1]))


