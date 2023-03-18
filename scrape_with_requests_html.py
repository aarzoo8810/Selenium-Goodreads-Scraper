from requests_html import HTMLSession

session = HTMLSession()

book_url_list = []
eng_book_url = []
for num in range(1, 2):
    url = f"https://www.goodreads.com/shelf/show/light-novel?page={num}"
    r = session.get(url)
    book_url = r.html.find('a.bookTitle')

    for link in book_url:
        link = list(link.absolute_links)[0]
        book_url_list.append(link)
        # print(link)

for url in book_url_list:
    r = session.get(url)
    language = r.html.find('.DescList > div:nth-child(4) > dd:nth-child(2) > div:nth-child(1) > div:nth-child(1)')
    print(language)
    

# print(book_url_list)
print(len(book_url_list))

# print(book_url_list)
# print(len(book_url_list))