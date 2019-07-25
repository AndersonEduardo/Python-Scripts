#FONTE: https://realpython.com/python-speech-recognition/

import speech_recognition as sr

r = sr.Recognizer()

file_path = '/home/anderson/Python-Scripts/OSR_us_000_0010_8k.wav'

harvard = sr.AudioFile(file_path)

with harvard as source:
    audio = r.record(source)

r.recognize_google(audio)


# pegando apenas os primeiros 4 segundos
with harvard as source:
    audio = r.record(source, duration=4)

r.recognize_google(audio) #usando a API do google (mas sao 7 opcoes)

#com duas variaveis dentro do 'with' (segmentos consecutivos)
with harvard as source:
    audio1 = r.record(source, duration=4)
    audio2 = r.record(source, duration=4)

r.recognize_google(audio1)
r.recognize_google(audio2)

#definindo o inicio da transcricao
with harvard as source:
    audio = r.record(source, offset=4.4, duration=2.8)

r.recognize_google(audio)

#pegando todas as possiveis transcricoes
r.recognize_google(audio, show_all=True)


## microfone ##
#solucao para o problema que tive: https://www.linuxquestions.org/questions/programming-9/speech-recognition-microphone-needs-pyaudio-0-2-11-or-later-but-i-have-0-2-8-a-4175629060/

mic = sr.Microphone()

r = sr.Recognizer()

#portas para o microfone
sr.Microphone.list_microphone_names()

#capturando audio do microfone
with mic as source:
    r.adjust_for_ambient_noise(source) #ajustando para ruido do ambiente
    audio = r.listen(source)

#transcrevendo audio capturado
transcricao = r.recognize_google(audio,language='pt-BR')

print(transcricao)

