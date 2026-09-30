from PIL import Image
from collections import Counter

im = Image.open(r"D:\coding\ugift-data-analysis\outputs\narrative-report\figures\chart_2909_mda_avail.png").convert("RGB")
colors = Counter()
for pixel in im.getdata():
    r, g, b = pixel
    if r > 245 and g > 245 and b > 245:
        continue
    if abs(r - g) < 8 and abs(g - b) < 8:
        continue
    colors[pixel] += 1
print(colors.most_common(8))
