import os
import os.path
import glob
import imageio
import requests
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys

class ImsGifMaker:
    def __init__(self, image_folder, output_folder):
        self.image_folder = image_folder
        self.output_folder = output_folder
        self.__IMS_URL = 'https://ims.gov.il/radar_satellite'
        self.__IMS_PREFIX = 'https://ims.gov.il/'

    def __getCookieFromResponse(self, resp_content, session):
        content = resp_content.decode('UTF-8','ignore')
        if ('document.cookie=' in content):
            document_cookie_split = content.split('document.cookie=\'')
            parsed_cookie = document_cookie_split[1].split(';')[0].split('=')
            print("Setting Cookie [" + parsed_cookie[0] + ": " + parsed_cookie[1] + "]")
            session.cookies.set(parsed_cookie[0],parsed_cookie[1], domain="ims.gov.il")


    def __get_json(self):
        print("Getting URL from: " + self.__IMS_URL)

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "br, gzip, deflate",
            "Accept-Language": "en-US;q=1",
            "Connection": "keep-alive",
            "Content-Type": "application/json; charset=utf-8",
            "Host": self.__IMS_PREFIX,
            "User-Agent": "Forest/342 (iPhone; iOS 12.1.2; Scale/3.00)"
        }

        cookie_jar = requests.cookies.RequestsCookieJar()
        s = requests.Session()
        resp = s.get(self.__IMS_URL, headers=headers, cookies=cookie_jar)

        resp_content = resp.content
        json_content = ''
        cookies = {}

        try:
            json_content = resp.json()
        except ValueError:
            print ("Failed parsing JSON, trying to fetch Cookie")
            headers = self.__getCookieFromResponse(resp_content, s)
        
        resp = s.get(self.__IMS_URL, headers=headers, cookies=cookie_jar)
        
        try:
            json_content = resp.json()
        except ValueError:
            print ("Failed parsing JSON. Content:")
            print (resp.content)
               
        return json_content

    @staticmethod
    def __get_images_from_json(arg):
        image_urls = []
        for radarImage in arg['IMSRadar']:
            image_urls.append(radarImage['file_name'])
        return image_urls

    def __does_image_exist_on_disk(self, arg):
        __filename = os.path.basename(arg)
        filepath = os.path.join(self.image_folder, __filename)
        return os.path.isfile(filepath)

    def __get_images_to_download(self, arg):
        images_to_download = []
        for downloadUrl in arg:
            if not self.__does_image_exist_on_disk(downloadUrl):
                images_to_download.append(downloadUrl)
        return images_to_download

    def __download_images(self, arg):
        for imageUrl in arg:
            file = self.__IMS_PREFIX + "/" + imageUrl
            __filename = os.path.basename(imageUrl)
            r = requests.get(file)
            with open(self.image_folder + "/" + __filename, 'wb') as f:
                f.write(r.content)

    def __cleanup_folder(self, arg):
        needed_files = set()
        for imageUrl in arg:
            needed_files.add(os.path.basename(imageUrl))

        file_list = os.listdir(self.image_folder)
        for fileName in file_list:
            if fileName not in needed_files:
                print("Removing: " + self.image_folder + '/' + fileName)
                os.remove(self.image_folder + '/' + fileName)

    def __create_gif(self):
        images = []
        filelist = glob.glob(os.path.join(self.image_folder, '*.gif'))
        for file_name in sorted(filelist):
            file_path = os.path.join(self.image_folder, file_name)
            images.append(imageio.imread(file_path))
        imageio.mimsave(self.output_folder + '/movie.gif', images, fps=2)

    def run(self):
        data = self.__get_json()
        if (not data):
            print("FAILED to get JSON")
            return
        image_urls = self.__get_images_from_json(data)
        self.__cleanup_folder(image_urls)
        image_urls_to_download = self.__get_images_to_download(image_urls)
        self.__download_images(image_urls_to_download)
        self.__create_gif()
