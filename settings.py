# YOUR NOT-SECRET SETTINGS HERE
# DON'T PUT YOUR SECRET TOKEN HERE!!!!
import numpy as np
from PIL import Image, ImageDraw

# Open the input image as numpy array, convert to RGB
def to_circle(pic):
    img=Image.open(pic).convert("RGB")
    npImage=np.array(img)
    h,w=img.size

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size,0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0,0,h,w],0,360,fill=255)

    # Convert alpha Image to numpy array
    npAlpha=np.array(alpha)

    # Add alpha layer to RGB
    npImage=np.dstack((npImage,npAlpha))

    # Save with alpha
    Image.fromarray(npImage).save('result.png')