def post(url, data, then):
    """Create a function with the POST method
    @param: url: STR
    @param: data: DICT
    @param: then: VOID
    """
    return f'fetch({url}. {{method: "POST"}})'
