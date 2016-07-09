import urllib.request
import xml.etree.ElementTree as ET


def search_book(ISBN):
    book_dict = {}
    try:
        book = urllib.request.urlopen(
            'https://www.goodreads.com/book/isbn/'
            + str(ISBN) + '?key=87I686KGOFf0WkB7uBSckg')
        data = book.read()
        book.close()
        root = ET.fromstring(data)
        book_dict['ISBN'] = ISBN
        book_dict['title'] = root[1][1].text
        book_dict['image'] = root[1][8].text
        book_dict['publisher'] = root[1][13].text
        book_dict['description'] = root[1][16].text
        book_dict['rating'] = root[1][18].text
        book_dict['author'] = root[1][26][0][1].text
    except:
        return {}
    return book_dict
