import base64
import requests
# This is not 100% my code, so credits to:
# @JasonLovesDoggo


human = [
    "en_au_001",  # English AU - Female
    "en_au_002",  # English AU - Male
    "en_uk_001",  # English UK - Male 1
    "en_uk_003",  # English UK - Male 2
    "en_us_001",  # English US - Female (Int. 1)
    "en_us_002",  # English US - Female (Int. 2)
    "en_us_006",  # English US - Male 1
    "en_us_007",  # English US - Male 2
    "en_us_009",  # English US - Male 3
    "en_us_010",
]

class TikTok:
    def __init__(self):
        self.URI_BASE = "https://api16-normal-useast5.us.tiktokv.com/media/api/text/speech/invoke/?text_speaker="

    def run(self, text, filepath,voice):
        
        r = requests.post(f"{self.URI_BASE}{human[voice]}&req_text={text}&speaker_map_type=0")
        
        # print(r.text)
        vstr = [r.json()["data"]["v_str"]][0]
        b64d = base64.b64decode(vstr)

        with open(filepath, "wb") as out:
            out.write(b64d)