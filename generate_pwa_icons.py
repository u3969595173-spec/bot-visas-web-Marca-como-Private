from PIL import Image, ImageDraw, ImageFont
import os

sizes = [192, 512]
bg_color = "#0f172a"
text_color = "#f59e0b"

def ensure_dir():
    os.makedirs('frontend/public/assets', exist_ok=True)

def create_icon(size):
    img = Image.new('RGB', (size, size), color=bg_color)
    draw = ImageDraw.Draw(img)
    # Simple blocky letters for C T
    w = size
    h = size
    # Draw C
    c_w = w * 0.3
    c_h = h * 0.5
    c_x = w * 0.15
    c_y = h * 0.25
    draw.rectangle([c_x, c_y, c_x + c_w, c_y + c_h], outline=text_color, width=int(size*0.05))
    
    # Draw T
    t_x = w * 0.55
    t_y = h * 0.25
    draw.rectangle([t_x, t_y, t_x + w*0.3, t_y + h*0.1], fill=text_color)
    draw.rectangle([t_x + w*0.1, t_y, t_x + w*0.2, t_y + c_h], fill=text_color)
    
    img.save(f'frontend/public/icon-{size}x{size}.png')

if __name__ == "__main__":
    ensure_dir()
    for s in sizes:
        create_icon(s)
    print("Logos PWA generados con exito!")
