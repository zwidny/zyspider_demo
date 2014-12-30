import lxml
import requests
import lxml.html


def get_url_content(url, **kwargs):
    q = requests.get(url, **kwargs)
    return q.content


def get_specify_content(source, location):
    '''
    Arguments:
        source  : data source / unicode html
        location: datasource  / a couple of (method, path)
    Results:
        return specify content
    '''
    html_element = lxml.html.fromstring(source)
    sign, path = location
    if sign == 'xpath':
        result = html_element.xpath(path)
        if result:
            return result[0].text_content()
        else:
            return ''
    elif sign == 'cssselect':
        result = html_element.cssselect(path)
        if result:
            return result[0].text_content()
        else:
            return ''
    else:
        pass


def spider(url, location_indicator, *args, **kwargs):
    args = args
    kwargs = kwargs
    content = get_url_content(url)
    result = get_specify_content(content, location_indicator)
    return result
