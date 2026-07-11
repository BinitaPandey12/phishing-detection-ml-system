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




from urllib.parse import urlparse
from datetime import datetime, timezone
import whois

def age_of_domain(url):
    try:
        hostname = urlparse(url).hostname

        domain = whois.whois(hostname)

        creation_date = domain.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date is None:
            print("Creation date not found")
            return 0

        # Make creation_date timezone-aware if needed
        if creation_date.tzinfo is None:
            creation_date = creation_date.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)

        age_days = (now - creation_date).days

        # print("Creation Date:", creation_date)
        # print("Current Date:", now)
        # print("Age Days:", age_days)

        return 1 if age_days >= 180 else 0

    except Exception as e:
        print("age_of_domain ERROR:", e)
        return 0


from urllib.parse import urlparse
from datetime import datetime, timezone
import whois

def domain_registration_length(url):
    try:
        hostname = urlparse(url).hostname

        domain = whois.whois(hostname)

        expiration_date = domain.expiration_date

        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        if expiration_date is None:
            print("Expiration date not found")
            return 0

        # Make timezone-aware if needed
        if expiration_date.tzinfo is None:
            expiration_date = expiration_date.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)

        remaining_days = (expiration_date - now).days

        print("Expiration Date:", expiration_date)
        print("Current Date:", now)
        print("Remaining Days:", remaining_days)

        return 1 if remaining_days > 365 else 0

    except Exception as e:
        print("domain_registration_length ERROR:", e)
        return 0


from urllib.parse import urlparse
from datetime import datetime
import ssl
import socket

def ssl_final_state(url):
    try:
        parsed = urlparse(url)

        if parsed.scheme.lower() != "https":
            return 0

        hostname = parsed.hostname

        context = ssl.create_default_context()

        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:

                cert = ssock.getpeercert()

                not_after = datetime.strptime(
                    cert["notAfter"],
                    "%b %d %H:%M:%S %Y %Z"
                )

                if not_after < datetime.utcnow():
                    return 0

                return 1

    except Exception as e:
        print("SSL ERROR:", e)
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
    
    
from urllib.parse import urljoin, urlparse

from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


def request_url(url):
    try:
        html = fetch_page(url)

        if html is None:
            return 0

        soup = BeautifulSoup(html, "html.parser")

        hostname = urlparse(url).hostname
        hostname = hostname.lower().replace("www.", "")

        resources = []

        resources.extend(soup.find_all("img"))
        resources.extend(soup.find_all("audio"))
        resources.extend(soup.find_all("embed"))
        resources.extend(soup.find_all("iframe"))
        resources.extend(soup.find_all("script"))
        resources.extend(soup.find_all("source"))
        resources.extend(soup.find_all("video"))

        total = 0
        external = 0

        for tag in resources:

            src = tag.get("src")

            if not src:
                continue

            src = src.strip()

            # Ignore inline/base64 resources
            if src.startswith("data:"):
                continue

            full_url = urljoin(url, src)

            parsed = urlparse(full_url)

            # Relative URL -> internal
            if parsed.hostname is None:
                total += 1
                continue

            total += 1

            resource_host = parsed.hostname.lower().replace("www.", "")

            if resource_host != hostname:
                external += 1

        if total == 0:
            return 1

        percentage = (external / total) * 100

        if percentage < 22:
            return 1
        elif percentage <= 61:
            return 0.5
        else:
            return 0

    except Exception:
        return 0

from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


def url_of_anchor(url):

    try:

        html = fetch_page(url)

        if html is None:
            return 0

        soup = BeautifulSoup(html, "html.parser")

        hostname = (
            urlparse(url)
            .hostname
            .lower()
            .replace("www.", "")
        )

        anchors = soup.find_all("a")

        if len(anchors) == 0:
            return 1

        suspicious = 0

        trusted_domains = [
            hostname,
            "gstatic.com",
            "googleusercontent.com",
            "googleapis.com",
            "cloudflare.com",
            "cloudflareinsights.com",
        ]

        for anchor in anchors:

            href = anchor.get("href")

            if not href:
                suspicious += 1
                continue

            href = href.strip()

            if href == "":
                suspicious += 1
                continue

            if href.startswith("#"):
                suspicious += 1
                continue

            if href.lower().startswith("javascript"):
                suspicious += 1
                continue

            full_url = urljoin(url, href)

            parsed = urlparse(full_url)

            # Relative links are internal
            if parsed.hostname is None:
                continue

            link_host = (
                parsed.hostname
                .lower()
                .replace("www.", "")
            )

            internal = any(
                link_host == domain
                or link_host.endswith("." + domain)
                for domain in trusted_domains
            )

            if not internal:
                suspicious += 1

        percentage = suspicious / len(anchors) * 100

        if percentage < 31:
            return 1
        elif percentage <= 67:
            return 0.5
        else:
            return 0

    except Exception:
        return 0

from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


def links_in_tags(url):

    try:

        html = fetch_page(url)

        if html is None:
            return 0

        soup = BeautifulSoup(html, "html.parser")

        hostname = (
            urlparse(url)
            .hostname
            .lower()
            .replace("www.", "")
        )

        tags = []

        tags.extend(soup.find_all("script"))
        tags.extend(soup.find_all("link"))
        tags.extend(soup.find_all("meta"))

        total = 0
        external = 0

        trusted_domains = [
            hostname,
            "googleapis.com",
            "gstatic.com",
            "cloudflare.com",
            "cloudflareinsights.com",
            "jsdelivr.net",
            "bootstrapcdn.com",
            "cdnjs.cloudflare.com",
            "unpkg.com",
        ]

        for tag in tags:

            link = tag.get("src") or tag.get("href") or tag.get("content")

            if not link:
                continue

            total += 1

            full_url = urljoin(url, link)

            parsed = urlparse(full_url)

            # Relative URL
            if parsed.hostname is None:
                continue

            link_host = (
                parsed.hostname
                .lower()
                .replace("www.", "")
            )

            internal = any(
                link_host == domain
                or link_host.endswith("." + domain)
                for domain in trusted_domains
            )

            if not internal:
                external += 1

        if total == 0:
            return 1

        percentage = (external / total) * 100

        if percentage < 17:
            return 1
        elif percentage <= 81:
            return 0.5
        else:
            return 0

    except Exception:
        return 0

from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


def sfh(url):

    try:

        html = fetch_page(url)

        if html is None:
            return 0

        soup = BeautifulSoup(html, "html.parser")

        forms = soup.find_all("form")

        # No forms present
        if len(forms) == 0:
            return 1

        hostname = (
            urlparse(url)
            .hostname
            .lower()
            .replace("www.", "")
        )

        suspicious = 0

        for form in forms:

            action = form.get("action")

            # Empty action attribute
            if action is None:
                suspicious += 1
                continue

            action = action.strip()

            # Blank or about:blank
            if action == "" or action.lower() == "about:blank":
                suspicious += 1
                continue

            # javascript:void(0)
            if action.lower().startswith("javascript"):
                suspicious += 1
                continue

            full_url = urljoin(url, action)

            parsed = urlparse(full_url)

            # Relative URL -> same website
            if parsed.hostname is None:
                continue

            form_host = (
                parsed.hostname
                .lower()
                .replace("www.", "")
            )

            if (
                form_host != hostname
                and not form_host.endswith("." + hostname)
            ):
                suspicious += 1

        percentage = suspicious / len(forms) * 100

        if percentage == 0:
            return 1
        elif percentage < 50:
            return 0.5
        else:
            return 0

    except Exception:
        return 0

from urllib.parse import urlparse
import whois


def abnormal_url(url):

    try:

        hostname = (
            urlparse(url)
            .hostname
            .lower()
            .replace("www.", "")
        )

        domain = whois.whois(hostname)

        registered = domain.domain_name

        if not registered:
            return 0

        if isinstance(registered, list):
            registered = registered[0]

        registered = (
            registered
            .lower()
            .replace("www.", "")
        )

        # Exact match
        if hostname == registered:
            return 1

        # Allow legitimate subdomains
        if hostname.endswith("." + registered):
            return 1

        return 0

    except Exception:
        return 0

def popup_window(url):

    try:

        html = fetch_page(url)

        if html is None:
            return 0

        html = html.lower()

        suspicious_patterns = [

            "window.open(",
            "alert(",
            "confirm(",
            "prompt("

        ]

        for pattern in suspicious_patterns:

            if pattern in html:
                return 0

        return 1

    except Exception:
        return 0

def web_traffic(url):
    return 1

def page_rank(url):
    return 1

def google_index(url):
    return 1

def links_pointing_to_page(url):
    return 1

def statistical_report(url):
    return 1
        
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


    
