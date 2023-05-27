import os

def get_proxy_settings():
    """
    Returns a dictionary of proxy settings based on environment variables.

    Parameters:
    None

    Returns:
    dict: dictionary of proxy settings based on environment variables.
    str: `.cer` file path relative from project root directory.
    """
    # Initialize empty dictionary
    proxy = {}
    # HTTP
    auth_http_str = ""
    if os.getenv("proxy_http_username"): 
        auth_http_str = os.getenv("proxy_http_username", "") + ":" + os.getenv("proxy_http_password", "") + "@"
    proxy['http'] = None
    if os.getenv("proxy_http_domain"):
        proxy['http'] = os.getenv("proxy_http_protocol", "") + "://" + auth_http_str + os.getenv("proxy_http_domain", "") + ":" + os.getenv("proxy_http_port", "")
    # HTTPS
    auth_https_str = ""
    if os.getenv("proxy_https_username"): 
        auth_https_str = os.getenv("proxy_https_username", "") + ":" + os.getenv("proxy_https_password", "") + "@"
    proxy['https'] = None
    if os.getenv("proxy_https_domain"):
        proxy['https'] = os.getenv("proxy_https_protocol", "") + "://" + auth_https_str + os.getenv("proxy_https_domain", "") + ":" + os.getenv("proxy_https_port", "")
    return proxy, os.getenv("proxy_cert_path")
