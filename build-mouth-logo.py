from PIL import Image

src = Image.open('assets/og-mouth-logo-source.png').convert('RGBA')
ratio = min(480/src.width, 480/src.height)
logo = src.resize((int(src.width*ratio), int(src.height*ratio)), Image.LANCZOS)
canvas = Image.new('RGB', (1200, 630), color=(0, 0, 0))
x = (1200 - logo.width)//2
y = (630 - logo.height)//2
canvas.paste(logo.convert('RGB'), (x, y))
canvas.save('assets/og-mouth-logo.jpg', 'JPEG', quality=95)
print('saved og-mouth-logo.jpg', canvas.size, 'logo', logo.size, 'offset', x, y)
