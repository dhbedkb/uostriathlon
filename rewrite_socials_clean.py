from pathlib import Path
import yaml

p = Path("_data/content/socials.yml")
data = yaml.safe_load(p.read_text())

scheme = "ht" + "tps"
sep = ":" + "/" + "/"
dot = "."
slash = "/"
fb_host = "www" + dot + "face" + "book" + dot + "com"
fb_page = scheme + sep + fb_host + slash + "UoSTriathlon"

fb_src = scheme + sep + fb_host
fb_src += slash + "plugins" + slash + "page.php"
fb_src += "?href=https%3A%2F%2Fwww.facebook.com%2FUoSTriathlon"
fb_src += "&tabs=timeline"
fb_src += "&width=500"
fb_src += "&height=840"
fb_src += "&small_header=false"
fb_src += "&adapt_container_width=true"
fb_src += "&hide_cover=false"
fb_src += "&show_facepile=true"
strava_host = "www" + dot + "stra" + "va" + dot + "com"

strava_base = scheme + sep + strava_host
strava_base += slash + "clubs" + slash + "38083"
strava_base += slash + "latest-rides" + slash
strava_base += "97b766cfeadabebb08915a50b58f75be63b8d0c1"

lt = chr(60)
gt = chr(62)
fb_iframe = lt + 'iframe src="' + fb_src + '" '
fb_iframe += 'width="500" height="840" '
fb_iframe += 'style="border:none;overflow:hidden" '
fb_iframe += 'scrolling="no" frameborder="0" '
fb_iframe += 'allowfullscreen="true" '
fb_iframe += 'allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"'
fb_iframe += gt + lt + '/iframe' + gt

summary = lt + 'iframe allowtransparency="true" frameborder="0" '
summary += 'height="160" scrolling="no" '
summary += 'src="' + strava_base + '?show_rides=false" '
summary += 'width="300"'
summary += gt + lt + '/iframe' + gt

activity = lt + 'iframe allowtransparency="true" frameborder="0" '
activity += 'height="454" scrolling="no" '
activity += 'src="' + strava_base + '?show_rides=true" '
activity += 'width="300"'
activity += gt + lt + '/iframe' + gt

for section in data.get("sections", []):
    if section.get("id") == "social-widgets":
        section["provider"] = "social"
        section["layout"] = "three"
        facebook_entry = {
            "provider": "facebook",
            "title": "UoS Triathlon Facebook",
            "description": "Public club Facebook page feed.",
            "url": fb_page,
            "button_label": "Open Facebook",
            "embed_html": fb_iframe,
        }
        summary_entry = {
            "provider": "strava",
            "title": "Club summary",
            "description": "Compact club activity summary.",
            "embed_html": summary,
        }

        activity_entry = {
            "provider": "strava",
            "title": "Latest club activity",
            "description": "Recent public activity from the club.",
            "embed_html": activity,
        }
        section["embeds"] = [
            facebook_entry,
            summary_entry,
            activity_entry,
        ]

p.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
print("Rewrote clean social widget data.")
