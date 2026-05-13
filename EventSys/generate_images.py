from PIL import Image, ImageDraw, ImageFont
import os
os.makedirs('imagenes de proyecto', exist_ok=True)
files=[
'mesa_redonda.png','mesa_cuadrada.png','silla_metal_negra.png','silla_tiffany.png','silla_plegable.png','silla_dorada.png',
'mantel_1.png','mantel_2.png','mantel_3.png','mantel_4.png','mantel_5.png','mantel_6.png','mantel_7.png','mantel_8.png','mantel_9.png','mantel_10.png','mantel_11.png','mantel_12.png',
'inflable_toy_story.png','inflable_chavo.png','carpa_6x6.png','carpa_10x10.png','arco_de_globos.png','centro_de_mesa.png','banderin.png','cubo_de_hielo.png','cajon_para_pastel.png','mesa_auxiliar.png','silla_funda.png','cubre_sillas.png'
]
for f in files:
    path = os.path.join('imagenes de proyecto', f)
    im = Image.new('RGB', (640, 360), (30, 30, 30))
    d = ImageDraw.Draw(im)
    text = f.replace('_', ' ').replace('.png', '').title()
    try:
        font = ImageFont.truetype('arial.ttf', 24)
    except Exception:
        font = ImageFont.load_default()
    w, h = d.textsize(text, font=font)
    d.text(((640 - w)/2, (360 - h)/2), text, fill='white', font=font)
    im.save(path)
print('images created', len(files))
