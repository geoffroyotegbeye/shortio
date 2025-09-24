from PIL import Image, ImageDraw, ImageFont
import random
import textwrap
from app.core.configs import WIDTH, HEIGHT, COLOR_PALETTES

def create_gradient_background(width, height, colors):
    img = Image.new('RGB', (width, height), colors[0])
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        ratio = y / height
        if ratio < 0.5:
            r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * (ratio * 2))
            g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * (ratio * 2))
            b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * (ratio * 2))
        else:
            ratio2 = (ratio - 0.5) * 2
            r = int(colors[1][0] + (colors[2][0] - colors[1][0]) * ratio2)
            g = int(colors[1][1] + (colors[2][1] - colors[1][1]) * ratio2)
            b = int(colors[1][2] + (colors[2][2] - colors[1][2]) * ratio2)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img

def create_text_image(text, img_path, palette_idx=0):
    palette = COLOR_PALETTES[palette_idx % len(COLOR_PALETTES)]
    img = create_gradient_background(WIDTH, HEIGHT, palette)
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("arial.ttf", 72)
    except:
        font_large = ImageFont.load_default()
    
    words = text.split()[:15]
    text_short = " ".join(words)
    lines = textwrap.wrap(text_short, width=20)
    total_height = len(lines) * 80
    start_y = (HEIGHT - total_height) // 2
    
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_large)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        y = start_y + i * 80
        draw.text((x+3, y+3), line, font=font_large, fill=(0, 0, 0, 100))
        draw.text((x, y), line, font=font_large, fill=(255, 255, 255))
    
    for _ in range(5):
        x = random.randint(50, WIDTH-50)
        y = random.randint(50, HEIGHT-50)
        size = random.randint(20, 60)
        color = random.choice(palette)
        draw.ellipse([x, y, x+size, y+size], fill=(*color, 100))
    
    img.save(img_path)
    return img_path

def create_subtitled_image(text, img_path, out_img_path):
    img = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 42)
    except:
        font = ImageFont.load_default()
    
    margin = 40
    lines = textwrap.wrap(text, width=35)
    line_height = 50
    total_text_height = len(lines) * line_height
    box_height = total_text_height + 60
    box_y = HEIGHT - box_height - margin
    
    overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([(20, box_y), (WIDTH-20, HEIGHT-margin)], 
                          fill=(0, 0, 0, 180))
    
    img = Image.alpha_composite(img.convert('RGBA'), overlay)
    draw = ImageDraw.Draw(img)
    
    y = box_y + 30
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        draw.text((x, y), line, font=font, fill=(255, 255, 255))
        y += line_height
    
    img.convert('RGB').save(out_img_path)
    return out_img_path