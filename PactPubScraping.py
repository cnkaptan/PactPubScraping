import bs4
import requests

f = open('Deneme.txt', 'w')


def write_book_name(soup):
    book_name = soup.find('div', attrs={'class': 'book-top-block-info-title float-left'}).text.strip()
    str_book_name = book_name + "\n"
    print(str_book_name)
    f.write(str_book_name)


def write_headers_in_chapter(header_soup):
    for header in header_soup:
        f.write("   --->   " + header.text.strip() + "\n")


def write_chapters(table_of_contents):
    try:
        for section in table_of_contents:
            f.write("   " + section.find(attrs={'class': 'book-toc-chapter-title arrow'}).text.strip() + "\n")
            header_soup = section.findAll(attrs={'class': 'book-toc-section-text float-left'})
            write_headers_in_chapter(header_soup)
    except:
        return


def main():
    books_url_list = get_links_of_book()
    for url in books_url_list:
        write_single_book_from_url(url)
        f.write('\n\n')


def write_single_book_from_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/68.0.3440.106 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    write_book_name(soup)
    soup = soup.find(id='book-info-toc')
    table_of_contents = soup.findAll(attrs={'class': 'book-toc-chapter'})
    # write_chapters(table_of_contents)


def get_links_of_book():
    books_file = open('books_list.txt', 'r')
    books_url_list = []
    for url in books_file.readlines():
        books_url_list.append(url)
    books_file.close()
    return books_url_list


if __name__ == '__main__':
    main()
    f.close()
