from collections import defaultdict

import scrapper

BASE_URL = "http://allegro.pl"
USER_LISTING_URL = BASE_URL + "/listing/user/listing.php?us_id=%s"
USER_SEARCH_URL = USER_LISTING_URL + "&string=%s"


class OfferEntry(scrapper.CrawlerItem):
    name = scrapper.CrawlerField(
        "div > div.details > header > h2 > a > span",
        lambda value, _, __: value.strip(),
    )
    price = scrapper.CrawlerField(
        "div > div.purchase > div > span.buy-now",
        lambda value, _, __: float([
            tt for tt in value.children if tt.strip and tt.strip()
        ].pop().strip().replace(",", ".")),
        True,
    )
    url = scrapper.CrawlerField(
        "div > div.details > header > h2 > a",
        lambda value, _, __: value["href"],
        True,
    )


class OffersEntries(scrapper.CrawlerMultiItem):
    item_class = OfferEntry
    content_selector = ".offers article"


def get_search_result(user_id, phrase):
    entries = OffersEntries(USER_SEARCH_URL % (user_id, phrase))

    return entries


def get_cheapest_offert(user_id, phrase):
    offers = get_search_result(user_id, phrase)
    return min(offers, key=lambda item: item.price)


def get_sumed_offers(user_ids, phrases):
    sums = defaultdict(lambda: {"products": [], "price": 0})
    for user_id in user_ids:
        for phrase in phrases:
            offert = get_cheapest_offert(user_id, phrase)

            sums[str(user_id)]["products"].append({
                "name": offert.name,
                "price": offert.price,
                "url": (
                    "" if offert.url.startswith(BASE_URL) else BASE_URL
                ) + offert.url,
            })
            sums[str(user_id)]["price"] += offert.price

    sums = [
        {
            "shop": s,
            "url": USER_LISTING_URL % s,
            "products": v["products"],
            "price": v["price"],
        }
        for s, v in sums.items()
    ]

    sums.sort(key=lambda r: r["price"])
    sums.sort(key=lambda r: len(r["products"]), reverse=True)

    return sums
