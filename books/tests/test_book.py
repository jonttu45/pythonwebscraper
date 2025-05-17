import unittest
from scrapy.http import HtmlResponse
from books.spiders.book import BookSpider
from scrapy.http import HtmlResponse, Request
from books.items import BooksItem

class BookSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = BookSpider()
        self.example_html = """
            <html>

            <body>
                <div class="container-fluid page">
                    <div class="page_inner">

                        <div class="row">

                            <div class="col-sm-8 col-md-9">

                                <div class="page-header action">
                                    <h1>All products</h1>
                                </div>

                                <div id="messages">

                                </div>

                                <div id="promotions">

                                </div>

                                <section>
                                    <div class="alert alert-warning" role="alert"><strong>Warning!</strong>
                                        This is a demo website
                                        for web scraping purposes. Prices and ratings here were randomly
                                        assigned and have no real
                                        meaning.</div>

                                    <div>
                                        <ol class="row">

                                            <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">

                                                <article class="product_pod">

                                                    <div class="image_container">

                                                        <a href="catalogue/a-light-in-the-attic_1000/index.html"><img
                                                                src="media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"
                                                                alt="A Light in the Attic" class="thumbnail"></a>

                                                    </div>

                                                    <p class="star-rating Three">
                                                        <i class="icon-star"></i>
                                                        <i class="icon-star"></i>
                                                        <i class="icon-star"></i>
                                                        <i class="icon-star"></i>
                                                        <i class="icon-star"></i>
                                                    </p>

                                                    <h3><a href="catalogue/a-light-in-the-attic_1000/index.html"
                                                            title="A Light in the Attic">A Light in the ...</a></h3>

                                                    <div class="product_price">

                                                        <p class="price_color">£51.77</p>

                                                        <p class="instock availability">
                                                            <i class="icon-ok"></i>

                                                            In stock

                                                        </p>

                                                        <form>
                                                            <button type="submit" class="btn btn-primary btn-block"
                                                                data-loading-text="Adding...">Add to basket</button>
                                                        </form>

                                                    </div>

                                                </article>

                                            </li>
                                            <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">

                                                <article class="product_pod">

                                                    <div class="image_container">

                                                        <a href="catalogue/tipping-the-velvet_999/index.html"><img
                                                                src="media/cache/26/0c/260c6ae16bce31c8f8c95daddd9f4a1c.jpg"
                                                                alt="Tipping the Velvet" class="thumbnail"></a>

                                                    </div>

                                                    <p class="star-rating One">
                                                        <i class="icon-star"></i>
                                                        <i class="icon-star"></i>
                                                        <i class="icon-star"></i>
                                                        <i class="icon-star"></i>
                                                        <i class="icon-star"></i>
                                                    </p>

                                                    <h3>
                                                        <a href="catalogue/tipping-the-velvet_999/index.html"
                                                            title="Tipping the Velvet">
                                                            Tipping the Velvet
                                                        </a>
                                                    </h3>

                                                    <div class="product_price">

                                                        <p class="price_color">£53.74</p>

                                                        <p class="instock availability">
                                                            <i class="icon-ok"></i>

                                                            In stock

                                                        </p>

                                                        <form>
                                                            <button type="submit" class="btn btn-primary btn-block"
                                                                data-loading-text="Adding...">
                                                                Add to basket
                                                            </button>
                                                        </form>

                                                    </div>

                                                </article>

                                            </li>
                                        </ol>

                                        <div>
                                            <ul class="pager">

                                                <li class="current">

                                                    Page 1 of 50

                                                </li>

                                                <li class="next">
                                                    <a href="catalogue/page-2.html">next</a>
                                                </li>

                                            </ul>
                                        </div>

                                    </div>
                                </section>

                            </div>

                        </div><!-- /row -->
                    </div><!-- /page_inner -->
                </div>
            </body>

            </html>
        """
        self.response = HtmlResponse(
            url="https://books.toscrape.com",
            body=self.example_html,
            encoding="utf-8"
    )

    def test_parse_scrapes_all_items(self):
        """Test if the spider scrapes books and pagination links."""
        # Collect the items produced by the generator in a list
        # so that it's possible to iterate over it more than once.
        results = list(self.spider.parse(self.response))

        # There should be two book items and one pagination request
        book_items = [item for item in results if isinstance(item, BooksItem)]
        pagination_requests = [
            item for item in results if isinstance(item, Request)
        ]

        self.assertEqual(len(book_items), 2)
        self.assertEqual(len(pagination_requests), 1)

    def test_parse_scrapes_correct_book_information(self):
        """Test if the spider scrapes the correct information for each book."""
        results_generator = self.spider.parse(self.response)

        # Book 1
        book_1 = next(results_generator)
        self.assertEqual(
            book_1["url"], "catalogue/a-light-in-the-attic_1000/index.html"
        )
        self.assertEqual(book_1["title"], "A Light in the Attic")
        self.assertEqual(book_1["price"], "£51.77")

        # Book 2
        book_2 = next(results_generator)
        self.assertEqual(
            book_2["url"], "catalogue/tipping-the-velvet_999/index.html"
        )
        self.assertEqual(book_2["title"], "Tipping the Velvet")
        self.assertEqual(book_2["price"], "£53.74")

    def test_parse_creates_pagination_request(self):
        """Test if the spider creates a pagination request correctly."""
        results = list(self.spider.parse(self.response))
        next_page_request = results[-1]
        self.assertIsInstance(next_page_request, Request)
        self.assertEqual(
            next_page_request.url,
            "https://books.toscrape.com/catalogue/page-2.html",
        )

if __name__ == "__main__":
    unittest.main()