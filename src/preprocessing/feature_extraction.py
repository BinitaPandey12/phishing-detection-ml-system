import re
import ipaddress
import requests
import dns.resolver
import whois

from datetime import datetime
from urllib.parse import urlparse

from bs4 import BeautifulSoup


def having_ip_address(url):
    try:
        hostname = urlparse(url).hostname
        ipaddress.ip_address(hostname)
        return 0
    except Exception:
        return 1


def url_length(url):
    length = len(url)

    if length < 54:
        return 1
    elif length <= 75:
        return 0.5
    else:
        return 0


SHORTENERS = [
    "bit.ly", "goo.gl", "shorte.st", "go2l.ink", "x.co",
    "ow.ly", "t.co", "tinyurl.com", "tr.im", "is.gd",
    "cli.gs", "yfrog.com", "migre.me", "ff.im", "tiny.cc",
    "url4.eu", "twit.ac", "su.pr", "twurl.nl", "snipurl.com",
    "short.to", "budurl.com", "ping.fm", "post.ly", "just.as",
    "bkite.com", "snipr.com", "fic.kr", "loopt.us", "doiop.com",
    "short.ie", "kl.am", "wp.me", "rubyurl.com", "om.ly",
    "to.ly", "bit.do", "lnkd.in", "db.tt", "qr.ae",
    "adf.ly", "bitly.com", "cur.lv", "ity.im", "q.gs",
    "po.st", "bc.vc", "u.to", "j.mp", "buzurl.com"
]


def shortening_service(url):
    hostname = urlparse(url).hostname

    if hostname is None:
        return 1

    hostname = hostname.lower()

    for service in SHORTENERS:
        if hostname == service or hostname.endswith("." + service):
            return 0

    return 1


def having_at_symbol(url):
    if "@" in url:
        return 0

    return 1


def double_slash_redirecting(url):
    pos = url.rfind("//")

    if pos > 7:
        return 0

    return 1


def prefix_suffix(url):
    hostname = urlparse(url).hostname

    if hostname and "-" in hostname:
        return 0

    return 1


def having_sub_domain(url):
    hostname = urlparse(url).hostname

    if hostname is None:
        return 0

    dots = hostname.count(".")

    if dots == 1:
        return 1
    elif dots == 2:
        return 0.5
    else:
        return 0


def https_token(url):
    hostname = urlparse(url).hostname

    if hostname and "https" in hostname.replace(".", "").lower():
        return 0

    return 1


def port(url):
    parsed = urlparse(url)

    if parsed.port is None:
        return 1

    if parsed.port in [80, 443]:
        return 1

    return 0


def redirect_feature(url):
    try:
        response = requests.get(url, timeout=10)

        redirects = len(response.history)

        if redirects <= 1:
            return 1
        elif redirects <= 3:
            return 0.5
        else:
            return 0

    except Exception:
        return 0


def dns_record(url):
    try:
        hostname = urlparse(url).hostname

        dns.resolver.resolve(hostname, "A")

        return 1

    except Exception:
        return 0


def age_of_domain(url):
    try:
        hostname = urlparse(url).hostname

        domain = whois.whois(hostname)

        creation_date = domain.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        age_days = (datetime.now() - creation_date).days

        if age_days >= 180:
            return 1

        return 0

    except Exception:
        return 0


def domain_registration_length(url):
    try:
        hostname = urlparse(url).hostname

        domain = whois.whois(hostname)

        expiration_date = domain.expiration_date

        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        remaining_days = (expiration_date - datetime.now()).days

        if remaining_days > 365:
            return 1

        return 0

    except Exception:
        return 0


# TODO: Implement certificate validation
def ssl_final_state(url):
    if url.startswith("https://"):
        return 1

    return 0
   
    
def fetch_page(url):
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        return response.text

    except Exception:
        return None
    
    
def favicon(url):
    try:
        html = fetch_page(url)

        if html is None:
            return 0

        soup = BeautifulSoup(html, "html.parser")

        icon = soup.find("link", rel=lambda x: x and "icon" in x.lower())

        if not icon:
            return 1

        href = icon.get("href", "")

        hostname = urlparse(url).hostname

        if hostname in href or href.startswith("/"):
            return 1

        return 0

    except Exception:
        return 0
    
    
def submitting_to_email(url):
    try:
        html = fetch_page(url)

        if html is None:
            return 0

        html = html.lower()

        if "mailto:" in html or "mail(" in html:
            return 0

        return 1

    except Exception:
        return 0
    
    
def right_click(url):
    try:
        html = fetch_page(url)

        if html is None:
            return 0

        html = html.lower()

        suspicious_patterns = [
            "contextmenu",
            "event.button==2",
            "event.button == 2",
        ]

        for pattern in suspicious_patterns:
            if pattern in html:
                return 0

        return 1

    except Exception:
        return 0
    
    
 #TODO   
def iframe(url):
    try:
        html = fetch_page(url)

        if html is None:
            return 0

        soup = BeautifulSoup(html, "html.parser")

        frames = soup.find_all("iframe")

        if len(frames) > 0:
            return 0

        return 1

    except Exception:
        return 0
    
def on_mouseover(url):
    try:
        html = fetch_page(url)

        if html is None:
            return 0

        html = html.lower()

        if "onmouseover" in html and "window.status" in html:
            return 0

        return 1

    except Exception:
        return 0
    
    
def request_url(url):
    return 0.5

def url_of_anchor(url):
    return 0.5

def links_in_tags(url):
    return 0.5

def sfh(url):
    return 0.5

def abnormal_url(url):
    return 0.5

def popup_window(url):
    return 0.5

def web_traffic(url):
    return 0.5

def page_rank(url):
    return 0.5

def google_index(url):
    return 0.5

def links_pointing_to_page(url):
    return 0.5

def statistical_report(url):
    return 0.5
        
def extract_url_features(url):
    return {
        "having_IP_Address": having_ip_address(url),
        "URL_Length": url_length(url),
        "Shortining_Service": shortening_service(url),
        "having_At_Symbol": having_at_symbol(url),
        "double_slash_redirecting": double_slash_redirecting(url),
        "Prefix_Suffix": prefix_suffix(url),
        "having_Sub_Domain": having_sub_domain(url),
        "HTTPS_token": https_token(url),
        "port": port(url),
        "Redirect": redirect_feature(url),
        "DNSRecord": dns_record(url),
        "age_of_domain": age_of_domain(url),
        "Domain_registeration_length": domain_registration_length(url),
        "SSLfinal_State": ssl_final_state(url),
        "Favicon": favicon(url),
        "Submitting_to_email": submitting_to_email(url),
        "RightClick": right_click(url),
        "Iframe": iframe(url),
        "on_mouseover": on_mouseover(url),
        "Request_URL": request_url(url),
        "URL_of_Anchor": url_of_anchor(url),
        "Links_in_tags": links_in_tags(url),
        "SFH": sfh(url),
        "Abnormal_URL": abnormal_url(url),
        "popUpWidnow": popup_window(url),
        "web_traffic": web_traffic(url),
        "Page_Rank": page_rank(url),
        "Google_Index": google_index(url),
        "Links_pointing_to_page": links_pointing_to_page(url),
        "Statistical_report": statistical_report(url),
    }


url = "https://example.com//login"


    
