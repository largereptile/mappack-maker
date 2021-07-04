from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from zipfile import ZipFile
import shutil

def no_part(maps):
    for file in maps:
        if file.endswith(".part"):
            return False
    return True

def get_downloads(beatmaps):
    list_of_files = filter(lambda x: os.path.isfile(os.path.join(os.getcwd(), x)), os.listdir(os.getcwd()))
    # Sort list of files based on last modification time in ascending order
    list_of_files = sorted(list_of_files, key=lambda x: os.path.getmtime(os.path.join(os.getcwd(), x)))
    return list_of_files[-(len(beatmaps)):]


firefox_opts = webdriver.FirefoxOptions()
firefox_opts.headless = True
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', os.getcwd())
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/x-osu-archive')
driver = webdriver.Firefox(options=firefox_opts, firefox_profile=profile)

def download_maps(username, password, with_videos, full_url, beatmaps):
    print("Logging in...")
    driver.get("https://osu.ppy.sh/home")
    signin = driver.find_element_by_class_name("js-user-login--menu").click()
    driver.find_element_by_name("username").send_keys(username)
    password_box = driver.find_element_by_name("password")
    password_box.send_keys(password)
    password_box.send_keys(Keys.ENTER)

    time.sleep(1)
    print(f"Login successful")
    for url in beatmaps:
        driver.get(url)
        buttons = driver.find_elements_by_class_name("js-beatmapset-download-link")
        if not with_videos and len(buttons) > 1:
            buttons[1].click()
        else:
            buttons[0].click()
        print(f"Starting download of {url}")


    maps_to_zip = get_downloads(beatmaps)
    while not no_part(maps_to_zip):
        time.sleep(1)
        maps_to_zip = get_downloads(beatmaps)

    print("All maps downloaded")

    zipfile = ZipFile("map_pack.zip", "w")
    for beatmap in maps_to_zip:
        print(f"Writing {beatmap} to zip")
        # shutil.move(os.path.join(downloads_path, beatmap), os.getcwd())
        zipfile.write(beatmap)
        os.remove(beatmap)
    zipfile.close()

    driver.quit()

    print("Complete")

if __name__ == "__main__":
# move these to tkinter window
    username = "username"
    password = "password"
    with_videos = False
    full_url = True
    beatmaps = ["https://osu.ppy.sh/beatmapsets/1350462#osu/2795985",
                "https://osu.ppy.sh/beatmapsets/1426332#osu/2999071",
                "https://osu.ppy.sh/beatmapsets/1452528#osu/2986545",
                "https://osu.ppy.sh/beatmapsets/920688#mania/1936645"]
    download_maps(username, password, with_videos, full_url, beatmaps)
