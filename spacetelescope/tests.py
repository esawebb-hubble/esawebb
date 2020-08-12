from django.test import TestCase, Client
from django.urls import reverse

from djangoplicity.media.models import Video
from djangoplicity.products.models import Book
from djangoplicity.science.models import ScienceAnnouncement

from product.models import Product, Category
from satchmo_store.shop.models import Config


class TestViewAsAdminUser(TestCase):
    fixtures = ['test']

    def setUp(self):
        self.client = Client()
        self.client.login(username='test_admin', password='admin')
        self.book = Book.objects.first()

    def test_login(self):
        login_url = reverse('admin:login')
        index_url = reverse('admin:index')

        response = self.client.get(login_url, follow=True)

        self.assertGreater(len(response.redirect_chain), 0)

        last_url, status_code = response.redirect_chain[-1]

        self.assertEqual(last_url, index_url)
        self.assertEqual(status_code, 302)

    def test_news(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)


class TestViewsAsStandardUser(TestCase):
    fixtures = ['test']

    def setUp(self):
        self.client = Client()
        self.client.login(username='test_standard', password='admin')
        self.published_book = Book.objects.filter(published=True).first()
        self.not_published_book = Book.objects.filter(published=False).first()

    def test_book_published(self):
        url = reverse('books_detail', args=[str(self.published_book.id)])
        response = self.client.get(url)

        self.assertContains(response, self.published_book.title, status_code=200)

    def test_book_not_published(self):
        """
        This test provides coverage for:
        spacetelescope/templates/403.html
        """
        url = reverse('books_detail', args=[str(self.not_published_book.id)])
        response = self.client.get(url)

        self.assertContains(response, 'Access Denied', status_code=403)


class TestAnnouncements(TestCase):
    fixtures = ['test']

    def setUp(self):
        self.client = Client()
        self.science_announcement = ScienceAnnouncement.objects.first()

    def test_announcements(self):
        response = self.client.get('/announcements/')
        self.assertContains(response, '<h1>Announcements <a href="http://feeds.feedburner.com/hubble_announcements/" class="listviewrsslink"><span class="fa fa-rss"></span></a></h1>')
        self.assertContains(response, '<a href="/copyright/">Usage of ESA/Hubble Images and Videos</a>')

    def test_announcements_webupdates(self):
        response = self.client.get('/announcements/webupdates/')
        self.assertContains(response,
                            '<h1>Web Updates <a href="/announcements/webupdates/feed/" class="listviewrsslink"><span class="fa fa-rss"></span></a></h1>')
        self.assertContains(response, '<a href="/copyright/">Usage of ESA/Hubble Images and Videos</a>')

    def test_forscientists(self):
        response = self.client.get('/forscientists/announcements/')
        self.assertContains(response,
                            '<h1>Announcements <a href="/forscientists/announcements/feed/" class="listviewrsslink"><span class="fa fa-rss"></span></a></h1>')
        self.assertContains(response, '<a href="/copyright/">Usage of ESA/Hubble Images and Videos</a>')

    def test_forscientists_detail(self):
        response = self.client.get('/forscientists/announcements/{}/'.format(self.science_announcement.pk))
        self.assertContains(response, self.science_announcement.title)


class TestMedia(TestCase):
    fixtures = ['test']

    def setUp(self):
        self.client = Client()
        self.video = Video.objects.get(pk='10000')

    def test_images(self):
        response = self.client.get('/images/')
        self.assertContains(response, 'View All')
        self.assertContains(response, 'Ranking')
        self.assertContains(response, 'Date')
        #self.assertContains(response, '<h1>Images <a href="/images/feed/" class="listviewrsslink"><span class="fa fa-rss"></span></a></h1>', html=True)

    def test_images_potw(self):
        response5 = self.client.get('/images/potw/')
        self.assertContains(response5,
                            '<h1>Picture of the Week <a href="http://feeds.feedburner.com/hubble_potw/" class="listviewrsslink"><span class="fa fa-rss"></span></a></h1>')

    def test_images_comparisons(self):
        response = self.client.get('/images/comparisons/')
        self.assertContains(response, '<h1>Image Comparisons</h1>')

    def test_videos_list(self):
        response = self.client.get('/videos/')
        self.assertContains(response, '<a href="/copyright/">Usage of ESA/Hubble Images and Videos</a>')

    def test_videos_detail(self):
        response = self.client.get('/videos/{}/'.format(self.video.id))
        self.assertContains(response, self.video.title)


class TestShop(TestCase):
    fixtures = ['test']

    def setUp(self):
        self.client = Client()

        self.shop = Config.objects.first()
        self.category = Category.objects.first()
        self.product = Product.objects.first()

    def test_shop_index(self):
        response = self.client.get('/shop/')
        self.assertContains(response, self.shop.store_name)

    def test_shop_freeorder(self):
        response = self.client.get('/shop/freeorder/')
        self.assertContains(response, 'Full Name')
        self.assertContains(response, 'Email Address')
        self.assertContains(response, 'Country of delivery')
        self.assertContains(response, 'Justification')

    def test_shop_category_detail(self):
        response = self.client.get('/shop/category/%s/' % self.category.slug)
        self.assertContains(response, self.category.name)

    def test_shop_product_process(self):
        # Add some products to cart, in order to render the cart_box template in the product detail
        response = self.client.post('/shop/add/', {
            'quantity': 3,
            'productname': self.product.slug
        })
        self.assertEqual(response.status_code, 302)

        # Visit product detail
        response = self.client.get('/shop/product/%s/' % self.product.slug)
        self.assertContains(response, self.product.name)

        # Visit cart page
        response = self.client.get('/shop/cart/')
        self.assertContains(response, self.product.name)

        # Visit checkout page
        response = self.client.get('/shop/checkout/')
        self.assertContains(response, 'Step 1 of 3')

        # TODO: review /shop/checkout/payment/ and /shop/checkout/payment/confirm/


class TestColumnTemplates(TestCase):
    fixtures = ['test']

    def setUp(self):
        self.client = Client()

    def test_onecolumn(self):
        response_online = self.client.get('/test-online/')
        response_offline = self.client.get('/test-not-online/')

        self.assertEqual(response_online.status_code, 200)
        self.assertEqual(response_offline.status_code, 404)

    def test_onecolumn_as_admin(self):
        self.client.login(username='test_admin', password='admin')
        response_offline = self.client.get('/test-not-online/')

        self.assertEqual(response_offline.status_code, 200)


class TestGeneralPurpose(TestCase):
    fixtures = ['test']

    def setUp(self):
        self.client = Client()

    def test_login_error(self):
        response = self.client.post('/login/', {'username': 'test_standard', 'password': 'badpassword'})
        self.assertContains(response, 'Your username and password didn\'t match. Please try again.')

    def test_login_success(self):
        response = self.client.post('/login/', {'username': 'test_standard', 'password': 'admin'}, follow=True)

        self.assertGreater(len(response.redirect_chain), 0)

        last_url, status_code = response.redirect_chain[-1]

        self.assertEqual(last_url, '/')
        self.assertEqual(status_code, 302)

    def test_logout(self):
        response = self.client.get('/logout/')
        self.assertContains(response, 'You have been successfully logged out.')

    def test_feed(self):
        response = self.client.get('/rss/feed.xml')
        self.assertEqual(response.status_code, 302)

    def test_password_reset(self):
        response_get = self.client.get('/password_reset/')
        self.assertContains(response_get,
                            '<p>Forgotten your password? Enter your e-mail address below, and we\'ll e-mail instructions for setting a new one.</p>')

        response_post = self.client.post("/password_reset/", data={"email": "test@email.com"})
        self.assertEqual(response_post.status_code, 302)
        self.assertEqual(response_post["Location"], "/password_reset/done/")
