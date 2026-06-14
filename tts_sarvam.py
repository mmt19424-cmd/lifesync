import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

LANGUAGES = {
    'Telugu': ('te-IN', 'అత్యవసరం! O negative రక్తం Apollo Hospital లో అవసరం. దయచేసి వెంటనే స్పందించండి.'),
    'Hindi': ('hi-IN', 'आपातकाल! Apollo Hospital में O negative रक्त की आवश्यकता है। कृपया तुरंत प्रतिक्रिया दें।'),
    'Tamil': ('ta-IN', 'அவசரம்! Apollo Hospital இல் O negative இரத்தம் தேவை. உடனே பதிலளிக்கவும்.'),
    'Kannada': ('kn-IN', 'ತುರ್ತು! Apollo Hospital ನಲ್ಲಿ O negative ರಕ್ತ ಬೇಕು. ದಯವಿಟ್ಟು ತಕ್ಷಣ ಪ್ರತಿಕ್ರಿಯಿಸಿ.'),
    'Bengali': ('bn-IN', 'জরুরি! Apollo Hospital এ O negative রক্ত দরকার। অনুগ্রহ করে এখনই সাড়া দিন।'),
    'Marathi': ('mr-IN', 'आणीबाणी! Apollo Hospital मध्ये O negative रक्त हवे आहे. कृपया लगेच प्रतिसाद द्या.'),
    'Malayalam': ('ml-IN', 'അടിയന്തരം! Apollo Hospital ൽ O negative രക്തം ആവശ്യമാണ്. ഉടനെ പ്രതികരിക്കുക.'),
    'Gujarati': ('gu-IN', 'કટોકટી! Apollo Hospital માં O negative રક્તની જરૂર છે. કૃપા કરી તરત જ પ્રતિસાદ આપો.'),
    'Punjabi': ('pa-IN', 'ਐਮਰਜੈਂਸੀ! Apollo Hospital ਵਿੱਚ O negative ਖੂਨ ਦੀ ਲੋੜ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਤੁਰੰਤ ਜਵਾਬ ਦਿਓ।'),
    'Odia': ('od-IN', 'ଜରୁରୀ! Apollo Hospital ରେ O negative ରକ୍ତ ଦରକାର। ଦୟାକରି ତୁରନ୍ତ ସାଡ଼ା ଦିଅନ୍ତୁ।'),
    'English': ('en-IN', 'Emergency! O negative blood needed at Apollo Hospital. Please respond immediately.')
}

def generate_all_audio():
    for lang_name, (lang_code, message) in LANGUAGES.items():
        print(f"Generating {lang_name}...")
        try:
            response = requests.post(
                'https://api.sarvam.ai/text-to-speech',
                headers={
                    'api-subscription-key': SARVAM_API_KEY,
                    'Content-Type': 'application/json'
                },
                json={
                    'inputs': [message],
                    'target_language_code': lang_code,
                    'speaker': 'vidya',
                    'model': 'bulbul:v2'
                }
            )
            data = response.json()
            audio = data.get('audios', [''])[0]
            if audio:
                filename = f"alert_{lang_name.lower()}.wav"
                with open(filename, 'wb') as f:
                    f.write(base64.b64decode(audio))
                print(f"✅ Saved {filename}!")
            else:
                print(f"❌ Failed {lang_name}:", data)
        except Exception as e:
            print(f"❌ Error {lang_name}:", e)

generate_all_audio()