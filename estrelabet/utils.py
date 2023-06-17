from http.cookies import SimpleCookie

cookie_string = 'NCC=PTB; __nxquid=LLVPDxcKyJcXbODDKGUoKfM7TcrRWA==0014; lang=ptb; _gcl_au=1.1.855789859.1686942139; _gid=GA1.2.1917156758.1686942139; vs_vid=NXkjbJA6bUjNB; vs_vfs=1; vs_sid=nXLkPe83PUmON; vs_lift_ai=95-100; _ga=GA1.1.1465873768.1686942139; _ga_E2ZYXEN6NV=GS1.2.1686972318.2.1.1686972377.0.0.0; vs_conv_ai=55-59; _ga_JNY80EMZ8E=GS1.1.1686972318.2.1.1686973380.60.0.0'

def cookie_parser():
    cookie = SimpleCookie()
    cookie.load(cookie_string)
    cookies = {}
    for key, morsel in cookie.items():
        cookies[key] = morsel.value
    return cookies