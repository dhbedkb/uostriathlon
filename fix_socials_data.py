from pathlib import Path
import yaml

p = Path("_data/content/socials.yml")
data = yaml.safe_load(p.read_text())

scheme = "https"
sep = "://"
dot = "."
slash = "/"

fb_host = "www" + dot + "facebook" + dot + "com"
strava_host = "www" + dot + "strava" + dot + "com"

fb_page = scheme + sep + fb_host + slash + "UoSTriathlon"
fb_src = scheme + sep + fb_host + slash + "plugins" + slash + "page.php"
fb_src += "?href=https%3A%2F%2Fwww.facebook.com%2FUoSTriathlon"
fb_src += "&tabs=timeline"
fb_src += "&width=500"
fb_src += "&height=840"
fb_src += "&small_header=false"
fb_src += "&adapt_container_width=true"
fb_src += "&hide_cover=false"
fb_src += "&show_facepile=true"
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

strava_summary = lt + 'iframe allowtransparency="true" frameborder="0" '
strava_summary += 'height="160" scrolling="no" '
strava_summary += 'src="' + strava_base + '?show_rides=false" '
strava_summary += 'width="300"' + gt + lt + '/iframe' + gt

strava_activity = lt + 'iframe allowtransparency="true" frameborder="0" '
strava_activity += 'height="454" scrolling="no" '
strava_activity += 'src="' + strava_base + '?show_rides=true" '
strava_activity += 'width="300"' + gt + lt + '/iframe' + gt
for section in data.get("sections", []):
    if section.get("id") == "social-widgets":
        section["provider"] = "social"
        section["layout"] = "three"
        section["embeds"] = [
            {
                "provider": "facebook",
                "title": "UoS Triathlon Facebook",
                "description": "Public club Facebook page feed.",
                "url": fb_page,
                "button_label": "Open Facebook",
                "embed_html": fb_iframe,
            },
            {
                "provider": "strava",
                "title": "Club summary",
                "description": "Compact club activity summary.",
                "embed_html": strava_summary,
            },
            {
                "provider": "strava",
                "title": "Latest club activity",
                "description": "Recent public activity from the club.",
                "embed_html": strava_activity,
            },
        ]

p.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
print("Rewrote clean social widget data.")

lt = chr(60)
gt = chr(62)

fb_iframe = lt + 'iframe src="' + fb_src + '" '
fb_iframe += 'width="500" height="840" '
fb_iframe += 'style="border:none;overflow:hidden" '
fb_iframe += 'scrolling="no" frameborder="0" '
fb_iframe += 'allowfullscreen="true" '
fb_iframe += 'allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"'
fb_iframe += gt + lt + '/iframe' + gt

strava_summary = lt + 'iframe allowtransparency="true" frameborder="0" '
strava_summary += 'height="160" scrolling="no" '
strava_summary += 'src="' + strava_base + '?show_rides=false" '
strava_summary += 'width="300"'
strava_summary += gt + lt + '/iframe' + gt

strava_activity = lt + 'iframe allowtransparency="true" frameborder="0" '
strava_activity += 'height="454" scrolling="no" '
strava_activity += 'src="' + strava_base + '?show_rides=true" '
strava_activity += 'width="300"'
strava_activity += gt + lt + '/iframe' + gt

for section in data.get("sections", []):
    if section.get("id") == "social-widgets":
        section["provider"] = "social"
        section["layout"] = "three"
        section["embeds"] = [
            {
                "provider": "facebook",
                "title": "UoS Triathlon Facebook",
                "description": "Public club Facebook page feed.",
                "url": fb_page,
                "button_label": "Open Facebook",
                "embed_html": fb_iframe,
            },
            {
                "provider": "strava",
                "title": "Club summary",
                "description": "Compact club activity summary.",
                "embed_html": strava_summary,
            },
            {
                "provider": "strava",
                "title": "Latest club activity",
                "description": "Recent public activity from the club.",
                "embed_html": strava_activity,
            },
        ]

p.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
print("Rewrote clean social widget data.")
