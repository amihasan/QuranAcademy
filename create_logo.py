from PIL import Image, ImageDraw, ImageFont
import os
import math

# Create a high-quality logo for Raindrops Academy
width, height = 800, 800
image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
draw = ImageDraw.Draw(image)

# Colors
teal = (30, 90, 125)  # #1e5a7d
green = (45, 134, 89)  # #2d8659
light_blue = (100, 180, 220)
white = (255, 255, 255)

# Draw circular background with gradient effect
center_x, center_y = width // 2, height // 2
circle_radius = 350

# Create gradient-like effect with multiple circles
for i in range(circle_radius, 0, -10):
    alpha = int(255 * (i / circle_radius))
    ratio = (circle_radius - i) / circle_radius
    r = int(teal[0] + (green[0] - teal[0]) * ratio)
    g = int(teal[1] + (green[1] - teal[1]) * ratio)
    b = int(teal[2] + (green[2] - teal[2]) * ratio)
    draw.ellipse(
        [center_x - i, center_y - i, center_x + i, center_y + i],
        fill=(r, g, b, alpha)
    )

# Draw water droplets
def draw_droplet(x, y, size, color, alpha=255):
    # Teardrop shape
    points = []
    # Bottom point of drop
    points.append((x, y + size))
    # Right curve
    for angle in range(180, 360, 10):
        rad = math.radians(angle)
        px = x + (size * 0.5) * math.cos(rad)
        py = y - (size * 0.3) + (size * 0.5) * math.sin(rad)
        points.append((px, py))
    # Left curve
    for angle in range(0, 180, 10):
        rad = math.radians(angle)
        px = x + (size * 0.5) * math.cos(rad)
        py = y - (size * 0.3) + (size * 0.5) * math.sin(rad)
        points.append((px, py))
    
    draw.polygon(points, fill=(*color, alpha))
    
    # Add highlight
    highlight_size = size * 0.2
    draw.ellipse(
        [x - highlight_size, y - size*0.2 - highlight_size, 
         x + highlight_size, y - size*0.2 + highlight_size],
        fill=(255, 255, 255, 200)
    )

# Main central droplet
draw_droplet(center_x, center_y - 50, 120, white, 255)

# Surrounding smaller droplets
droplet_positions = [
    (center_x - 120, center_y - 100, 60),
    (center_x + 120, center_y - 100, 60),
    (center_x - 150, center_y + 50, 50),
    (center_x + 150, center_y + 50, 50),
    (center_x, center_y + 120, 70),
]

for x, y, size in droplet_positions:
    draw_droplet(x, y, size, light_blue, 230)

# Add a crescent moon and star symbol
# Crescent moon
moon_center_x = center_x - 80
moon_center_y = center_y + 180
moon_radius = 40

# Outer circle for crescent
draw.ellipse(
    [moon_center_x - moon_radius, moon_center_y - moon_radius,
     moon_center_x + moon_radius, moon_center_y + moon_radius],
    fill=white
)
# Inner circle to create crescent
draw.ellipse(
    [moon_center_x - moon_radius + 12, moon_center_y - moon_radius + 8,
     moon_center_x + moon_radius + 12, moon_center_y + moon_radius + 8],
    fill=(0, 0, 0, 0)
)

# Star
star_center_x = center_x + 60
star_center_y = center_y + 160
star_size = 30

def draw_star(cx, cy, size, color):
    points = []
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        radius = size if i % 2 == 0 else size * 0.4
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    draw.polygon(points, fill=color)

draw_star(star_center_x, star_center_y, star_size, white)

# Save the logo
output_path = 'static/images/logo.png'
os.makedirs('static/images', exist_ok=True)
image.save(output_path, 'PNG')
print(f"✓ Logo created successfully: {output_path}")

# Create a smaller version for favicon
favicon = image.resize((64, 64), Image.Resampling.LANCZOS)
favicon.save('static/images/favicon.png', 'PNG')
print("✓ Favicon created successfully: static/images/favicon.png")

# Create a horizontal banner version with text
banner_width, banner_height = 1200, 300
banner = Image.new('RGBA', (banner_width, banner_height), (255, 255, 255, 0))
banner_draw = ImageDraw.Draw(banner)

# Scale down and place logo on left
logo_small = image.resize((250, 250), Image.Resampling.LANCZOS)
banner.paste(logo_small, (25, 25), logo_small)

# Add text "Raindrops Academy" on the right
try:
    # Try to use a nice font if available
    font_large = ImageFont.truetype("arial.ttf", 80)
    font_small = ImageFont.truetype("arial.ttf", 40)
except:
    # Fallback to default font
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

text = "Raindrops Academy"
tagline = "Learn • Grow • Succeed"

banner_draw.text((320, 80), text, fill=teal, font=font_large)
banner_draw.text((320, 180), tagline, fill=green, font=font_small)

banner.save('static/images/logo_banner.png', 'PNG')
print("✓ Banner logo created successfully: static/images/logo_banner.png")
