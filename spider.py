import lxml
import requests
import lxml.html


def get_url_content(url, **kwargs):
    '''

    Get bytes content from url

    '''
    q = requests.get(url, **kwargs)
    return q.content


def get_item(html_content, indicator):
    '''
    Argument:
        @content  --  html content
        @indicator -- (name, cotent_type, indicator_type, indicator):
            name - the name of the content you want get
            content_type - the content type you want to  extract. for example: text or href
            indicator_type - the type of (xpath, cssselect, re)
            indicatorz - the value of indicator_type

    Return:
        tuple($name, $content you extract)
    '''
    bhtml = lxml.html.fromstring(html_content)
    name, target_type, indicator_type, indicator_value = indicator
    if target_type == "text":
        if indicator_type == "xpath":
            target = bhtml.xpath(indicator_value)
            if target:
                target = target[0]
                return (name, target.text_content())
            else:
                print("%s is invalid" % indicator_value)
        elif indicator_type == "cssselect":
            target = bhtml.cssselect(indicator_value)
            if target:
                target = target[0]
                return (name, target.text_content())
            else:
                print("%s is invalid" % indicator_value)
        else:
            print("%s is invalide" % indicator_type)
    elif target_type == "href":
        if indicator_type == "xpath":
            target = bhtml.xpath(indicator_value)
            if target:
                target = target[0]
                return (name, target.attrib['href'])
            else:
                print("%s is invalid" % indicator_value)
        elif indicator_type == "cssselect":
            target = bhtml.cssselect(indicator_value)
            if target:
                target = target[0]
                return (name, target.attrib['href'])
            else:
                print("%s is invalid" % indicator_value)

        else:
            print("%s is invalide" % indicator_type)
    else:
        print("%s is invalid" % target_type)
    return


def get_items(html_content, indicators):
    content = []
    for i in indicators:
        content.append(get_item(html_content, i))
    return content


def spider(url, location_indicator, *args, **kwargs):
    html_content = get_url_content(url)
    return get_items(html_content, location_indicator)
