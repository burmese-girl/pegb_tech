from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.utils.safestring import mark_safe
import numpy as np
from decimal import *
gender_choices = (('MALE', 'MALE'), ('FEMALE', 'FEMALE'))
nationality_choices = (('SG', ('SINGAPOREAN')),
                       ('AF', ('AFGHAN')),
                       ('AL', ('ALBANIAN')),
                       ('DZ', ('ALGERIAN')),
                       ('US', ('AMERICAN')),
                       ('AD', ('ANDORRAN')),
                       ('AO', ('ANGOLAN')),
                       ('AG', ('ANTIGUANS OR BARBUDANS')),
                       ('AR', ('ARGENTINEAN')),
                       ('AM', ('ARMENIAN')),
                       ('AU', ('AUSTRALIAN')),
                       ('AT', ('AUSTRIAN')),
                       ('AZ', ('AZERBAIJANI')),
                       ('BS', ('BAHAMIAN')),
                       ('BH', ('BAHRAINI')),
                       ('BD', ('BANGLADESHI')),
                       ('BB', ('BARBADIAN')),
                       ('BW', ('BATSWANA')),
                       ('BY', ('BELARUSIAN')),
                       ('BE', ('BELGIAN')),
                       ('BZ', ('BELIZEAN')),
                       ('BJ', ('BENINESE')),
                       ('BT', ('BHUTANESE')),
                       ('BO', ('BOLIVIAN')),
                       ('BA', ('BOSNIAN OR HERZEGOVINIAN')),
                       ('BR', ('BRAZILIAN')),
                       ('GB-ENG', ('BRITISH')),
                       ('BN', ('BRUNEIAN')),
                       ('BG', ('BULGARIAN')),
                       ('BF', ('BURKINABE')),
                       ('MM', ('BURMESE')),
                       ('BI', ('BURUNDIAN')),
                       ('KH', ('CAMBODIAN')),
                       ('CM', ('CAMEROONIAN')),
                       ('CA', ('CANADIAN')),
                       ('CV', ('CAPE VERDEAN')),
                       ('CF', ('CENTRAL AFRICAN')),
                       ('TD', ('CHADIAN')),
                       ('CL', ('CHILEAN')),
                       ('CN', ('CHINESE')),
                       ('CO', ('COLOMBIAN')),
                       ('KM', ('COMORAN')),
                       ('CG', ('CONGOLESE')),
                       ('CR', ('COSTA RICAN')),
                       ('HR', ('CROATIAN')),
                       ('CU', ('CUBAN')),
                       ('CY', ('CYPRIOT')),
                       ('CZ', ('CZECH')),
                       ('DK', ('DANISH')),
                       ('DJ', ('DJIBOUTI')),
                       ('DO', ('DOMINICAN')),
                       ('NL', ('DUTCH')),
                       ('TL', ('EAST TIMORESE')),
                       ('EC', ('ECUADOREAN')),
                       ('EG', ('EGYPTIAN')),
                       ('AE', ('EMIRIAN')),
                       ('GQ', ('EQUATORIAL GUINEAN')),
                       ('ER', ('ERITREAN')),
                       ('EE', ('ESTONIAN')),
                       ('ET', ('ETHIOPIAN')),
                       ('FJ', ('FIJIAN')),
                       ('PH', ('FILIPINO')),
                       ('FI', ('FINNISH')),
                       ('FR', ('FRENCH')),
                       ('GA', ('GABONESE')),
                       ('GM', ('GAMBIAN')),
                       ('GE', ('GEORGIAN')),
                       ('DE', ('GERMAN')),
                       ('GH', ('GHANAIAN')),
                       ('GR', ('GREEK')),
                       ('GD', ('GRENADIAN')),
                       ('GT', ('GUATEMALAN')),
                       ('GW', ('GUINEA-BISSAUAN')),
                       ('GN', ('GUINEAN')),
                       ('GY', ('GUYANESE')),
                       ('HT', ('HAITIAN')),
                       ('HN', ('HONDURAN')),
                       ('HU', ('HUNGARIAN')),
                       ('KI', ('I-KIRIBATI')),
                       ('IS', ('ICELANDER')),
                       ('IN', ('INDIAN')),
                       ('ID', ('INDONESIAN')),
                       ('IR', ('IRANIAN')),
                       ('IQ', ('IRAQI')),
                       ('IE', ('IRISH')),
                       ('IL', ('ISRAELI')),
                       ('IT', ('ITALIAN')),
                       ('CI', ('IVORIAN')),
                       ('JM', ('JAMAICAN')),
                       ('JP', ('JAPANESE')),
                       ('JO', ('JORDANIAN')),
                       ('KZ', ('KAZAKHSTANI')),
                       ('KE', ('KENYAN')),
                       ('KN', ('KITTIAN AND NEVISIAN')),
                       ('KW', ('KUWAITI')),
                       ('KG', ('KYRGYZ')),
                       ('LA', ('LAOTIAN')),
                       ('LV', ('LATVIAN')),
                       ('LB', ('LEBANESE')),
                       ('LR', ('LIBERIAN')),
                       ('LY', ('LIBYAN')),
                       ('LI', ('LIECHTENSTEINER')),
                       ('LT', ('LITHUANIAN')),
                       ('LU', ('LUXEMBOURGER')),
                       ('MK', ('MACEDONIAN')),
                       ('MG', ('MALAGASY')),
                       ('MW', ('MALAWIAN')),
                       ('MY', ('MALAYSIAN')),
                       ('MV', ('MALDIVAN')),
                       ('ML', ('MALIAN')),
                       ('MT', ('MALTESE')),
                       ('MH', ('MARSHALLESE')),
                       ('MR', ('MAURITANIAN')),
                       ('MU', ('MAURITIAN')),
                       ('MX', ('MEXICAN')),
                       ('FM', ('MICRONESIAN')),
                       ('MD', ('MOLDOVAN')),
                       ('MC', ('MONACAN')),
                       ('MN', ('MONGOLIAN')),
                       ('MA', ('MOROCCAN')),
                       ('LS', ('MOSOTHO')),
                       ('MZ', ('MOZAMBICAN')),
                       ('NA', ('NAMIBIAN')),
                       ('NR', ('NAURUAN')),
                       ('NP', ('NEPALESE')),
                       ('NZ', ('NEW ZEALANDER')),
                       ('NI', ('NICARAGUAN')),
                       ('NG', ('NIGERIAN')),
                       ('NE', ('NIGERIEN')),
                       ('KP', ('NORTH KOREAN')),
                       ('GB-NIR', ('NORTHERN IRISH')),
                       ('NO', ('NORWEGIAN')),
                       ('OM', ('OMANI')),
                       ('PK', ('PAKISTANI')),
                       ('PW', ('PALAUAN')),
                       ('PA', ('PANAMANIAN')),
                       ('PG', ('PAPUA NEW GUINEAN')),
                       ('PY', ('PARAGUAYAN')),
                       ('PE', ('PERUVIAN')),
                       ('PL', ('POLISH')),
                       ('PT', ('PORTUGUESE')),
                       ('QA', ('QATARI')),
                       ('RO', ('ROMANIAN')),
                       ('RU', ('RUSSIAN')),
                       ('RW', ('RWANDAN')),
                       ('LC', ('SAINT LUCIAN')),
                       ('SV', ('SALVADORAN')),
                       ('WS', ('SAMOAN')),
                       ('SM', ('SAN MARINESE')),
                       ('ST', ('SAO TOMEAN')),
                       ('SA', ('SAUDI')),
                       ('GB-SCT', ('SCOTTISH')),
                       ('SN', ('SENEGALESE')),
                       ('RS', ('SERBIAN')),
                       ('SC', ('SEYCHELLOIS')),
                       ('SL', ('SIERRA LEONEAN')),
                       ('SK', ('SLOVAKIAN')),
                       ('SI', ('SLOVENIAN')),
                       ('SB', ('SOLOMON ISLANDER')),
                       ('SO', ('SOMALI')),
                       ('ZA', ('SOUTH AFRICAN')),
                       ('KR', ('SOUTH KOREAN')),
                       ('ES', ('SPANISH')),
                       ('LK', ('SRI LANKAN')),
                       ('SD', ('SUDANESE')),
                       ('SR', ('SURINAMER')),
                       ('SZ', ('SWAZI')),
                       ('SE', ('SWEDISH')),
                       ('CH', ('SWISS')),
                       ('SY', ('SYRIAN')),
                       ('TW', ('TAIWANESE')),
                       ('TJ', ('TAJIK')),
                       ('TZ', ('TANZANIAN')),
                       ('TH', ('THAI')),
                       ('TG', ('TOGOLESE')),
                       ('TO', ('TONGAN')),
                       ('TT', ('TRINIDADIAN OR TOBAGONIAN')),
                       ('TN', ('TUNISIAN')),
                       ('TR', ('TURKISH')),
                       ('TV', ('TUVALUAN')),
                       ('UG', ('UGANDAN')),
                       ('UA', ('UKRAINIAN')),
                       ('UY', ('URUGUAYAN')),
                       ('UZ', ('UZBEKISTANI')),
                       ('VE', ('VENEZUELAN')),
                       ('VN', ('VIETNAMESE')),
                       ('GB-WLS', ('WELSH')),
                       ('YE', ('YEMENITE')),
                       ('ZM', ('ZAMBIAN')),
                       ('ZW', ('ZIMBABWEAN')),
                       ('99', ('OTHER')))
country_choices = (('SG', ('SINGAPORE')),
                   ('AF', ('AFGHANISTAN')),
                   ('AL', ('ALBANIA')),
                   ('DZ', ('ALGERIA')),
                   ('AS', ('AMERICAN SAMOA')),
                   ('AD', ('ANDORRA')),
                   ('AO', ('ANGOLA')),
                   ('AI', ('ANGUILLA')),
                   ('AQ', ('ANTARCTICA')),
                   ('AG', ('ANTIGUA AND BARBUDA')),
                   ('AR', ('ARGENTINA')),
                   ('AM', ('ARMENIA')),
                   ('AW', ('ARUBA')),
                   ('AU', ('AUSTRALIA')),
                   ('AT', ('AUSTRIA')),
                   ('AZ', ('AZERBAIJAN')),
                   ('BS', ('BAHAMAS')),
                   ('BH', ('BAHRAIN')),
                   ('BD', ('BANGLADESH')),
                   ('BB', ('BARBADOS')),
                   ('BY', ('BELARUS')),
                   ('BE', ('BELGIUM')),
                   ('BZ', ('BELIZE')),
                   ('BJ', ('BENIN')),
                   ('BM', ('BERMUDA')),
                   ('BT', ('BHUTAN')),
                   ('BO', ('BOLIVIA')),
                   ('BA', ('BOSNIA AND HERZEGOVINA')),
                   ('BW', ('BOTSWANA')),
                   ('BV', ('BOUVET ISLAND')),
                   ('BR', ('BRAZIL')),
                   ('BQ', ('BRITISH ANTARCTIC TERRITORY')),
                   ('IO', ('BRITISH INDIAN OCEAN TERRITORY')),
                   ('VG', ('BRITISH VIRGIN ISLANDS')),
                   ('BN', ('BRUNEI')),
                   ('BG', ('BULGARIA')),
                   ('BF', ('BURKINA FASO')),
                   ('BI', ('BURUNDI')),
                   ('KH', ('CAMBODIA')),
                   ('CM', ('CAMEROON')),
                   ('CA', ('CANADA')),
                   ('CV', ('CAPE VERDE')),
                   ('KY', ('CAYMAN ISLANDS')),
                   ('CF', ('CENTRAL AFRICAN REPUBLIC')),
                   ('TD', ('CHAD')),
                   ('CL', ('CHILE')),
                   ('CN', ('CHINA')),
                   ('CX', ('CHRISTMAS ISLAND')),
                   ('CC', ('COCOS [KEELING] ISLANDS')),
                   ('CO', ('COLOMBIA')),
                   ('KM', ('COMOROS')),
                   ('CG', ('CONGO - BRAZZAVILLE')),
                   ('CD', ('CONGO - KINSHASA')),
                   ('CK', ('COOK ISLANDS')),
                   ('CR', ('COSTA RICA')),
                   ('HR', ('CROATIA')),
                   ('CU', ('CUBA')),
                   ('CW', ('CURACAO')),
                   ('CY', ('CYPRUS')),
                   ('CZ', ('CZECH REPUBLIC')),
                   ('CI', ("COTE D'IVOIRE")),
                   ('DK', ('DENMARK')),
                   ('DJ', ('DJIBOUTI')),
                   ('DM', ('DOMINICA')),
                   ('DO', ('DOMINICAN REPUBLIC')),
                   ('EC', ('ECUADOR')),
                   ('EG', ('EGYPT')),
                   ('SV', ('EL SALVADOR')),
                   ('GQ', ('EQUATORIAL GUINEA')),
                   ('ER', ('ERITREA')),
                   ('EE', ('ESTONIA')),
                   ('ET', ('ETHIOPIA')),
                   ('FK', ('FALKLAND ISLANDS')),
                   ('FO', ('FAROE ISLANDS')),
                   ('FJ', ('FIJI')),
                   ('FI', ('FINLAND')),
                   ('FR', ('FRANCE')),
                   ('GF', ('FRENCH GUIANA')),
                   ('PF', ('FRENCH POLYNESIA')),
                   ('TF', ('FRENCH SOUTHERN TERRITORIES')),
                   ('GA', ('GABON')),
                   ('GM', ('GAMBIA')),
                   ('GE', ('GEORGIA')),
                   ('DE', ('GERMANY')),
                   ('GH', ('GHANA')),
                   ('GI', ('GIBRALTAR')),
                   ('GR', ('GREECE')),
                   ('GL', ('GREENLAND')),
                   ('GD', ('GRENADA')),
                   ('GP', ('GUADELOUPE')),
                   ('GU', ('GUAM')),
                   ('GT', ('GUATEMALA')),
                   ('GG', ('GUERNSEY')),
                   ('GN', ('GUINEA')),
                   ('GW', ('GUINEA-BISSAU')),
                   ('GY', ('GUYANA')),
                   ('HT', ('HAITI')),
                   ('HM', ('HEARD ISLAND AND MCDONALD ISLANDS')),
                   ('HN', ('HONDURAS')),
                   ('HK', ('HONG KONG SAR CHINA')),
                   ('HU', ('HUNGARY')),
                   ('IS', ('ICELAND')),
                   ('IN', ('INDIA')),
                   ('ID', ('INDONESIA')),
                   ('IR', ('IRAN')),
                   ('IQ', ('IRAQ')),
                   ('IE', ('IRELAND')),
                   ('IM', ('ISLE OF MAN')),
                   ('IL', ('ISRAEL')),
                   ('IT', ('ITALY')),
                   ('JM', ('JAMAICA')),
                   ('JP', ('JAPAN')),
                   ('JE', ('JERSEY')),
                   ('JO', ('JORDAN')),
                   ('KZ', ('KAZAKHSTAN')),
                   ('KE', ('KENYA')),
                   ('KI', ('KIRIBATI')),
                   ('KW', ('KUWAIT')),
                   ('KG', ('KYRGYZSTAN')),
                   ('LA', ('LAOS')),
                   ('LV', ('LATVIA')),
                   ('LB', ('LEBANON')),
                   ('LS', ('LESOTHO')),
                   ('LR', ('LIBERIA')),
                   ('LY', ('LIBYA')),
                   ('LI', ('LIECHTENSTEIN')),
                   ('LT', ('LITHUANIA')),
                   ('LU', ('LUXEMBOURG')),
                   ('MO', ('MACAU SAR CHINA')),
                   ('MK', ('MACEDONIA')),
                   ('MG', ('MADAGASCAR')),
                   ('MW', ('MALAWI')),
                   ('MY', ('MALAYSIA')),
                   ('MV', ('MALDIVES')),
                   ('ML', ('MALI')),
                   ('MT', ('MALTA')),
                   ('MH', ('MARSHALL ISLANDS')),
                   ('MQ', ('MARTINIQUE')),
                   ('MR', ('MAURITANIA')),
                   ('MU', ('MAURITIUS')),
                   ('YT', ('MAYOTTE')),
                   ('MX', ('MEXICO')),
                   ('FM', ('MICRONESIA')),
                   ('MD', ('MOLDOVA')),
                   ('MC', ('MONACO')),
                   ('MN', ('MONGOLIA')),
                   ('ME', ('MONTENEGRO')),
                   ('MS', ('MONTSERRAT')),
                   ('MA', ('MOROCCO')),
                   ('MZ', ('MOZAMBIQUE')),
                   ('MM', ('MYANMAR [BURMA]')),
                   ('NA', ('NAMIBIA')),
                   ('NR', ('NAURU')),
                   ('NP', ('NEPAL')),
                   ('NL', ('NETHERLANDS')),
                   ('NC', ('NEW CALEDONIA')),
                   ('NZ', ('NEW ZEALAND')),
                   ('NI', ('NICARAGUA')),
                   ('NE', ('NIGER')),
                   ('NG', ('NIGERIA')),
                   ('NU', ('NIUE')),
                   ('NF', ('NORFOLK ISLAND')),
                   ('KP', ('NORTH KOREA')),
                   ('MP', ('NORTHERN MARIANA ISLANDS')),
                   ('NO', ('NORWAY')),
                   ('OM', ('OMAN')),
                   ('PK', ('PAKISTAN')),
                   ('PW', ('PALAU')),
                   ('PS', ('PALESTINIAN TERRITORIES')),
                   ('PA', ('PANAMA')),
                   ('PG', ('PAPUA NEW GUINEA')),
                   ('PY', ('PARAGUAY')),
                   ('PE', ('PERU')),
                   ('PH', ('PHILIPPINES')),
                   ('PN', ('PITCAIRN ISLANDS')),
                   ('PL', ('POLAND')),
                   ('PT', ('PORTUGAL')),
                   ('PR', ('PUERTO RICO')),
                   ('QA', ('QATAR')),
                   ('RO', ('ROMANIA')),
                   ('RU', ('RUSSIA')),
                   ('RW', ('RWANDA')),
                   ('RE', ('REUNION')),
                   ('BL', ('SAINT BARTHELEMY')),
                   ('SH', ('SAINT HELENA')),
                   ('KN', ('SAINT KITTS AND NEVIS')),
                   ('LC', ('SAINT LUCIA')),
                   ('MF', ('SAINT MARTIN')),
                   ('PM', ('SAINT PIERRE AND MIQUELON')),
                   ('VC', ('SAINT VINCENT AND THE GRENADINES')),
                   ('WS', ('SAMOA')),
                   ('SM', ('SAN MARINO')),
                   ('SA', ('SAUDI ARABIA')),
                   ('SN', ('SENEGAL')),
                   ('RS', ('SERBIA')),
                   ('SC', ('SEYCHELLES')),
                   ('SL', ('SIERRA LEONE')),
                   ('SK', ('SLOVAKIA')),
                   ('SI', ('SLOVENIA')),
                   ('SB', ('SOLOMON ISLANDS')),
                   ('SO', ('SOMALIA')),
                   ('ZA', ('SOUTH AFRICA')),
                   ('GS', ('SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS')),
                   ('KR', ('SOUTH KOREA')),
                   ('ES', ('SPAIN')),
                   ('LK', ('SRI LANKA')),
                   ('SD', ('SUDAN')),
                   ('SR', ('SURINAME')),
                   ('SJ', ('SVALBARD AND JAN MAYEN')),
                   ('SZ', ('SWAZILAND')),
                   ('SE', ('SWEDEN')),
                   ('CH', ('SWITZERLAND')),
                   ('SY', ('SYRIA')),
                   ('ST', ('SAO TOME AND PRINCIPE')),
                   ('TW', ('TAIWAN')),
                   ('TJ', ('TAJIKISTAN')),
                   ('TZ', ('TANZANIA')),
                   ('TH', ('THAILAND')),
                   ('TL', ('TIMOR-LESTE')),
                   ('TG', ('TOGO')),
                   ('TK', ('TOKELAU')),
                   ('TO', ('TONGA')),
                   ('TT', ('TRINIDAD AND TOBAGO')),
                   ('TN', ('TUNISIA')),
                   ('TR', ('TURKEY')),
                   ('TM', ('TURKMENISTAN')),
                   ('TC', ('TURKS AND CAICOS ISLANDS')),
                   ('TV', ('TUVALU')),
                   ('UM', ('U.S. MINOR OUTLYING ISLANDS')),
                   ('VI', ('U.S. VIRGIN ISLANDS')),
                   ('UG', ('UGANDA')),
                   ('UA', ('UKRAINE')),
                   ('AE', ('UNITED ARAB EMIRATES')),
                   ('GB', ('UNITED KINGDOM')),
                   ('US', ('UNITED STATES')),
                   ('UY', ('URUGUAY')),
                   ('UZ', ('UZBEKISTAN')),
                   ('VU', ('VANUATU')),
                   ('VA', ('VATICAN CITY')),
                   ('VE', ('VENEZUELA')),
                   ('VN', ('VIETNAM')),
                   ('WF', ('WALLIS AND FUTUNA')),
                   ('EH', ('WESTERN SAHARA')),
                   ('YE', ('YEMEN')),
                   ('ZM', ('ZAMBIA')),
                   ('ZW', ('ZIMBABWE')),
                   ('99', ('OTHER')))
township_choices = (('Bahan', 'Bahan Township, Yangon'),
                    ('Insein', 'Insein Township, Yangon'),
                    ('Hlaing', 'Hlaing Township, Yangon'),
                    ('Kamayut', 'Kamayut Township, Yangon'),
                    ('Tamwe', 'Tamwe Township, Yangon'),
                    ('Mayangone', 'Mayangone Township, Yangon'),
                    ('Sanchaung', 'Sanchaung Township, Yangon'),
                    ('Kyee Myin Daing', 'Kyee Myin Daing Township, Yangon'),
                    ('ThingyanKyun', 'ThingyanKyun Township, Yangon'),
                    ('South Okkalapa', 'South Okkalapa Township, Yangon'),
                    ('North Okkalapa', 'North Okkalapa Township, Yangon'),
                    ('South Dagon', 'South Dagon Township, Yangon'),
                    ('North Dagon', 'North Dagon Township, Yangon'),
                    ('Tharkata', 'Tharkata Township, Yangon'),
                    ('Dawpon', 'Dawpon Township, Yangon'),
                    ('Mingalar Taung Nyunt', 'Mingalar Taung Nyunt Township, Yangon'),
                    ('Lanmataw', 'Lamataw Township, Yangon'),
                    ('Botahtaung', 'Botahtaung Township, Yangon'),
                    ('Yankin', 'Yankin Township, Yangon'),
                    ('Kyauktada', 'Kyauktada Township, Yangon'),
                    ('HlaingTharYar', 'Hlaing Thar Yar Township, Yangon'),
                    ('ShwePyiThar', 'Shwe Pyi Thar Township, Yangon'),)

# Create your models here.
class UserProfile(models.Model):
    class Meta:
        abstract = False
        ordering = ['user']

    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    name = models.CharField(help_text="Name", blank=True, max_length=256)
    gender = models.CharField(help_text="Gender", blank=True, max_length=10)
    dob = models.DateField(help_text="DOB", blank=True, max_length=20)
    country_code = models.CharField(
        help_text="Country Code", blank=True, max_length=6)
    mobile = models.CharField(
        help_text="Mobile Number", blank=True, max_length=11)
    created_from = models.CharField(
        help_text="Created From", blank=True, max_length=255)
    active_user = models.BooleanField(default=False)
    language = models.CharField(max_length=10, blank=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class ProductCategory(models.Model):
    name = models.CharField(help_text="Name", max_length=256, blank=True)
    complete_name = models.CharField(help_text="Complete Name", max_length=256, blank=True)

    def __str__(self):
        return self.name


fs = FileSystemStorage(location='ecommerce/static/login/images/upload/')


class Product(models.Model):
    name = models.CharField(help_text='Product Name', blank=True, max_length=255)
    selling_price = models.IntegerField(help_text="Price", blank=True, )
    product_image = models.ImageField(upload_to='products', storage=fs, help_text="Product Image",
                                      default='placeholder.png', blank=True, null=True)
    currency = models.CharField(help_text='Currency', blank=True, max_length=255, default="Ks")
    is_sale = models.BooleanField(help_text="Available in Sale", default=True)
    category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, help_text="Product Category",
                                    default=1, )
    details = models.TextField("Product Detail", blank=True,
                               default="Product exports from China with High Quality. We always use the fresh and "
                                       "good quality.")
    weight = models.FloatField("Product Weight", blank=True, default=1)
    uom = models.CharField("Unit of Measurement", max_length=10, blank=True, default='kg')

    quantity = models.IntegerField("Quantity", blank=False, default=1)
    cart_quantity = models.IntegerField("Cart Quantity", blank=False, default=1)
    order_quantity = models.IntegerField("Order Quantity", blank=False, default=1)

    def __str__(self):
        return self.name

    def display_selling_price(self):
        return '{0}'.format(self.currency)

    def image_tag(self):
        if self.product_image:
            split_path = self.product_image.path.split(sep='/ecommerce', maxsplit=2)
            return mark_safe('<img src="%s" id="image_tag" width="180" height="180" />' % (split_path[1]))


class CustomerCategory(models.Model):
    name = models.CharField(help_text="Category", max_length=256, blank=True)
    complete_name = models.CharField(help_text="Category Name", max_length=256, blank=True)
    num_orders_from = models.IntegerField("Number of Orders From", blank=False, default=0)
    num_orders_to = models.IntegerField("Number of Orders To", blank=False, default=0)

    def __str__(self):
        return self.name

    def display_order_num(self):
        return '{0}'.format(self.num_orders_from)

    def display_order_num_to(self):
        return '{0}'.format(self.num_orders_to)

image_fs = FileSystemStorage(location='media/')
def create_new_ref_number():
    all_order = Order.objects.all()
    length_obj = len(all_order)
    order_no = "GR" + str(np.binary_repr(length_obj, width=12))
    # print("*** Order Number in default :::{0}".format(order_no))
    return order_no


class Order(models.Model):
    order_no = models.CharField("Order No.", max_length=16, blank=True, unique=True, default=create_new_ref_number)
    customer_name = models.CharField(help_text="Name", max_length=256, blank=False)
    customer_phone = models.CharField("Customer Phone", max_length=12, blank=False)
    customer_address = models.CharField("Customer Address", max_length=256, blank=True)
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE, )
    create_date = models.DateTimeField("Create Date", blank=True, )
    discount = models.IntegerField("Discount % ", blank=True, default=0)
    tax = models.DecimalField("Tax Amount", blank=True, default=0.0, decimal_places=2, max_digits=20)
    total = models.DecimalField("Total Amount", decimal_places=2, max_digits=20, blank=True, default=0.00)
    sub_total = models.DecimalField("Subtotal Amount", blank=True, default=0.0, decimal_places=2, max_digits=20)
    order_quantity = models.IntegerField("Order Quantity", blank=False, default=1)
    deli_fee = models.DecimalField("Delivery Charges", decimal_places=2, max_digits=20, blank=True, default=0.00)
    payment_type = models.CharField("Payment Type", max_length=256, blank=True)
    banking_type = models.CharField("Other Payment", max_length=256, blank=True)
    banking_image = models.ImageField(upload_to='banking', storage=image_fs, help_text="Banking Slip Image",
                                      default='banking.png', blank=True, null=True)

    def __str__(self):
        return self.order_no

    def display_customer_name(self):
        return  self.customer_name


    def save(self, *args, **kwargs):
        # import pdb;pdb.set_trace()
        order_items = self.order_items.all()
        total = Decimal(0)
        for order in order_items:
            total += order.total_price
        self.sub_total = total
        # print("*** Self Value in Order", self.total)
        self.total = Decimal(self.sub_total) - Decimal(self.discount) + Decimal(self.tax) + Decimal(self.deli_fee)
        super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    qty = models.PositiveIntegerField(default=1)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    discount_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    final_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    total_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.final_price = self.discount_price if self.discount_price > 0 else self.price
        self.total_price = Decimal(self.qty) * Decimal(self.final_price)
        super(OrderItem, self).save(*args, **kwargs)
        self.order.save()


User.profile = property(lambda u: UserProfile.objects.get_create(user=u))
