import datetime
from mongoengine import Document, StringField, DateTimeField

class Contrato(Document):
    Ano = StringField(required=True, max_length=20)
    Sector = StringField(required=True, max_length=200)
    Entidad = StringField(required=True, max_length=200)
    Beneficiario = StringField(required=True, max_length=200)
    CodigoSubUnidad = StringField(required=True, max_length=200)
    NombreSubUnidad = StringField(required=True, max_length=200)
    NumerodeCompromiso = StringField(required=True, max_length=200)
    TipodeDocumentoSoporte = StringField(required=True, max_length=200)
    NumerodeDocumentoSoporte = StringField(required=True, max_length=200)
    ObjetodelContrato = StringField(required=True, max_length=5000)
    RubrodelGasto = StringField(required=True, max_length=500)
    ValorDelCompromiso = StringField(required=True, max_length=200)
    Modificacion = DateTimeField(default=datetime.datetime.now)

