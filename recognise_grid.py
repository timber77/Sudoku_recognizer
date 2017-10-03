from pixelinformation import getPxlInfo
import pytesseract
def recogniseGrid():
    returned= getPxlInfo()
    pxldict, width, height, allPixelsBW, newImage = returned
    print (pxldict)

    #search the top left corner
    for i1 in range(len(allPixelsBW)-1):
        if allPixelsBW[i1] == 0:
            n1 = i1 // width
            x1 = i1 - (width * n1)
            y1 = n1 + 1
            k = i1
            mainLineWidth = 1
            #getting the linewidth of the outer grid
            while True:
                if allPixelsBW[k + 30*width] == 0:
                    k += 1
                    mainLineWidth += 1
                else:
                    break

            break
    #search the bottom right corner
    i2 = len(allPixelsBW) - 1
    for i2 in range(len(allPixelsBW) - 1, 0, -1):
        if allPixelsBW[i2] == 0:
            n2 = i2 / width
            x2 = i2 - (width * int(n2))
            y2 = int(n2 + 1)
            break

    sidelengthx = x2-x1
    sidelengthy = y2-y1
    sidelengthAvg = (sidelengthx + sidelengthy) // 2
    print (pytesseract.image_to_string(newImage, config ='digits'))

    print (x1, y1)
    print (x2, y2)
    print (width, height)
    print (sidelengthx, sidelengthy)
    print (sidelengthAvg)
    print (mainLineWidth)
