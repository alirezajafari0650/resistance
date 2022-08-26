import re


def upload_broadcast(instance, filename):
    filename = filename.replace(' ', '_')
    filename = filename.replace('\u200c', '_')
    foldername = instance.broadcast.title
    foldername = foldername.replace(' ', '_')
    foldername = foldername.replace('\u200c', '_')
    return 'file/%s/%s' % (
        foldername,
        filename,
    )


def reverse_number(text):
    list_text = []
    persian_numbers = {
        '۰': '0',
        '۱': '1',
        '۲': '2',
        '۳': '3',
        '۴': '4',
        '۵': '5',
        '۶': '6',
        '۷': '7',
        '۸': '8',
        '۹': '9',
    }
    english_numbers = {
        '0': '۰',
        '1': '۱',
        '2': '۲',
        '3': '۳',
        '4': '۴',
        '5': '۵',
        '6': '۶',
        '7': '۷',
        '8': '۸',
        '9': '۹',
    }
    for i in range(1, len(text) - 1):
        if text[i] in persian_numbers and len(text[i - 1]) > 2 and len(text[i + 1]) > 2:
            list_text.append(' '.join([text[i - 1], persian_numbers[text[i]]]))
            list_text.append(' '.join([persian_numbers[text[i]], text[i + 1]]))
        elif text[i] in english_numbers and len(text[i - 1]) > 2 and len(text[i + 1]) > 2:
            list_text.append(' '.join([text[i - 1], english_numbers[text[i]]]))
            list_text.append(' '.join([english_numbers[text[i]], text[i + 1]]))
    return list_text


def clean_search(search_text):
    search_text = re.split('\u200c|,|;| |،|\n', search_text)
    search_text.extend(reverse_number(search_text))
    search_text = list(set(search_text))
    cleaned_search_text = []
    for text in search_text:
        if len(text) > 2 and (not text.isdigit()):
            cleaned_search_text.append(text)
    return cleaned_search_text


def search_to_query(cleaned_search_text):
    # query = Q()
    # for text in cleaned_search_text:
    #
    # return query
    pass


def number_and_size(instance):
    try:
        page_number = int(instance.query_params.get('page', 1))
    except:
        page_number = 1
    try:
        page_size = int(instance.query_params.get('page_size', 50))
    except:
        page_size = 50
    if page_number < 1:
        page_number = 1
    if page_size < 1:
        page_size = 50
    if page_size > 200:
        page_size = 200

    return page_number, page_size


def get_response(instance, serialized_data, count):
    url = instance.build_absolute_uri()
    if 'page=' in url:
        url = url.split('page=')
        try:
            number = int(url[1][0])
        except:
            number = 1
    else:
        url = [url, '']
        number = 1
        if '?' not in url[0]:
            url[0] = '?' + url[0]

    next = url[0] + 'page=' + str(number + 1) + url[1][1:]
    if number > 1:
        previous = url[0] + 'page=' + str(number - 1) + url[1][1:]
    else:
        previous = None
    data = {
        'count': count,
        'next_page': next,
        'previous_page': previous,
        'results': serialized_data,
    }
    return data
