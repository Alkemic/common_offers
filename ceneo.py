from collections import defaultdict

import scrapper


class ProductEntry(scrapper.CrawlerItem):
    name = scrapper.CrawlerField(
        'div.product-content > h1',
        lambda value, _, __: value.strip() if value else None,
    )


class OfferEntry(scrapper.CrawlerItem):
    shop_name = scrapper.CrawlerField(
        'td.cell-store-logo > a > img',
        lambda value, _, __: value['alt'] if value else None,
        True,
    )
    price = scrapper.CrawlerField(
        'td.cell-price > a > strong',
        lambda value, _, __: value.strip() if value else 0.0,
    )


class OffersEntries(scrapper.CrawlerMultiItem):
    item_class = OfferEntry
    content_selector = 'tbody > tr.product-offer'


def get_product_page(url):
    entries = OffersEntries(url)
    product = ProductEntry(url)

    return str(product.name), {
        str(item.shop_name): float(str(item.price).replace(",", "."))
        for item in entries
    }


def get_sumed_offers(urls):
    sums = defaultdict(lambda: {"products": [], "price": 0})
    for url in urls:
        name, offers = get_product_page(url)
        for shop, price in offers.items():
            sums[shop]["products"].append({"name": name, "price": price})
            sums[shop]["price"] += price

    sums = [
        {"shop": s, "products": v["products"], "price": v["price"]}
        for s, v in sums.items()
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
