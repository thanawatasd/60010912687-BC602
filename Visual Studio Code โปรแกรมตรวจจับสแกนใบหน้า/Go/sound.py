import time
import playsound
from gtts import gTTS
from datetime import datetime
now = datetime.now()
timestamp = datetime.timestamp(now)
#def playSound(name,name_speak):
tts=gTTS(text='วัดอุณหภูมิใหม่ค่ะ',lang='th')
mp3 = 'noscan' + '.mp3'
tts.save(mp3)
#playsound.playsound('yes.mp3' , True)
#playsound.playsound('no.mp3', True)
#os.remove(mp3)