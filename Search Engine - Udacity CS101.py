def compute_ranks(graph):
    d = 0.8 # damping factor, recommended by udacity
    numloops = 10

    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1-d) / npages #probability of randomly clicking page
            for nodes in graph:
                if page in graph[nodes]:
                    newrank = newrank + d * (ranks[nodes] / len(graph[nodes]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

#a bit confused on the numloops on this one and how it allows the ranks to converge into a more accurate ranking result


def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    graph = {} #would be <url>, [list of outlinks]
    index = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)

            graph[page] = outlinks

            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph



def get_page(url):
    if url in cache:
        return cache[url]
    else:
        return None


def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote


def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

#breaking down page content into words and adding the site as a value for each of those keywords
def add_page_to_index(index, url, content): 
    words = content.split()
    for word in words:
        add_to_index(index, word, url)


def add_to_index(index, keyword, url): #assigning urls as keyword values
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = (url)
        
def lookup(index, keyword): #returning list of urls related to keyword
    if keyword in index:
        return index[keyword]
    else:
        return None

