
import aufgsettings
import matplotlib.image as mpimg


def loadImage(src, noPrint=0):

    pixelData = mpimg.imread(src)

    imgWidth = pixelData.shape[1]
    imgHeight = pixelData.shape[0]
    imgNrOfClrCmp = pixelData.shape[2]
    imgColorCompSize = pixelData.itemsize

    if (noPrint == 0):
        print("# = Image loaded =")
        print("# Width: " + str(imgWidth))
        print("# Height: " + str(imgHeight))
        print("# Number of color components per pixel: " + str(imgNrOfClrCmp))
        print("# Datatype of color components: " + str(pixelData.dtype)
              + " ( " + str(imgColorCompSize) + " Bytes )")
        print("#")

    imageProperties = {'imgWidth': imgWidth,
                       'imgHeight': imgHeight,
                       'imgNrOfClrCmp': imgNrOfClrCmp,
                       'imgColorCompSize': imgColorCompSize}

    return (pixelData, imageProperties)
