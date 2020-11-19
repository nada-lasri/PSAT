from WebScrapperWithPreprocess import ArticleScrapperWithDownload

url = "https://edition.cnn.com/2020/10/14/media/fox-news-unmasking-obamagate/index.html"
try:
    scrapper = ArticleScrapperWithDownload(url)
    scrapper.preprocessAndExtraction()
    print("URL : " + scrapper.url)
    print("\n")
    print("=======")
    print("Title:" + scrapper.article.title)

    print("Texte")
    if scrapper.article_text=="":
        print("texte VIDE")
    print(scrapper.article_text)
    print("\n")
    print("=======")
    print("\n")
except Exception as e:
    print(e)