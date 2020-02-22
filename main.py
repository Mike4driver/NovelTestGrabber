from selenium import webdriver
from selenium.webdriver.chrome.options import  Options
import time
from multiprocessing import Pool
import os
import re
import sys

def getAllChapterLinks(link, browser):
    """
    Returns Dictionary containing information about the novel, Including the number of chapters and the chapter links
    {Name, Link, Chapters [{chapterNumber, chapterLink}]}
    """
    browser.get(link)
    try:
        chapterContainers = browser.find_elements_by_class_name('chapter-chs')
        
        chapterElems = []
        for chapterContainer in chapterContainers:
            for chapterElem in chapterContainer.find_elements_by_tag_name('a'):
                chapterElems.append(chapterElem)

        chapterLinks = [chapterElem.get_attribute("href") for chapterElem in chapterElems]
        
        novelInfo = {
            "Name": browser.find_element_by_class_name('block-title').text,
            "Link": link,
            "Chapters":[]
        }
        i = 0
        for chapterLink in chapterLinks:
            i+=1
            # print('{}/{} Chapters for this Novel Completed'.format(i, len(chapterLinks)))
            novelInfo["Chapters"].append({
                "chapterNumber": i,
                "chapterLink": chapterLink,
                # "chapterText": getChapterTexts(chapterLink, browser)[1]
            })
            # novelInfo["Chapters"]["chapterLink"] = chapterLink
            # novelInfo["Chapters"]["chapterText"] = getChapterTexts(chapterLink, browser)
    except:
        novelInfo = {}


    return novelInfo

def getChapterTexts(link, browser):
    browser.get(link)
    try:
        chapterLinkNumber = link.split('/')[-1]
        chapterText = browser.find_element_by_class_name("desc").text.replace("*", "").replace("￣", "").replace("_", "").replace("→", "").replace("Please help us improve Trinity Audio", "")
        return [chapterLinkNumber, chapterText]
    except:
        return False

def textGrabber(chapter, novel):
    os.environ["LANG"] = "en_US.UTF-8"


    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript':2})
    # chrome_options.add_extension('Driver/uBlock.crx')
    # chrome_options.add_extension('Driver/NoScript_v11.0.2.crx')
    newPath = r"Novels\{}".format(novel["Name"].replace("?", ''))
    if 'volume' in chapter['chapterLink']:
        chapterNumber = "-".join(chapter['chapterLink'].split('/')[-2:])
    else:
        chapterNumber = chapter['chapterLink'].split('/')[-1]
        if 'chapter' in chapterNumber:
            chapterNumber = chapterNumber.split('-')[-1]
    if stringIsNum(chapterNumber):
        if not os.path.isfile(newPath + f"\{chapterNumber.zfill(5)}.txt"):
            try:
                browser = webdriver.Chrome(executable_path=r'E:\NovelProject\Driver\chromedriver.exe', chrome_options=chrome_options)
                chapterLinkNumber, chapterText = getChapterTexts(chapter['chapterLink'], browser)
                browser.quit()
                if chapterText:
                    chapterText = re.sub("\[A-Za-z0-9]",'', chapterText.replace("Sponsored Content", ""))
                    with open(newPath + f"\{chapterNumber.zfill(5)}.txt", "w") as f:
                        f.write(chapterText)
                    print(f"Chapter {chapter['chapterNumber']}/{len(novel['Chapters'])} finished")
            except:
                pass
        else:
            print(f"Skipping Chapter {chapterNumber}/{len(novel['Chapters'])} Already Present")
    else:
        if not os.path.isfile(newPath + f"\{chapterNumber.zfill(5)}.txt"):
            try:
                chapterLinkNumber, chapterText = getChapterTexts(chapter['chapterLink'], browser)
                if chapterText:
                    with open(newPath + f"\{chapterNumber.zfill(5)}.txt", mode="w") as f:
                        f.write(chapterText)
                    print(f"Chapter {chapter['chapterNumber']}/{len(novel['Chapters'])} finished")
            except:
                pass
        else:
            print(f"Skipping Chapter {chapterNumber}/{len(novel['Chapters'])} Already Present")


def stringIsNum(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

def getNovelOnDemand(novelLink, browser):
    novel = getAllChapterLinks(novelLink, browser)
    newPath = r"Novels\{}".format(novel["Name"].replace("?", ''))
    if not os.path.exists(newPath):
        os.makedirs(newPath)       
    print(f"System has {os.cpu_count()} cores... creating {os.cpu_count()} threads") 
    # TODO: Have Pools write all the chapters that have yet to be downloaded into a queue then use the process pool on that queue
    # This will prevent the behavior we currently see where a the latest books in the update are all only being handled by the last process
    with Pool(processes=16) as p:
        # for chapter in novel["Chapters"]:
        p.starmap(textGrabber, [(chapter, novel) for chapter in novel["Chapters"]])



if __name__ == "__main__":
    newNovelLink = sys.argv[1]

    os.environ["LANG"] = "en_US.UTF-8"
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript':2})
    browser = webdriver.Chrome(executable_path=r'E:\NovelProject\Driver\chromedriver.exe', chrome_options=chrome_options)
    getNovelOnDemand(newNovelLink, browser)


    browser.close()