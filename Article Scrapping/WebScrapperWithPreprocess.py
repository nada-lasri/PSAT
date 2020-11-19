__title__ = 'WebScrapperWithPreprocess'
__author__ = 'Ousmane TOUAT, Elöd Egyed-Zsigmond'

from newspaper import Article
import re
import requests
import unicodedata
import unidecode

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0','X-JAVASCRIPT-ENABLED':'true','Accept-Encoding':'br, gzip, deflate','Referer':'www.google.fr','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


class ArticleScrapperWithDownload():
    """This class store the Article object from the Newspaper Library"""

    def __init__(self, url):
        self.url = url
        # Create the Article class then download the article page from the url
        self.return_code = 1  # OK
        self.article = Article(url)
        response = requests.get(url, headers=headers)

        #print(response.status_code)
        if (response.status_code == 404):
            # Search for 404 "File not found" error
            self.return_code = 404
            raise Exception("Error 404 : with this url :" + str(url))
        elif (response.status_code == 403):
            # Search for 403 "Forbidden" error
            self.return_code = 403
            raise Exception("Error 403 : with this url :" + str(url))
        # trimming the beginning "http:// and https:// from response url and orig url
        respons_url = self.cleanurl(str(response.url))
        original_url = self.cleanurl(str(url))
        if (respons_url != original_url):
            # Search for redirection links which is an issue for our scrapper
            self.return_code = 'redirect'
            raise Exception("Redirection error : with this \n \
        url       : " + str(url) + "\n \
        trimmedurl: " + str(original_url) + "\n \
        res url   : " + str(response.url) + "\n \
        tr resurl : " + str(respons_url))


        # Emulate the download method by directly putting the response content extracted before
        self.article.download(response.content)
        self.article_title = ""
        self.article_date = ""
        self.article_text = ""

    def cleanurl(self, url_text_to_clean):
        result_url = url_text_to_clean
        if ("://" in url_text_to_clean):
            result_url = str(url_text_to_clean).partition("://")[2]
        if ("www." in url_text_to_clean):
            result_url = str(url_text_to_clean).partition("www.")[2]
        return result_url

    def preprocessAndExtraction(self):
        """This function does the article scrapping with preprocessing while downloading the article
        Require an Internet connection. It returns a string which contains the scrapped article , using the
        Newspaper3k library"""

        # Preprocess the html code by removing the "q" tag and all tags about any table
        htmlCode = self.article.html

        htmlCode = htmlCode.replace("<q>", '')
        htmlCode = htmlCode.replace("</q>", '')
        htmlCode = htmlCode.replace("</table>", '')
        htmlCode = htmlCode.replace("<tbody>", '')
        htmlCode = htmlCode.replace("</tbody>", '')
        htmlCode = htmlCode.replace("</tr>", '')
        htmlCode = htmlCode.replace("</td>", '')

        regextable = r"<table(.*?)>"
        regextr = r"<tr(.*?)>"
        regextd = r"<td(.*?)>"
        subst = "/n"
        htmlCode = re.sub(regextable, subst, htmlCode, 0, re.MULTILINE)
        htmlCode = re.sub(regextd, subst, htmlCode, 0, re.MULTILINE)
        htmlCode = re.sub(regextr, subst, htmlCode, 0, re.MULTILINE)

        self.article.html = htmlCode
        # Let Newspaper3k parses the article
        self.article.parse()



        self.article_title = self.article.title
        self.article_date = self.article.publish_date
        self.article_text = self.article.text
        #text = unidecode.unidecode(self.article_text)

        #à regarder encore
        text = unicodedata.normalize('NFKC', self.article_text).encode('utf-8', 'ignore')
        self.article_text = text.decode("utf-8")

        #text = unicodedata.normalize('NFKC', self.article_text).encode('latin1', 'ignore')
        #self.article_text = text.decode("latin1")


        return self.article_text
