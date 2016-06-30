from collections import defaultdict

import scrapper


BASE_URL = "http://www.ceneo.pl"


class ProductEntry(scrapper.CrawlerItem):
    name = scrapper.CrawlerField(
        "div.product-content > h1",
        lambda value, _, __: value.strip() if value else None,
    )


class OfferEntry(scrapper.CrawlerItem):
    shop_name = scrapper.CrawlerField(
        "td.cell-store-logo > a > img",
        lambda value, _, __: value["alt"] if value else None,
        True,
    )
    price = scrapper.CrawlerField(
        "td.cell-price > a .price",
        lambda value, _, __: float(str(value.text.strip()).replace(",", "."))
        if value else 0.0,
        True,
    )
    url = scrapper.CrawlerField(
        "div.product-name > a",
        lambda value, _, __: value["href"],
        True,
    )


class OffersEntries(scrapper.CrawlerMultiItem):
    item_class = OfferEntry
    content_selector = "tbody > tr.product-offer"


def get_product_page(url):
    entries = OffersEntries(url)
    product = ProductEntry(url)

    return "%s" % product.name, entries


def get_sumed_offers(urls):
    sums = defaultdict(lambda: {"products": [], "price": 0})
    for url in urls:
        name, offers = get_product_page(url)
        for offer in offers:
            sums[offer.shop_name]["products"].append({
                "name": name,
                "price": offer.price,
                "url": BASE_URL + offer.url,
            })
            sums[offer.shop_name]["price"] += offer.price

    sums = [
        {
            "shop": shop,
            "url": "http://%s" % shop,
            "products": products["products"],
            "price": products["price"]
        }
        for shop, products in sums.items()
    ]

    sums.sort(key=lambda r: r["price"])
    sums.sort(key=lambda r: len(r["products"]), reverse=True)

    return sums


if __name__ == "__main__":
    import sys
    for row in get_sumed_offers(sys.argv[1:]):
        print "%20s - %.2f (%d)" % (
            row["shop"], row["price"], len(row["products"]),
        )
