# mantis/util.py

MAX_PER_PAGE = 100
DEFAULT_PER_PAGE = 20
DEFAULT_OFFSET = 1


# noinspection SpellCheckingInspection
def iferror(func, default):
    try:
        return func()
    except:
        return default


def paginate(query, limit=None, offset=None):
    try:
        limit = int(limit)
    except (ValueError, TypeError):
        limit = DEFAULT_PER_PAGE
    try:
        offset = int(offset)
    except (ValueError, TypeError):
        offset = DEFAULT_OFFSET
    paginate_obj = query.paginate(offset, limit, False, MAX_PER_PAGE)
    if paginate_obj.pages < paginate_obj.page:
        offset = DEFAULT_OFFSET
        paginate_obj = query.paginate(offset, limit, False, MAX_PER_PAGE)
    return paginate_obj
