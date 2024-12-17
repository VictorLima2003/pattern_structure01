from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

FINANCIAL_INSTRUMENT_TYPE_CHOICES = [
    ('bank_account', 'Bank Account'),
    ('fund', 'Fund'),
    ('cri', 'CRI'),
    ('cra', 'CRA'),
    ('debenture', 'Debênture'),
]

ENTITY_TYPE_CHOICES = [
    ('pf', 'Pessoa Física'),
    ('pj', 'Pessoa Jurídica'),
]


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    iso3 = models.CharField(max_length=3, unique=True, null=False)
    nationality = models.CharField(max_length=255, null=False)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        db_table = 'country'

    def __str__(self):
        return f"{self.iso3} - {self.name}"


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    info = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'
        db_table = 'currency'

    def __str__(self):
        return f"{self.code} - {self.name}"


class FinancialInstitution(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255, null=False)
    info = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'financial_institution'
        verbose_name = 'Financial Institution'
        verbose_name_plural = 'Financial Institutions'

    def __str__(self):
        return self.name


class BankAccount(models.Model):
    id = models.AutoField(primary_key=True)
    financial_institution = models.ForeignKey(FinancialInstitution, on_delete=models.CASCADE, null=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=False)
    branch = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=255, null=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=False)
    info = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'bank_account'
        verbose_name = 'Bank Account'
        verbose_name_plural = 'Bank Accounts'
        unique_together = ('financial_institution', 'currency', 'branch', 'number', 'country')

    def __str__(self):
        return f"{self.financial_institution.name} - {self.branch} - {self.number} ({self.country.name})"


class FinancialInstrument(models.Model):
    id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=FINANCIAL_INSTRUMENT_TYPE_CHOICES)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=False)
    info = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'financial_instrument'
        verbose_name = 'Financial Instrument'
        verbose_name_plural = 'Financial Instruments'
        unique_together = ('ticker', 'name', 'type', 'currency')

    def __str__(self):
        return f"{self.name} ({self.ticker}, {self.type}, {self.currency.code})"


class Entity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=ENTITY_TYPE_CHOICES)
    info = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'entity'
        verbose_name = 'Entity'
        verbose_name_plural = 'Entities'

    def __str__(self):
        return f"{self.name} - ({self.type})"


class EntityBankAccount(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    info = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'entity_bank_account'
        verbose_name = 'Entity <->  Bank Account'
        verbose_name_plural = 'Entity <->  Bank Account'
        unique_together = ('entity', 'bank_account')

    def __str__(self):
        return f"{self.entity.name} - ({self.bank_account.financial_institution.name} - {self.bank_account.number})"


class Log(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.JSONField()
    table_name = models.CharField(max_length=255)
    change_time = models.DateTimeField(default=timezone.now)
    change_type = models.CharField(max_length=10)

    class Meta:
        db_table = '_log'
        verbose_name = 'Log'
        verbose_name_plural = 'Log'

    def __str__(self):
        return f"{self.table_name} - {self.change_type} - {self.change_time}"


class QuoteClose(models.Model):
    id = models.AutoField(primary_key=True)
    financial_instrument = models.ForeignKey(FinancialInstrument, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=40, decimal_places=20)
    source = models.CharField(max_length=32, default='maud')

    class Meta:
        db_table = 'quote_close'
        verbose_name = 'Quote Close'
        verbose_name_plural = 'Quote Close'
        unique_together = ('financial_instrument', 'date', 'source')

    def __str__(self):
        return f"{self.financial_instrument.ticker} - {self.date} - {self.source}"


class Contract(models.Model):
    entities = models.ManyToManyField('Entity', related_name='entities')
    bank_accounts = models.ManyToManyField('BankAccount')
    officer = models.ForeignKey('Entity', on_delete=models.CASCADE, related_name='officer_contracts', null=True)
    witnesses = models.ManyToManyField('Entity', related_name='witnesses')
    info = models.JSONField(null=True)
    upload_url = models.CharField(max_length=2048, null=True)
    last_update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contract'
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'

    def __str__(self):
        return f"Contract {self.id}"

class RoutineLog(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    info = models.JSONField(null=True)

    class Meta:
        db_table = 'routine_log'
        verbose_name = 'Routine Log'
        verbose_name_plural = 'Routine Log'

    def __str__(self):
        return f"{self.name} - {self.start_date:%Y-%m-%d.%H:%M:%S}"


class EventType(models.Model):
    name = models.CharField(max_length=255, primary_key=True)

    class Meta:
        db_table = 'event_type'
        verbose_name = 'Event Type'
        verbose_name_plural = 'Events Type'

    def __str__(self):
        return f"{self.name}"


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    declaration_date = models.DateField(blank=True, null=True)
    ex_date = models.DateField()
    record_date = models.DateField(blank=True, null=True)
    pay_date = models.DateField(blank=True, null=True)
    financial_instrument = models.ForeignKey(FinancialInstrument, on_delete=models.CASCADE)
    type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    factor = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'event'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f"{self.financial_instrument.name} - {self.type.name} - {self.ex_date:%Y-%m-%d}"


class IndustryClassification(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    field = models.CharField(max_length=255)
    id_father = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'industry_classification'
        verbose_name = 'Industry Classification'
        verbose_name_plural = 'Industry Classification'

    def __str__(self):
        return f"{self.field} - {self.name}"


class Portfolio(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    info = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'portfolio'
        verbose_name = 'Portfolio'
        verbose_name_plural = 'Portfolio'

    def __str__(self):
        return f"{self.name}"


class FinancialInstitutionTrade(models.Model):
    id = models.AutoField(primary_key=True)
    financial_institution = models.ForeignKey(FinancialInstitution, on_delete=models.CASCADE, null=False)
    info = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'financial_institution_trade'
        verbose_name = 'Financial Institution Trade'
        verbose_name_plural = 'Financial Institution Trades'

    def __str__(self):
        return f"{self.financial_institution.name} - {self.id}"

class PortfolioBankAccount(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    info = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'portfolio_bank_account'
        verbose_name = 'Portfolio <->  Bank Account'
        verbose_name_plural = 'Portfolio <->  Bank Account'
        unique_together = ('portfolio', 'bank_account')

    def __str__(self):
        return f"{self.portfolio.name} - ({self.bank_account.financial_institution.name} - {self.bank_account.number})"

# class Document(models.Model):
#     name = models.CharField(max_length=255)
#     extension = models.CharField(max_length=10)
#     tag = ArrayField(models.CharField(max_length=50), null=True, blank=True, default=list)
#     info = models.JSONField(null=True, blank=True)
#     base64 = models.TextField()
#
#     class Meta:
#         db_table = 'document'
#
#     def __str__(self):
#         return self.name

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    info = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'tag'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Document(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('url', 'URL'),
        ('base64', 'Base64'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    file_extension = models.CharField(max_length=10)
    type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES, default='url')
    content = models.TextField()
    info = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'database_document'


class DocumentTag(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'document_tag'
        verbose_name = 'Document Tag'
        verbose_name_plural = 'Document Tags'
        unique_together = ('document', 'tag')

    def __str__(self):
        return f"{self.document.name} - {self.tag.name}"