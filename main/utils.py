from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string


def proper_paginate(paginator, current_page, neighbors=2):
    if paginator.num_pages > 2*neighbors:
        start_index = max(1, current_page-neighbors)
        end_index = min(paginator.num_pages, current_page + neighbors)
        if end_index < start_index + 2*neighbors:
            end_index = start_index + 2*neighbors
        elif start_index > end_index - 2*neighbors:
            start_index = end_index - 2*neighbors
        if start_index < 1:
            end_index -= start_index
            start_index = 1
        elif end_index > paginator.num_pages:
            start_index -= (end_index-paginator.num_pages)
            end_index = paginator.num_pages
        page_list = [f for f in range(start_index, end_index+1)]
        return page_list[:(2*neighbors + 1)]
    return paginator.page_range



def getPercentile(obj, parts):
    n = len(obj)
    l = [int(n/parts)] * parts
    for i in range(n%parts):
        l[i] += 1
    stamps = []
    ptr = 0
    for i in l:
        stamps.append(ptr + i)
        ptr += i

    out = [0] * parts
    ptr = 0
    for i in range(len(obj)):
        if(i == stamps[ptr]):
            ptr += 1
        print(i, ptr)
        out[ptr] += obj[i][1]

    return out


def getData(request, output, paging, page, template,):
    paginator = Paginator(output, paging )
    pg = proper_paginate(paginator, int(page))
    
    try:
        rows = paginator.page(page)
    except PageNotAnInteger:
        rows = paginator.page(1)
    except EmptyPage:
        rows = paginator.page(paginator.num_pages)


    data = {
        'table': render_to_string(template, {'transaction': rows, 'page-page_range': pg}),
        'paginator': render_to_string('main/includes/Paginator.html', {'page': rows, 'page_range': pg, 'id': "Product-" + request.GET['queryType']})
    }
    return data

