import csv
import time
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import bs4
options = Options()
#options.add_argument('--headless')
options.add_argument('--disable-gpu') 
options.add_argument('--log-level=3')


def main():
    def word_selector(sentences):
        selected = []
        for idx,each in enumerate(sentences):
            # if len(selected)==4:
            #     break
            if len(each[1].split(' '))>=3:
                # print(each[0])
                selected.append((each[0],each[2],each[1]))
            
        return selected
    
    def download_audio(word,sen_id,sent,write_list):

        if '0' in word:
            word = word.replace('0','')
        if len(write_list)<1:
            write_list.append(word)
        url = 'http://audio.tatoeba.org/sentences/spa/'+sen_id+'.mp3'
        try:
            response = requests.get(url)
        except:
            print('Cannot download audio')
            return False
        if '404 Not Found' in (bs4.BeautifulSoup(response.content,'html5lib')).get_text():
            print('Failed')
            return False
        with open('sentences/'+word+'.mp3','wb') as f:
            f.write(response.content)
        try:
            write_list.append(sent)
            write_list.append(sent.replace(ids[index][0].lower(),'___'))
            return True,write_list
        except:
            print('Error found in downloading audio')
            return False


    with open('/Users/Christopher/Documents/ACA/DownloadSentences/Deliver/inputwords.csv','r',encoding='UTF-8') as fp:
        word_list = list(csv.reader(fp))


    SITE_URL = 'https://tatoeba.org/spa/sentences/search?from=spa&to=eng&query=%3D{}'
    driver = webdriver.Chrome('/Users/Christopher/Documents/ACA/DownloadSentences/Deliver/chromedriver',options=options)

    for all in word_list:
        all[2] = all[2].replace('(/-a)','').strip()
        print('Word : ',all[1],all[2])
        try:
            driver.get(SITE_URL.format(all[1])+'&has_audio=yes')
        except:
            print('Error loading ' + SITE_URL.format(all[1])+'&has_audio=yes')
            continue
        time.sleep(5)
        sentences = []
        try:
            words = driver.find_elements_by_css_selector('.sentence-and-translations')
        except:
            print('words not found for ' + SITE_URL.format(all[1])+'&has_audio=yes')
            continue
        try:
            text = driver.find_elements_by_css_selector('.sentence-and-translations')
        except:
            print('text not found for ' + SITE_URL.format(all[1])+'&has_audio=yes')
            continue
        for index,a in enumerate(words):
            if all[2] in text[index].text:
                # print('[INFO]  WORD FOUND')
                try:
                    sent = a.find_element_by_css_selector('.sentence .text').text
                    id = a.find_element_by_tag_name('a').get_attribute('href').rsplit('/')[-1]
                    sentences.append((all[1],sent,id))
                except:
                    print('error finding sentence ...')
        stop = 5
        max_p=2
        while True:
            if not max_p<stop:
                break
            words = []
            try:
                driver.get(SITE_URL.format(all[1])+'&has_audio=yes&page='+str(max_p))
            except:
                print('Cannot load ' + SITE_URL.format(all[1])+'&has_audio=yes&page='+str(max_p))
            time.sleep(3)
            try:
                words = driver.find_elements_by_css_selector('.sentence-and-translations')
            except:
                print('words not found for ' + SITE_URL.format(all[1])+'&has_audio=yes&page='+str(max_p))
            try:
                text = driver.find_elements_by_css_selector('.sentence-and-translations')
            except:
                print('text not found for ' + SITE_URL.format(all[1])+'&has_audio=yes&page='+str(max_p))
            for index,a in enumerate(words):
                if all[2] in text[index].text:
                    try:
                        sent = a.find_element_by_css_selector('.sentence .text').text
                        id = a.find_element_by_tag_name('a').get_attribute('href').rsplit('/')[-1]
                        sentences.append((all[1],sent,id))
                    except:
                        print('error finding sentence ...')
            max_p+=1
            if len(sentences)<3 and stop<=15:
                stop+=1
            # print(str(len(sentences)),str(max_p),str(stop))
        # print(sentences)
        ids =word_selector(sentences)
        i=0
        index = 0
        write_list=[]
        while True:
            if len(ids)<2:
                if i==1:
                    break
            # if len(ids)-1 == index:
                # print('')
            if i==2:
                break
            try:
                status,write_list = download_audio(ids[index][0]+str(i),ids[index][1],ids[index][2],write_list)
                index+=1
            except:
                print('error on status and write list')
            if status == False:
                continue
            i+=1
        if len(write_list)==0:
            word_list.append(all[0])
        with open('words_list.csv','a',newline='',encoding='utf-8-sig') as file:
            writer=csv.writer(file)
            writer.writerow(write_list)
    try:
        driver.close()
    except:
        pass

if __name__ == '__main__' : main()
