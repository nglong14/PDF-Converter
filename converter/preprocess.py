from PIL import ImageEnhance

def image_preprocess(image):
    image.convert('L')
    #Enhance contrast and sharpness
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)

    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.0)
    return image
