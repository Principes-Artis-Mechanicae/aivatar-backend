import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin

# IP 유동적임
url = "https://41010f7c-3a13-429c.gradio.live"

# 이미지를 base64로 인코딩
with open('./source/yeo.jpg', 'rb') as img:
    img_base64 = base64.b64encode(img.read()).decode('utf-8')

# Server에 보내줄 Parameter
payload = {
    "prompt": """(analog film, photography:0.8), (Glow:0.8), masterpiece, (best quality:1.2), perfect anatomy, (4k), 
    (photorealistic:1.37), chromatic aberration, masterpiece portrait, ultra-detailed, detailed face, (ultra realistic body details:1.4),
    (big eyes:1.326), ((kpop idol, korean mixed:1.18), <lora:add_detail:1>, <lora:koreaface15:0.5>, (pureerosface_v1 :0.58), <lora:last:0.55>)""",
    "negative_prompt": """easynegative, ng_deepnegative_v1_75t, badhandv4, By bad artist -neg, bad_pictures, (unrealistic:2.2), paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2),
    lowres, normal quality, skin spots, acnes, skin blemishes, age spot, backlight, (ugly:1.331), (bad anatomy:1.21), (bad proportions:1.331), (disfigured:1.331),  (unclear eyes:1.331), glans""",
    "steps": 31,
    "denoising_strength": 0.2,
    "sampler_name": "DPM++ 2S a Karras",
    "seed": 902425906,
    "init_images": [img_base64]
}

# 이미지 보내기
response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)

# 이미지 받기
r = response.json()

# 이미지 저장 및 pnginfo에 parameter 추가
# 1개 이상의 이미지를 받을 수 있음, 하지만 현재는 1개만 받음
for i in r['images']:
    # base64로 인코딩된 이미지를 디코딩
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

    # pnginfo에 parameter 추가
    png_payload = {
        "image": "data:image/png;base64," + i
    }
    response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

    # pnginfo에 parameter 추가
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))
    # 이미지 저장
    image.save('output.png', pnginfo=pnginfo)