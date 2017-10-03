from PIL import Image, ImageDraw
import os

def getPxlInfo():
    #print("Enter path to the picture:")
    #path = input()
    path = "C:/Users/Jonas Martin/Pictures/Saved Pictures/sudoku2.png"
    im = Image.open(path)
    greyscaleIm = im.convert("L")
    pixels = greyscaleIm.load()
    width, height = greyscaleIm.size

    newImage = Image.new("L",(width,height),255)
    draw = ImageDraw.Draw(newImage)


    allPixels = []
    for x in range(width):
        for y in range(height):
            cpixel = pixels[x, y]
            allPixels.append(cpixel)

    threshold = sum(allPixels)/len(allPixels)
    pxldict = dict()
    allPixelsBW = []

    for y in range(height):
        for x in range(width):
            cpixel = pixels[x, y]
            if cpixel > threshold:
                pxldict[x,y] = 255
                allPixelsBW.append(255)
                draw.point((x,y),255)

            else:
                pxldict[x,y] = 0
                allPixelsBW.append(0)
                draw.point((x,y), 0)

    #greyscale_im.show()

    newImage.show()
    '''
    print(len(pxldict))
    print (width, height)
    print (threshold)
    print (pxldict)
    '''

    return (pxldict, width, height, allPixelsBW, newImage)
