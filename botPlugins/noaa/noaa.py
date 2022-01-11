from datetime import datetime
import requests
from PIL import Image
import io, os
import sys


# download images
def pull_image(url, tag):
    filename = tag + '.png'
    with open(filename, 'wb') as handle:
        response = requests.get(url, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    return filename


# merge images
def merge_images(image_list, tag):
    images = [Image.open(x) for x in image_list]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))
    #print(tag,total_width,max_height)
    #new_im = new_im.resize((900,500))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    filename = './images/'+tag+'noaa.png'
    new_im= new_im.resize((total_width,max_height))
    new_im.save(filename)
    return filename


def getCurrent():
    current_temp_url = 'https://graphical.weather.gov/images/conus/T4_conus.png'
    current_weather_url = 'https://graphical.weather.gov/images/conus/Wx1_conus.png'
    # download images and save the filenames to a list
    current = [pull_image(current_temp_url, './images/current_temperature_national'),
               pull_image(current_weather_url, './images/current_weather_national')]
    filename = merge_images(current, 'current')
    return filename

def getForecasts():
    precipitation_url = 'https://www.cpc.ncep.noaa.gov/products/predictions/814day/814prcp.new.gif'
    temperature_url = 'https://www.cpc.ncep.noaa.gov/products/predictions/814day/814temp.new.gif'
    # download images and save the filenames to a list
    forecasts = [pull_image(temperature_url, './images/forecasted_temperature_national'),
                 pull_image(precipitation_url, './images/forecasted_precipitation_national')]
    filename = merge_images(forecasts, '8-14_day_outlook')
    return filename

def main():
    # 8 - 14 day forecast links for NOAA
    precipitation_url = 'https://www.cpc.ncep.noaa.gov/products/predictions/814day/814prcp.new.gif'
    temperature_url = 'https://www.cpc.ncep.noaa.gov/products/predictions/814day/814temp.new.gif'
    current_temp_url = 'https://graphical.weather.gov/images/conus/T4_conus.png'
    current_weather_url = 'https://graphical.weather.gov/images/conus/Wx1_conus.png'

    # download images and save the filenames to a list
    forecasts = [pull_image(temperature_url, './noaaImages/forecasted_temperature_national'),
                 pull_image(precipitation_url, './noaaImages/forecasted_precipitation_national')]

    current = [pull_image(current_temp_url, './noaaImages/current_temperature_national'),
               pull_image(current_weather_url, './noaaImages/current_weather_national')]
    # this method iterates through the image list and merges all the images into one big image
    # get the 8-14 day forecasts
    merge_images(forecasts, '8-14_day_outlook')
    # get the current temperature and weather
    merge_images(current, 'current')

def get_image_as_data(filename, width=None, height=None):
    im = Image.open(filename)
    if isinstance(width, int) and isinstance(height, int):
        im = im.resize((width, height))
    imBA = io.BytesIO()
    im.save(imBA, format="PNG")
    return imBA.getvalue()

if __name__ == '__main__':
    parameters = sys.argv
    parameters.pop(0)
    noaa_type = parameters[0]

    print('type=FILE')
    if noaa_type.lower() == 'current':
        print(getCurrent())
    elif noaa_type.lower() == 'forecast':
        print(getForecasts())