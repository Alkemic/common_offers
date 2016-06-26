from collections import defaultdict

import scrapper


USER_SEARCH_URL = "http://allegro.pl/listing/user/" \
    "listing.php?us_id=%s&string=%s"


class OfferEntry(scrapper.CrawlerItem):
    name = scrapper.CrawlerField(
        "div > div.details > header > h2 > a > span",
        lambda value, _, __: value.strip(),
    )
    price = scrapper.CrawlerField(
        "div > div.purchase > div > span.buy-now",
        lambda value, _, __: [
            tt for tt in value.children if tt.strip and tt.strip()
        ].pop().strip(),
        True,
    )


class OffersEntries(scrapper.CrawlerMultiItem):
    item_class = OfferEntry
    content_selector = ".offers article"


def get_search_result(user_id, phrase):
    entries = OffersEntries(USER_SEARCH_URL % (user_id, phrase))

    return [(a.name, a.price) for a in entries]


def get_cheapest_offert(user_id, phrase):
    offers = get_search_result(user_id, phrase)
    return min(offers, key=lambda item: item[1])


def get_sumed_offers(user_ids, phrases):
    sums = defaultdict(lambda: {"products": [], "price": 0})
    for user_id in user_ids:
        for phrase in phrases:
            cheapest = get_cheapest_offert(user_id, phrase)

            sums[str(user_id)]["products"].append({
                "name": cheapest[0],
                "price": float(cheapest[1].replace(",", ".")),
            })
            sums[str(user_id)]["price"] += float(
                cheapest[1].replace(",", "."))

    sums = [
        {"shop": s, "products": v["products"], "price": v["price"]}
        for s, v in sums.items()
    ]

    sums.sort(key=lambda r: r["price"])
    sums.sort(key=lambda r: len(r["products"]), reverse=True)

    return sums
