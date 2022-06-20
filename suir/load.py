from pathlib import Path
from django.db import transaction
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Point
from suir.models import Municipio, Comunidad
import json


codes = {
	'Bluefields':'BEF',
	'Corn Island':'CIS',
	'Kukrahill':'KHL',
	'Desembocadura del Rio Grande':'DRG',
	'El Ayote':'AYO',
	'El Rama':'RMA',
	'El Tortuguero':'TTG',
	'La Cruz de Rio Grande':'CRG',
	'Laguna de Perlas':'LAP',
	'Muelle de los Bueyes':'MLB',
	'Nueva Guinea':'NGA',
	'Paiwas':'PWA',
}

json_com = '''[
    {
      "lat" : 11.9958,
      "lng" : -83.68998,
      "municipio" : "BEF",
      "nombre" : "El Bluff (Puerto El Bluff)"
    },
    {
      "lat" : 11.40753,
      "lng" : -84.28327,
      "municipio" : "BEF",
      "nombre" : "Aguas Frías"
    },
    {
      "lat" : 11.37873,
      "lng" : -84.2923,
      "municipio" : "BEF",
      "nombre" : "Aguas Gatas"
    },
    {
      "lat" : 11.86704,
      "lng" : -84.03728,
      "municipio" : "BEF",
      "nombre" : "Asentamiento"
    },
    {
      "lat" : 11.984167,
      "lng" : -83.858317,
      "municipio" : "BEF",
      "nombre" : "Asentamiento Augusto C. Sandino"
    },
    {
      "lat" : 11.57932,
      "lng" : -84.01302,
      "municipio" : "BEF",
      "nombre" : "Atlanta"
    },
    {
      "lat" : 11.56707,
      "lng" : -83.72275,
      "municipio" : "BEF",
      "nombre" : "Bangkukuk Taik (Punta de Águila)"
    },
    {
      "lat" : 11.78974,
      "lng" : -83.82673,
      "municipio" : "BEF",
      "nombre" : "Big Creek"
    },
    {
      "lat" : 12.1007,
      "lng" : -83.997,
      "municipio" : "BEF",
      "nombre" : "Boca de Mahaganny"
    },
    {
      "lat" : 11.58181,
      "lng" : -84.09748,
      "municipio" : "BEF",
      "nombre" : "Boca Tapada"
    },
    {
      "lat" : 11.83733,
      "lng" : -84.12412,
      "municipio" : "BEF",
      "nombre" : "Boquita de Silva 1"
    },
    {
      "lat" : 11.84975,
      "lng" : -84.10309,
      "municipio" : "BEF",
      "nombre" : "Boquita de Silva 2"
    },
    {
      "lat" : 11.772783,
      "lng" : -83.97055,
      "municipio" : "BEF",
      "nombre" : "Buenos Aires"
    },
    {
      "lat" : 11.52169,
      "lng" : -83.90505,
      "municipio" : "BEF",
      "nombre" : "Camilo"
    },
    {
      "lat" : 11.77224,
      "lng" : -84.01823,
      "municipio" : "BEF",
      "nombre" : "Caño Azul 1"
    },
    {
      "lat" : 11.78041,
      "lng" : -84.01593,
      "municipio" : "BEF",
      "nombre" : "Caño Azul 2"
    },
    {
      "lat" : 11.997283,
      "lng" : -83.90945,
      "municipio" : "BEF",
      "nombre" : "Caño Azul de Santa Elena"
    },
    {
      "lat" : 12.043778,
      "lng" : -83.83507,
      "municipio" : "BEF",
      "nombre" : "Caño Blanco"
    },
    {
      "lat" : 11.8387,
      "lng" : -83.95057,
      "municipio" : "BEF",
      "nombre" : "Caño Maíz"
    },
    {
      "lat" : 12.12004,
      "lng" : -83.80385,
      "municipio" : "BEF",
      "nombre" : "Caño Negro"
    },
    {
      "lat" : 11.77617,
      "lng" : -84.03489,
      "municipio" : "BEF",
      "nombre" : "Coco 1"
    },
    {
      "lat" : 11.79086,
      "lng" : -84.05452,
      "municipio" : "BEF",
      "nombre" : "Coco 2"
    },
    {
      "lat" : 11.73753,
      "lng" : -83.94409,
      "municipio" : "BEF",
      "nombre" : "Colorado"
    },
    {
      "lat" : 11.70981,
      "lng" : -84.08797,
      "municipio" : "BEF",
      "nombre" : "Colorado de Masayita"
    },
    {
      "lat" : 12.09822,
      "lng" : -83.94537,
      "municipio" : "BEF",
      "nombre" : "Crisimbila"
    },
    {
      "lat" : 11.56048,
      "lng" : -84.05544,
      "municipio" : "BEF",
      "nombre" : "Daniel Guido"
    },
    {
      "lat" : 11.4404,
      "lng" : -83.93886,
      "municipio" : "BEF",
      "nombre" : "Diriangén de Pijibay"
    },
    {
      "lat" : 11.80499,
      "lng" : -83.91713,
      "municipio" : "BEF",
      "nombre" : "Dokuno"
    },
    {
      "lat" : 11.62033,
      "lng" : -84.08635,
      "municipio" : "BEF",
      "nombre" : "Dos de Oro Dos"
    },
    {
      "lat" : 11.80747,
      "lng" : -84.00914,
      "municipio" : "BEF",
      "nombre" : "El Cañal"
    },
    {
      "lat" : 11.51522,
      "lng" : -84.11894,
      "municipio" : "BEF",
      "nombre" : "El Coco"
    },
    {
      "lat" : 11.87619,
      "lng" : -84.0845,
      "municipio" : "BEF",
      "nombre" : "El Coloradito"
    },
    {
      "lat" : 11.56019,
      "lng" : -83.81504,
      "municipio" : "BEF",
      "nombre" : "El Corozo"
    },
    {
      "lat" : 11.93901,
      "lng" : -83.82288,
      "municipio" : "BEF",
      "nombre" : "El Danto"
    },
    {
      "lat" : 11.49817,
      "lng" : -84.09534,
      "municipio" : "BEF",
      "nombre" : "El Diamante"
    },
    {
      "lat" : 11.91302,
      "lng" : -84.08329,
      "municipio" : "BEF",
      "nombre" : "El Diamante de Kukra River"
    },
    {
      "lat" : 11.7065,
      "lng" : -83.88731,
      "municipio" : "BEF",
      "nombre" : "El Gorrión"
    },
    {
      "lat" : 11.77086,
      "lng" : -83.90844,
      "municipio" : "BEF",
      "nombre" : "El Guapote"
    },
    {
      "lat" : 11.54345,
      "lng" : -84.05128,
      "municipio" : "BEF",
      "nombre" : "El Guineo 1"
    },
    {
      "lat" : 11.50858,
      "lng" : -84.0554,
      "municipio" : "BEF",
      "nombre" : "El Guineo 2"
    },
    {
      "lat" : 11.5904,
      "lng" : -83.8137,
      "municipio" : "BEF",
      "nombre" : "El Javillo"
    },
    {
      "lat" : 11.7956,
      "lng" : -84.15121,
      "municipio" : "BEF",
      "nombre" : "El Limón"
    },
    {
      "lat" : 11.56408,
      "lng" : -83.9576,
      "municipio" : "BEF",
      "nombre" : "El Masayón"
    },
    {
      "lat" : 11.82317,
      "lng" : -84.03282,
      "municipio" : "BEF",
      "nombre" : "El Naranjal"
    },
    {
      "lat" : 11.51715,
      "lng" : -84.01287,
      "municipio" : "BEF",
      "nombre" : "El Naranjo"
    },
    {
      "lat" : 11.35494,
      "lng" : -84.31197,
      "municipio" : "BEF",
      "nombre" : "El Pajarito"
    },
    {
      "lat" : 11.34271,
      "lng" : -84.33852,
      "municipio" : "BEF",
      "nombre" : "El Pájaro"
    },
    {
      "lat" : 11.6223,
      "lng" : -83.9273,
      "municipio" : "BEF",
      "nombre" : "El Papayo"
    },
    {
      "lat" : 11.77958,
      "lng" : -84.06685,
      "municipio" : "BEF",
      "nombre" : "El Paraíso de Kukra River"
    },
    {
      "lat" : 11.6267,
      "lng" : -83.9531,
      "municipio" : "BEF",
      "nombre" : "El Pato"
    },
    {
      "lat" : 11.47395,
      "lng" : -83.87747,
      "municipio" : "BEF",
      "nombre" : "El Pijibay"
    },
    {
      "lat" : 11.5353,
      "lng" : -83.8712,
      "municipio" : "BEF",
      "nombre" : "El Porvenir"
    },
    {
      "lat" : 11.65758,
      "lng" : -83.92728,
      "municipio" : "BEF",
      "nombre" : "El Progreso"
    },
    {
      "lat" : 11.8737,
      "lng" : -84.10686,
      "municipio" : "BEF",
      "nombre" : "El Quebradón"
    },
    {
      "lat" : 11.59193,
      "lng" : -84.06582,
      "municipio" : "BEF",
      "nombre" : "El Quemado"
    },
    {
      "lat" : 11.90854,
      "lng" : -84.14486,
      "municipio" : "BEF",
      "nombre" : "El Virgen"
    },
    {
      "lat" : 11.53302,
      "lng" : -83.93403,
      "municipio" : "BEF",
      "nombre" : "Eloysa"
    },
    {
      "lat" : 11.99844,
      "lng" : -84.10606,
      "municipio" : "BEF",
      "nombre" : "Guana Creek"
    },
    {
      "lat" : 11.31581,
      "lng" : -84.30588,
      "municipio" : "BEF",
      "nombre" : "Jasmín del Guineo"
    },
    {
      "lat" : 11.30132,
      "lng" : -84.33234,
      "municipio" : "BEF",
      "nombre" : "Jasmín del Guineo 2"
    },
    {
      "lat" : 11.85135,
      "lng" : -84.04189,
      "municipio" : "BEF",
      "nombre" : "La Aurora"
    },
    {
      "lat" : 11.56393,
      "lng" : -83.9455,
      "municipio" : "BEF",
      "nombre" : "La Bocana Masayón"
    },
    {
      "lat" : 11.30272,
      "lng" : -84.21894,
      "municipio" : "BEF",
      "nombre" : "La Concepción de Piedra Fina"
    },
    {
      "lat" : 11.58364,
      "lng" : -83.85189,
      "municipio" : "BEF",
      "nombre" : "La Coquera Monte Cristo"
    },
    {
      "lat" : 11.77104,
      "lng" : -83.8166,
      "municipio" : "BEF",
      "nombre" : "La Cuna"
    },
    {
      "lat" : 11.4986,
      "lng" : -84.1539,
      "municipio" : "BEF",
      "nombre" : "La Gloria"
    },
    {
      "lat" : 11.39011,
      "lng" : -84.33554,
      "municipio" : "BEF",
      "nombre" : "La Guitarra"
    },
    {
      "lat" : 11.93189,
      "lng" : -84.03293,
      "municipio" : "BEF",
      "nombre" : "Las Breñas 1"
    },
    {
      "lat" : 11.9301,
      "lng" : -84.0149,
      "municipio" : "BEF",
      "nombre" : "Las Breñas 2"
    },
    {
      "lat" : 11.92626,
      "lng" : -83.93176,
      "municipio" : "BEF",
      "nombre" : "Las Cuevas"
    },
    {
      "lat" : 11.6268,
      "lng" : -83.95235,
      "municipio" : "BEF",
      "nombre" : "Las Delicias"
    },
    {
      "lat" : 11.4624,
      "lng" : -84.02398,
      "municipio" : "BEF",
      "nombre" : "Las Flores"
    },
    {
      "lat" : 11.6919,
      "lng" : -83.7303,
      "municipio" : "BEF",
      "nombre" : "Las Nubes"
    },
    {
      "lat" : 11.6129,
      "lng" : -83.7536,
      "municipio" : "BEF",
      "nombre" : "Las Pavas"
    },
    {
      "lat" : 11.70569,
      "lng" : -84.01929,
      "municipio" : "BEF",
      "nombre" : "Los Ángeles de Masayon"
    },
    {
      "lat" : 11.83163,
      "lng" : -84.16652,
      "municipio" : "BEF",
      "nombre" : "Los Peñones"
    },
    {
      "lat" : 11.58902,
      "lng" : -83.88978,
      "municipio" : "BEF",
      "nombre" : "Masayita"
    },
    {
      "lat" : 11.54457,
      "lng" : -84.00952,
      "municipio" : "BEF",
      "nombre" : "Molinares"
    },
    {
      "lat" : 11.5959,
      "lng" : -83.65817,
      "municipio" : "BEF",
      "nombre" : "Monkey Point"
    },
    {
      "lat" : 11.6296,
      "lng" : -83.87556,
      "municipio" : "BEF",
      "nombre" : "Monte Cristo"
    },
    {
      "lat" : 11.39196,
      "lng" : -84.1608,
      "municipio" : "BEF",
      "nombre" : "Monte Verde"
    },
    {
      "lat" : 11.94598,
      "lng" : -83.80852,
      "municipio" : "BEF",
      "nombre" : "Musilaina"
    },
    {
      "lat" : 11.59824,
      "lng" : -83.80273,
      "municipio" : "BEF",
      "nombre" : "Nueva Esperanza"
    },
    {
      "lat" : 11.42363,
      "lng" : -84.31906,
      "municipio" : "BEF",
      "nombre" : "Nuevo Delirio"
    },
    {
      "lat" : 11.47993,
      "lng" : -84.35619,
      "municipio" : "BEF",
      "nombre" : "Nuevo San Antonio"
    },
    {
      "lat" : 11.52917,
      "lng" : -83.92187,
      "municipio" : "BEF",
      "nombre" : "Palo Bonito"
    },
    {
      "lat" : 11.43937,
      "lng" : -84.23344,
      "municipio" : "BEF",
      "nombre" : "Paraíso de Aguas Zarcas"
    },
    {
      "lat" : 11.37988,
      "lng" : -84.21774,
      "municipio" : "BEF",
      "nombre" : "Piedra Fina"
    },
    {
      "lat" : 11.73507,
      "lng" : -83.98042,
      "municipio" : "BEF",
      "nombre" : "Poza Azul"
    },
    {
      "lat" : 11.7177,
      "lng" : -83.9803,
      "municipio" : "BEF",
      "nombre" : "Poza Azul de Kukra River"
    },
    {
      "lat" : 11.60707,
      "lng" : -84.08647,
      "municipio" : "BEF",
      "nombre" : "Pueblo Nuevo"
    },
    {
      "lat" : 11.88227,
      "lng" : -83.80937,
      "municipio" : "BEF",
      "nombre" : "Rama Cay"
    },
    {
      "lat" : 11.29191,
      "lng" : -83.8754,
      "municipio" : "BEF",
      "nombre" : "Río Maíz"
    },
    {
      "lat" : 11.76438,
      "lng" : -84.12022,
      "municipio" : "BEF",
      "nombre" : "Rubén Darío"
    },
    {
      "lat" : 11.50233,
      "lng" : -84.18549,
      "municipio" : "BEF",
      "nombre" : "Salto de León"
    },
    {
      "lat" : 12.06309,
      "lng" : -83.81287,
      "municipio" : "BEF",
      "nombre" : "San Antonio (Playa Seca)"
    },
    {
      "lat" : 11.28511,
      "lng" : -84.22472,
      "municipio" : "BEF",
      "nombre" : "San Diego"
    },
    {
      "lat" : 11.41563,
      "lng" : -84.2506,
      "municipio" : "BEF",
      "nombre" : "San Francisco de Agua Frías"
    },
    {
      "lat" : 11.74706,
      "lng" : -84.11324,
      "municipio" : "BEF",
      "nombre" : "San Isidro"
    },
    {
      "lat" : 11.89238,
      "lng" : -84.01556,
      "municipio" : "BEF",
      "nombre" : "San José"
    },
    {
      "lat" : 11.296194,
      "lng" : -84.173222,
      "municipio" : "BEF",
      "nombre" : "San José de las Brisas"
    },
    {
      "lat" : 11.38826,
      "lng" : -84.35466,
      "municipio" : "BEF",
      "nombre" : "San Luis de Aguas Gatas"
    },
    {
      "lat" : 12.09247,
      "lng" : -83.79631,
      "municipio" : "BEF",
      "nombre" : "San Mariano"
    },
    {
      "lat" : 11.60723,
      "lng" : -83.85622,
      "municipio" : "BEF",
      "nombre" : "San Miguel"
    },
    {
      "lat" : 12.10022,
      "lng" : -83.79968,
      "municipio" : "BEF",
      "nombre" : "San Nicolás"
    },
    {
      "lat" : 11.4656,
      "lng" : -84.22239,
      "municipio" : "BEF",
      "nombre" : "San Pablo"
    },
    {
      "lat" : 11.39193,
      "lng" : -84.19623,
      "municipio" : "BEF",
      "nombre" : "San Pedro"
    },
    {
      "lat" : 11.69259,
      "lng" : -83.83772,
      "municipio" : "BEF",
      "nombre" : "San Rafael"
    },
    {
      "lat" : 11.31276,
      "lng" : -84.21377,
      "municipio" : "BEF",
      "nombre" : "San Rafael del Zahino"
    },
    {
      "lat" : 11.97603,
      "lng" : -83.96525,
      "municipio" : "BEF",
      "nombre" : "San Sebastian"
    },
    {
      "lat" : 11.47545,
      "lng" : -84.20694,
      "municipio" : "BEF",
      "nombre" : "San Sebastian de Aguas Zarcas"
    },
    {
      "lat" : 11.37594,
      "lng" : -84.10844,
      "municipio" : "BEF",
      "nombre" : "Santa Elena"
    },
    {
      "lat" : 11.87166,
      "lng" : -83.95303,
      "municipio" : "BEF",
      "nombre" : "Santa Elisa"
    },
    {
      "lat" : 11.80407,
      "lng" : -84.11934,
      "municipio" : "BEF",
      "nombre" : "Santa Fé"
    },
    {
      "lat" : 11.31374,
      "lng" : -84.26465,
      "municipio" : "BEF",
      "nombre" : "Santa Fé del Caracol"
    },
    {
      "lat" : 11.6559,
      "lng" : -84.0332,
      "municipio" : "BEF",
      "nombre" : "Santa Isabel"
    },
    {
      "lat" : 11.47561,
      "lng" : -84.05727,
      "municipio" : "BEF",
      "nombre" : "Santa Rosa del Guineo"
    },
    {
      "lat" : 11.528533,
      "lng" : -83.880233,
      "municipio" : "BEF",
      "nombre" : "Santa Rosa del Porvenir"
    },
    {
      "lat" : 11.68877,
      "lng" : -83.96998,
      "municipio" : "BEF",
      "nombre" : "Santo Tomás Masayón"
    },
    {
      "lat" : 12.02223,
      "lng" : -83.81683,
      "municipio" : "BEF",
      "nombre" : "Sconfran"
    },
    {
      "lat" : 12.117,
      "lng" : -83.7411,
      "municipio" : "BEF",
      "nombre" : "Smokey Lane"
    },
    {
      "lat" : 11.95992,
      "lng" : -83.98203,
      "municipio" : "BEF",
      "nombre" : "Taleno"
    },
    {
      "lat" : 11.89594,
      "lng" : -83.93416,
      "municipio" : "BEF",
      "nombre" : "Ticktick Caanu (Zompopera)"
    },
    {
      "lat" : 11.81295,
      "lng" : -84.05183,
      "municipio" : "BEF",
      "nombre" : "Toboba"
    },
    {
      "lat" : 11.7731,
      "lng" : -83.8941,
      "municipio" : "BEF",
      "nombre" : "Torsuanny"
    },
    {
      "lat" : 11.81753,
      "lng" : -84.07974,
      "municipio" : "BEF",
      "nombre" : "Villa Nueva"
    },
    {
      "lat" : 11.73907,
      "lng" : -83.76717,
      "municipio" : "BEF",
      "nombre" : "Willin Cay 1"
    },
    {
      "lat" : 11.70666,
      "lng" : -83.77401,
      "municipio" : "BEF",
      "nombre" : "Willin Cay 2"
    },
    {
      "lat" : 11.67381,
      "lng" : -83.83569,
      "municipio" : "BEF",
      "nombre" : "Wiring Cay"
    },
    {
      "lat" : 11.77347,
      "lng" : -83.75752,
      "municipio" : "BEF",
      "nombre" : "Yaladina"
    },
    {
      "lat" : 12.17582,
      "lng" : -83.05981,
      "municipio" : "CIS",
      "nombre" : "Brig Bay I"
    },
    {
      "lat" : 12.16391,
      "lng" : -83.06921,
      "municipio" : "CIS",
      "nombre" : "Brig Bay II"
    },
    {
      "lat" : 12.18371,
      "lng" : -83.0516,
      "municipio" : "CIS",
      "nombre" : "North End"
    },
    {
      "lat" : 12.15156,
      "lng" : -83.06326,
      "municipio" : "CIS",
      "nombre" : "Quinn Hill"
    },
    {
      "lat" : 12.1751508,
      "lng" : -83.037239,
      "municipio" : "CIS",
      "nombre" : "Sally Peachie"
    },
    {
      "lat" : 12.17024,
      "lng" : -83.04074,
      "municipio" : "CIS",
      "nombre" : "South End"
    },
    {
      "lat" : 12.28727,
      "lng" : -82.98111,
      "municipio" : "CIS",
      "nombre" : "Little Corn Island"
    },
    {
      "lat" : 13.25529,
      "lng" : -83.98927,
      "municipio" : "DRG",
      "nombre" : "Company Creek"
    },
    {
      "lat" : 13.2131,
      "lng" : -83.9256,
      "municipio" : "DRG",
      "nombre" : "Guadalupe"
    },
    {
      "lat" : 12.89395,
      "lng" : -83.58325,
      "municipio" : "DRG",
      "nombre" : "Kara"
    },
    {
      "lat" : 12.934549,
      "lng" : -83.577884,
      "municipio" : "DRG",
      "nombre" : "Karawala"
    },
    {
      "lat" : 12.90642,
      "lng" : -83.52388,
      "municipio" : "DRG",
      "nombre" : "La Barra"
    },
    {
      "lat" : 13.14645,
      "lng" : -83.90263,
      "municipio" : "DRG",
      "nombre" : "La Esperanza"
    },
    {
      "lat" : 12.96295,
      "lng" : -83.53207,
      "municipio" : "DRG",
      "nombre" : "Sandy Bay Sirpi"
    },
    {
      "lat" : 12.94016,
      "lng" : -83.53586,
      "municipio" : "DRG",
      "nombre" : "Walpa"
    },
    {
      "lat" : 12.38561,
      "lng" : -84.17574,
      "municipio" : "RMA",
      "nombre" : "Aguas Calientes"
    },
    {
      "lat" : 12.44731,
      "lng" : -84.48325,
      "municipio" : "RMA",
      "nombre" : "Bella Vista"
    },
    {
      "lat" : 12.00045,
      "lng" : -84.35242,
      "municipio" : "RMA",
      "nombre" : "Boca Azul"
    },
    {
      "lat" : 12.01909,
      "lng" : -84.33369,
      "municipio" : "RMA",
      "nombre" : "Boca Azulita"
    },
    {
      "lat" : 11.83728,
      "lng" : -84.12391,
      "municipio" : "RMA",
      "nombre" : "Boquita de Silva"
    },
    {
      "lat" : 11.80415,
      "lng" : -84.11945,
      "municipio" : "RMA",
      "nombre" : "Boquita de Silva N°2"
    },
    {
      "lat" : 12.51081,
      "lng" : -84.2318,
      "municipio" : "RMA",
      "nombre" : "Cabecera de Valentín"
    },
    {
      "lat" : 12.29759,
      "lng" : -84.25247,
      "municipio" : "RMA",
      "nombre" : "Calderon"
    },
    {
      "lat" : 12.37513,
      "lng" : -84.28558,
      "municipio" : "RMA",
      "nombre" : "Caño Adolfo"
    },
    {
      "lat" : 12.25412,
      "lng" : -84.49007,
      "municipio" : "RMA",
      "nombre" : "Caño García"
    },
    {
      "lat" : 12.4606,
      "lng" : -84.27815,
      "municipio" : "RMA",
      "nombre" : "Caño Valentín"
    },
    {
      "lat" : 12.34315,
      "lng" : -84.1582,
      "municipio" : "RMA",
      "nombre" : "Caño Wilson"
    },
    {
      "lat" : 11.92323,
      "lng" : -84.23445,
      "municipio" : "RMA",
      "nombre" : "Cedro Macho"
    },
    {
      "lat" : 12.38841,
      "lng" : -84.66748,
      "municipio" : "RMA",
      "nombre" : "Cerro Grande"
    },
    {
      "lat" : 12.13961,
      "lng" : -84.09879,
      "municipio" : "RMA",
      "nombre" : "Chalmeca Abajo"
    },
    {
      "lat" : 12.2151,
      "lng" : -84.09421,
      "municipio" : "RMA",
      "nombre" : "Chalmeca Arriba"
    },
    {
      "lat" : 12.18837,
      "lng" : -84.09012,
      "municipio" : "RMA",
      "nombre" : "Chalmeca Centro"
    },
    {
      "lat" : 12.41417,
      "lng" : -84.40584,
      "municipio" : "RMA",
      "nombre" : "Correntada Larga"
    },
    {
      "lat" : 12.23937,
      "lng" : -84.25842,
      "municipio" : "RMA",
      "nombre" : "Cuatro Esquina"
    },
    {
      "lat" : 12.1665,
      "lng" : -84.38118,
      "municipio" : "RMA",
      "nombre" : "Diamante Rojo"
    },
    {
      "lat" : 12.14963,
      "lng" : -84.27087,
      "municipio" : "RMA",
      "nombre" : "El Amparo"
    },
    {
      "lat" : 12.22715,
      "lng" : -84.23576,
      "municipio" : "RMA",
      "nombre" : "El Areno"
    },
    {
      "lat" : 12.10202,
      "lng" : -84.11273,
      "municipio" : "RMA",
      "nombre" : "El Banco"
    },
    {
      "lat" : 11.93884,
      "lng" : -84.08642,
      "municipio" : "RMA",
      "nombre" : "El Carmen"
    },
    {
      "lat" : 12.06518,
      "lng" : -84.15485,
      "municipio" : "RMA",
      "nombre" : "El Castillo"
    },
    {
      "lat" : 11.87625,
      "lng" : -84.08454,
      "municipio" : "RMA",
      "nombre" : "El Coloradito"
    },
    {
      "lat" : 12.21537,
      "lng" : -84.17339,
      "municipio" : "RMA",
      "nombre" : "El Colorado"
    },
    {
      "lat" : 12.05088,
      "lng" : -84.20193,
      "municipio" : "RMA",
      "nombre" : "El Delirio"
    },
    {
      "lat" : 11.91273,
      "lng" : -84.10599,
      "municipio" : "RMA",
      "nombre" : "El Diamante"
    },
    {
      "lat" : 12.05241,
      "lng" : -84.33897,
      "municipio" : "RMA",
      "nombre" : "El Embudo"
    },
    {
      "lat" : 12.38711,
      "lng" : -84.39811,
      "municipio" : "RMA",
      "nombre" : "El Garrobo"
    },
    {
      "lat" : 12.52971,
      "lng" : -84.48256,
      "municipio" : "RMA",
      "nombre" : "El Guabo"
    },
    {
      "lat" : 12.49161,
      "lng" : -84.67401,
      "municipio" : "RMA",
      "nombre" : "El Jobito"
    },
    {
      "lat" : 12.43193,
      "lng" : -84.6837,
      "municipio" : "RMA",
      "nombre" : "El Jobo"
    },
    {
      "lat" : 12.28209,
      "lng" : -84.55045,
      "municipio" : "RMA",
      "nombre" : "El Limón"
    },
    {
      "lat" : 12.11759,
      "lng" : -84.20261,
      "municipio" : "RMA",
      "nombre" : "El Milan"
    },
    {
      "lat" : 11.98195,
      "lng" : -84.21226,
      "municipio" : "RMA",
      "nombre" : "El Mobile"
    },
    {
      "lat" : 12.43688,
      "lng" : -84.34062,
      "municipio" : "RMA",
      "nombre" : "El Molejón"
    },
    {
      "lat" : 12.0039,
      "lng" : -84.30398,
      "municipio" : "RMA",
      "nombre" : "El Murciélago"
    },
    {
      "lat" : 12.03889,
      "lng" : -84.31083,
      "municipio" : "RMA",
      "nombre" : "El Palmar"
    },
    {
      "lat" : 12.11776,
      "lng" : -84.06682,
      "municipio" : "RMA",
      "nombre" : "El Paraíso"
    },
    {
      "lat" : 12.0185,
      "lng" : -84.14677,
      "municipio" : "RMA",
      "nombre" : "El Pavón"
    },
    {
      "lat" : 12.03449,
      "lng" : -84.21628,
      "municipio" : "RMA",
      "nombre" : "El Porvenir"
    },
    {
      "lat" : 12.17397,
      "lng" : -84.31682,
      "municipio" : "RMA",
      "nombre" : "El Recreo"
    },
    {
      "lat" : 12.18194,
      "lng" : -84.25998,
      "municipio" : "RMA",
      "nombre" : "El Silencio"
    },
    {
      "lat" : 12.51204,
      "lng" : -84.18969,
      "municipio" : "RMA",
      "nombre" : "El Toro"
    },
    {
      "lat" : 11.90809,
      "lng" : -84.1459,
      "municipio" : "RMA",
      "nombre" : "El Virgen"
    },
    {
      "lat" : 12.06345,
      "lng" : -84.12456,
      "municipio" : "RMA",
      "nombre" : "Fruta de Pan"
    },
    {
      "lat" : 11.99145,
      "lng" : -84.23717,
      "municipio" : "RMA",
      "nombre" : "Guadalupe"
    },
    {
      "lat" : 11.96273,
      "lng" : -84.06583,
      "municipio" : "RMA",
      "nombre" : "Guana Kreek"
    },
    {
      "lat" : 12.43048,
      "lng" : -84.31818,
      "municipio" : "RMA",
      "nombre" : "Ignacia"
    },
    {
      "lat" : 12.40027,
      "lng" : -84.60899,
      "municipio" : "RMA",
      "nombre" : "Isla Grande"
    },
    {
      "lat" : 12.06601,
      "lng" : -84.23203,
      "municipio" : "RMA",
      "nombre" : "Julio Buitrago"
    },
    {
      "lat" : 12.30458,
      "lng" : -84.75018,
      "municipio" : "RMA",
      "nombre" : "Kilaika"
    },
    {
      "lat" : 12.25982,
      "lng" : -84.48967,
      "municipio" : "RMA",
      "nombre" : "Kisilala"
    },
    {
      "lat" : 12.26096,
      "lng" : -84.47253,
      "municipio" : "RMA",
      "nombre" : "Kisilala (Contiguo Kisilala N°2)"
    },
    {
      "lat" : 12.26589,
      "lng" : -84.35735,
      "municipio" : "RMA",
      "nombre" : "Kisilala N°1"
    },
    {
      "lat" : 12.2655,
      "lng" : -84.42239,
      "municipio" : "RMA",
      "nombre" : "Kisilala N°2"
    },
    {
      "lat" : 12.5995,
      "lng" : -84.64849,
      "municipio" : "RMA",
      "nombre" : "Kurinwasito"
    },
    {
      "lat" : 12.08161,
      "lng" : -84.25311,
      "municipio" : "RMA",
      "nombre" : "La Ceiba"
    },
    {
      "lat" : 12.09037,
      "lng" : -84.2204,
      "municipio" : "RMA",
      "nombre" : "La Concha Río Rama"
    },
    {
      "lat" : 12.20885,
      "lng" : -84.42814,
      "municipio" : "RMA",
      "nombre" : "La Concha Vía Carretera"
    },
    {
      "lat" : 12.17607,
      "lng" : -84.35504,
      "municipio" : "RMA",
      "nombre" : "La Corona"
    },
    {
      "lat" : 12.54535,
      "lng" : -84.62154,
      "municipio" : "RMA",
      "nombre" : "La Danta"
    },
    {
      "lat" : 12.20027,
      "lng" : -84.28955,
      "municipio" : "RMA",
      "nombre" : "La Esperanza"
    },
    {
      "lat" : 12.06239,
      "lng" : -84.27113,
      "municipio" : "RMA",
      "nombre" : "La Fortuna"
    },
    {
      "lat" : 12.13526,
      "lng" : -84.14431,
      "municipio" : "RMA",
      "nombre" : "La Mosquitia"
    },
    {
      "lat" : 12.2585,
      "lng" : -84.10004,
      "municipio" : "RMA",
      "nombre" : "La Palma"
    },
    {
      "lat" : 12.14316,
      "lng" : -84.25523,
      "municipio" : "RMA",
      "nombre" : "La Palmera"
    },
    {
      "lat" : 12.4455,
      "lng" : -84.41982,
      "municipio" : "RMA",
      "nombre" : "La Piñuela"
    },
    {
      "lat" : 12.30432,
      "lng" : -84.16497,
      "municipio" : "RMA",
      "nombre" : "La Raicilla"
    },
    {
      "lat" : 11.95055,
      "lng" : -84.14638,
      "municipio" : "RMA",
      "nombre" : "La Sardina"
    },
    {
      "lat" : 12.18707,
      "lng" : -84.01202,
      "municipio" : "RMA",
      "nombre" : "La Sompopa"
    },
    {
      "lat" : 12.29405,
      "lng" : -84.38335,
      "municipio" : "RMA",
      "nombre" : "La Tigra"
    },
    {
      "lat" : 12.59172,
      "lng" : -84.60918,
      "municipio" : "RMA",
      "nombre" : "La Toalla"
    },
    {
      "lat" : 11.98735,
      "lng" : -84.14708,
      "municipio" : "RMA",
      "nombre" : "La Virgen"
    },
    {
      "lat" : 12.03369,
      "lng" : -84.26026,
      "municipio" : "RMA",
      "nombre" : "Las Iguanas"
    },
    {
      "lat" : 12.23769,
      "lng" : -84.1172,
      "municipio" : "RMA",
      "nombre" : "Las Lapas"
    },
    {
      "lat" : 11.88806,
      "lng" : -84.19362,
      "municipio" : "RMA",
      "nombre" : "Loma Linda"
    },
    {
      "lat" : 12.09735,
      "lng" : -84.05849,
      "municipio" : "RMA",
      "nombre" : "Magnolia"
    },
    {
      "lat" : 12.10151,
      "lng" : -84.18355,
      "municipio" : "RMA",
      "nombre" : "María Cristina"
    },
    {
      "lat" : 12.2999,
      "lng" : -84.3223,
      "municipio" : "RMA",
      "nombre" : "Mataka"
    },
    {
      "lat" : 12.30448,
      "lng" : -84.41408,
      "municipio" : "RMA",
      "nombre" : "Minas de Kisilala"
    },
    {
      "lat" : 12.4312,
      "lng" : -84.52476,
      "municipio" : "RMA",
      "nombre" : "Mirasol"
    },
    {
      "lat" : 12.36382,
      "lng" : -84.25286,
      "municipio" : "RMA",
      "nombre" : "Monte Rosa"
    },
    {
      "lat" : 12.31532,
      "lng" : -84.48534,
      "municipio" : "RMA",
      "nombre" : "Montes de Oro"
    },
    {
      "lat" : 12.25136,
      "lng" : -84.30197,
      "municipio" : "RMA",
      "nombre" : "Muelle  Real"
    },
    {
      "lat" : 12.35546,
      "lng" : -84.56232,
      "municipio" : "RMA",
      "nombre" : "Musuwaka"
    },
    {
      "lat" : 12.46788,
      "lng" : -84.16502,
      "municipio" : "RMA",
      "nombre" : "Nuevo Sauce"
    },
    {
      "lat" : 12.17831,
      "lng" : -84.23609,
      "municipio" : "RMA",
      "nombre" : "Oscar Brenes"
    },
    {
      "lat" : 12.13791,
      "lng" : -84.21425,
      "municipio" : "RMA",
      "nombre" : "Pablo Ubeda"
    },
    {
      "lat" : 12.13418,
      "lng" : -84.33255,
      "municipio" : "RMA",
      "nombre" : "Pijibay (El Recreo)"
    },
    {
      "lat" : 12.42304,
      "lng" : -84.23533,
      "municipio" : "RMA",
      "nombre" : "Pijibay (Wapi)"
    },
    {
      "lat" : 12.34619,
      "lng" : -84.77089,
      "municipio" : "RMA",
      "nombre" : "Pilan"
    },
    {
      "lat" : 12.47642,
      "lng" : -84.50665,
      "municipio" : "RMA",
      "nombre" : "Poza Redonda"
    },
    {
      "lat" : 11.95111,
      "lng" : -84.12202,
      "municipio" : "RMA",
      "nombre" : "Pueblo Nuevo"
    },
    {
      "lat" : 12.44766,
      "lng" : -84.19532,
      "municipio" : "RMA",
      "nombre" : "Salto de la Cruz"
    },
    {
      "lat" : 12.54164,
      "lng" : -84.59615,
      "municipio" : "RMA",
      "nombre" : "Salto Grande"
    },
    {
      "lat" : 12.1566,
      "lng" : -84.21619,
      "municipio" : "RMA",
      "nombre" : "San Agustín"
    },
    {
      "lat" : 11.91585,
      "lng" : -84.18131,
      "municipio" : "RMA",
      "nombre" : "San Antonio del Pozol"
    },
    {
      "lat" : 12.18281,
      "lng" : -84.04536,
      "municipio" : "RMA",
      "nombre" : "San Brown"
    },
    {
      "lat" : 12.4587,
      "lng" : -84.24866,
      "municipio" : "RMA",
      "nombre" : "San Jerónimo"
    },
    {
      "lat" : 11.94538,
      "lng" : -84.25338,
      "municipio" : "RMA",
      "nombre" : "San Jerónimo (Río Plata)"
    },
    {
      "lat" : 12.03167,
      "lng" : -84.10231,
      "municipio" : "RMA",
      "nombre" : "San Luis"
    },
    {
      "lat" : 12.56282,
      "lng" : -84.50794,
      "municipio" : "RMA",
      "nombre" : "San Rafael"
    },
    {
      "lat" : 12.22408,
      "lng" : -84.03303,
      "municipio" : "RMA",
      "nombre" : "San Ramón"
    },
    {
      "lat" : 12.43132,
      "lng" : -84.15751,
      "municipio" : "RMA",
      "nombre" : "Santa  Rita"
    },
    {
      "lat" : 11.83162,
      "lng" : -84.16634,
      "municipio" : "RMA",
      "nombre" : "Santa Rita de Los Peñones"
    },
    {
      "lat" : 12.1753,
      "lng" : -84.19888,
      "municipio" : "RMA",
      "nombre" : "Santa Rosa"
    },
    {
      "lat" : 12.24096,
      "lng" : -84.01808,
      "municipio" : "RMA",
      "nombre" : "Son Cuan"
    },
    {
      "lat" : 12.12307,
      "lng" : -84.28824,
      "municipio" : "RMA",
      "nombre" : "Tatumbla"
    },
    {
      "lat" : 12.37519,
      "lng" : -84.45959,
      "municipio" : "RMA",
      "nombre" : "Tutuwaká"
    },
    {
      "lat" : 11.81968,
      "lng" : -84.0918,
      "municipio" : "RMA",
      "nombre" : "Villa Nueva"
    },
    {
      "lat" : 12.38414,
      "lng" : -84.31851,
      "municipio" : "RMA",
      "nombre" : "Wapi"
    },
    {
      "lat" : 12.22626,
      "lng" : -84.33961,
      "municipio" : "RMA",
      "nombre" : "Zaragoza"
    },
    {
      "lat" : 12.795,
      "lng" : -84.035,
      "municipio" : "TTG",
      "nombre" : "Aguas Honda"
    },
    {
      "lat" : 12.529141,
      "lng" : -84.43631,
      "municipio" : "TTG",
      "nombre" : "Bambú Piñol"
    },
    {
      "lat" : 12.8171,
      "lng" : -84.31023,
      "municipio" : "TTG",
      "nombre" : "Caño Azul"
    },
    {
      "lat" : 12.68311,
      "lng" : -84.23645,
      "municipio" : "TTG",
      "nombre" : "Chili Kreek"
    },
    {
      "lat" : 12.64678,
      "lng" : -84.50786,
      "municipio" : "TTG",
      "nombre" : "Divino Niño"
    },
    {
      "lat" : 12.81924,
      "lng" : -84.14849,
      "municipio" : "TTG",
      "nombre" : "El Bambú"
    },
    {
      "lat" : 12.65615,
      "lng" : -84.56161,
      "municipio" : "TTG",
      "nombre" : "El Cedro"
    },
    {
      "lat" : 12.60388,
      "lng" : -84.15737,
      "municipio" : "TTG",
      "nombre" : "El Espavel"
    },
    {
      "lat" : 12.795,
      "lng" : -84.095,
      "municipio" : "TTG",
      "nombre" : "El Lajero"
    },
    {
      "lat" : 12.57686,
      "lng" : -84.23207,
      "municipio" : "TTG",
      "nombre" : "EL Marrón"
    },
    {
      "lat" : 12.64351,
      "lng" : -84.02631,
      "municipio" : "TTG",
      "nombre" : "El Papel"
    },
    {
      "lat" : 12.9157,
      "lng" : -84.14256,
      "municipio" : "TTG",
      "nombre" : "El Paraíso"
    },
    {
      "lat" : 12.93282,
      "lng" : -84.3338,
      "municipio" : "TTG",
      "nombre" : "El Pavón"
    },
    {
      "lat" : 12.52783,
      "lng" : -84.48264,
      "municipio" : "TTG",
      "nombre" : "El Wavo"
    },
    {
      "lat" : 12.85051,
      "lng" : -84.1063,
      "municipio" : "TTG",
      "nombre" : "Good Living"
    },
    {
      "lat" : 12.51207,
      "lng" : -84.2792,
      "municipio" : "TTG",
      "nombre" : "Hierba Buena"
    },
    {
      "lat" : 12.8402,
      "lng" : -84.37974,
      "municipio" : "TTG",
      "nombre" : "Karahola"
    },
    {
      "lat" : 12.7328,
      "lng" : -84.072,
      "municipio" : "TTG",
      "nombre" : "Kasmiting"
    },
    {
      "lat" : 12.92451,
      "lng" : -83.9552,
      "municipio" : "TTG",
      "nombre" : "Kun Kun"
    },
    {
      "lat" : 12.70923,
      "lng" : -84.51273,
      "municipio" : "TTG",
      "nombre" : "La Guitarra"
    },
    {
      "lat" : 12.71568,
      "lng" : -84.20365,
      "municipio" : "TTG",
      "nombre" : "La Isla Kukarawala"
    },
    {
      "lat" : 12.50992,
      "lng" : -84.35396,
      "municipio" : "TTG",
      "nombre" : "La Paila"
    },
    {
      "lat" : 12.61115,
      "lng" : -84.57199,
      "municipio" : "TTG",
      "nombre" : "La Toalla"
    },
    {
      "lat" : 12.75871,
      "lng" : -84.42257,
      "municipio" : "TTG",
      "nombre" : "Mata de Caña"
    },
    {
      "lat" : 12.7591,
      "lng" : -84.2424,
      "municipio" : "TTG",
      "nombre" : "Nuevo Belén"
    },
    {
      "lat" : 12.94573,
      "lng" : -84.23284,
      "municipio" : "TTG",
      "nombre" : "Paharatigni"
    },
    {
      "lat" : 12.76693,
      "lng" : -84.19696,
      "municipio" : "TTG",
      "nombre" : "Salto de Busaya"
    },
    {
      "lat" : 12.64943,
      "lng" : -84.44639,
      "municipio" : "TTG",
      "nombre" : "San Antonio de Kukarawala"
    },
    {
      "lat" : 12.69659,
      "lng" : -84.13728,
      "municipio" : "TTG",
      "nombre" : "San Francisco de Suslatigni"
    },
    {
      "lat" : 12.95513,
      "lng" : -84.03518,
      "municipio" : "TTG",
      "nombre" : "San Francisco de Wawalatigni"
    },
    {
      "lat" : 12.62146,
      "lng" : -84.23869,
      "municipio" : "TTG",
      "nombre" : "San Isidro"
    },
    {
      "lat" : 12.65338,
      "lng" : -84.3002,
      "municipio" : "TTG",
      "nombre" : "San José de Sawawas"
    },
    {
      "lat" : 12.87753,
      "lng" : -84.03963,
      "municipio" : "TTG",
      "nombre" : "San Jose Kurinwas"
    },
    {
      "lat" : 12.68505,
      "lng" : -84.02322,
      "municipio" : "TTG",
      "nombre" : "San Juan de Chaca Chaca"
    },
    {
      "lat" : 12.8695,
      "lng" : -84.32198,
      "municipio" : "TTG",
      "nombre" : "San Juan de Kurinwas"
    },
    {
      "lat" : 12.70079,
      "lng" : -84.599,
      "municipio" : "TTG",
      "nombre" : "San Miguel Calzon Quemado"
    },
    {
      "lat" : 12.76969,
      "lng" : -84.1406,
      "municipio" : "TTG",
      "nombre" : "San Miguel de los Olivos"
    },
    {
      "lat" : 12.71231,
      "lng" : -84.42599,
      "municipio" : "TTG",
      "nombre" : "San Miguelito"
    },
    {
      "lat" : 12.6002,
      "lng" : -84.49898,
      "municipio" : "TTG",
      "nombre" : "San Rafael"
    },
    {
      "lat" : 12.71984,
      "lng" : -84.15378,
      "municipio" : "TTG",
      "nombre" : "Santa Lucía"
    },
    {
      "lat" : 12.63759,
      "lng" : -84.39193,
      "municipio" : "TTG",
      "nombre" : "Santa Rita"
    },
    {
      "lat" : 12.7108,
      "lng" : -84.0483,
      "municipio" : "TTG",
      "nombre" : "Santa Teresa"
    },
    {
      "lat" : 12.58938,
      "lng" : -84.25812,
      "municipio" : "TTG",
      "nombre" : "Sawawas Central"
    },
    {
      "lat" : 12.6967,
      "lng" : -84.0822,
      "municipio" : "TTG",
      "nombre" : "Suslatigni"
    },
    {
      "lat" : 12.57411,
      "lng" : -84.41977,
      "municipio" : "TTG",
      "nombre" : "Tintas Verde"
    },
    {
      "lat" : 12.65219,
      "lng" : -84.19843,
      "municipio" : "TTG",
      "nombre" : "Walpapine"
    },
    {
      "lat" : 12.73539,
      "lng" : -84.5466,
      "municipio" : "TTG",
      "nombre" : "Wasmuka"
    },
    {
      "lat" : 12.73899,
      "lng" : -84.30753,
      "municipio" : "TTG",
      "nombre" : "Waspado"
    },
    {
      "lat" : 12.91795,
      "lng" : -84.0662,
      "municipio" : "TTG",
      "nombre" : "Wawalatigni"
    },
    {
      "lat" : 12.81895,
      "lng" : -84.20132,
      "municipio" : "TTG",
      "nombre" : "El Tortuguero"
    },
    {
      "lat" : 12.27628,
      "lng" : -83.84712,
      "municipio" : "KHL",
      "nombre" : "Asentamiento Samuel Law"
    },
    {
      "lat" : 12.1128,
      "lng" : -83.9693,
      "municipio" : "KHL",
      "nombre" : "Belén"
    },
    {
      "lat" : 12.241114,
      "lng" : -83.79478,
      "municipio" : "KHL",
      "nombre" : "Big Lagoon"
    },
    {
      "lat" : 12.21516,
      "lng" : -84.09422,
      "municipio" : "KHL",
      "nombre" : "Chalmeca"
    },
    {
      "lat" : 12.2443,
      "lng" : -83.82498,
      "municipio" : "KHL",
      "nombre" : "El Campión"
    },
    {
      "lat" : 12.2715,
      "lng" : -83.793,
      "municipio" : "KHL",
      "nombre" : "El Capricho"
    },
    {
      "lat" : 12.46028,
      "lng" : -83.98367,
      "municipio" : "KHL",
      "nombre" : "El Diamante"
    },
    {
      "lat" : 12.2966,
      "lng" : -83.83165,
      "municipio" : "KHL",
      "nombre" : "El Escobal"
    },
    {
      "lat" : 12.31649,
      "lng" : -83.86758,
      "municipio" : "KHL",
      "nombre" : "El Panchón"
    },
    {
      "lat" : 12.49271,
      "lng" : -84.05645,
      "municipio" : "KHL",
      "nombre" : "El Porvenir"
    },
    {
      "lat" : 12.37177,
      "lng" : -83.89191,
      "municipio" : "KHL",
      "nombre" : "El Rosario"
    },
    {
      "lat" : 12.13861,
      "lng" : -83.93922,
      "municipio" : "KHL",
      "nombre" : "El Sílico"
    },
    {
      "lat" : 12.44742,
      "lng" : -84.07662,
      "municipio" : "KHL",
      "nombre" : "El Trapiche"
    },
    {
      "lat" : 12.2952,
      "lng" : -83.95985,
      "municipio" : "KHL",
      "nombre" : "El Wary"
    },
    {
      "lat" : 12.27859,
      "lng" : -83.84188,
      "municipio" : "KHL",
      "nombre" : "Flor de Pino"
    },
    {
      "lat" : 12.10412,
      "lng" : -83.99502,
      "municipio" : "KHL",
      "nombre" : "Home Creek"
    },
    {
      "lat" : 12.31683,
      "lng" : -83.80845,
      "municipio" : "KHL",
      "nombre" : "La Ceiba"
    },
    {
      "lat" : 12.2592,
      "lng" : -83.99119,
      "municipio" : "KHL",
      "nombre" : "La Fonseca"
    },
    {
      "lat" : 12.36232,
      "lng" : -84.05808,
      "municipio" : "KHL",
      "nombre" : "La Pichinga"
    },
    {
      "lat" : 12.51397,
      "lng" : -84.11086,
      "municipio" : "KHL",
      "nombre" : "La Unión"
    },
    {
      "lat" : 12.17475,
      "lng" : -83.99194,
      "municipio" : "KHL",
      "nombre" : "La Zompopa"
    },
    {
      "lat" : 12.29861,
      "lng" : -83.83572,
      "municipio" : "KHL",
      "nombre" : "Las Lapas"
    },
    {
      "lat" : 12.24454,
      "lng" : -83.84481,
      "municipio" : "KHL",
      "nombre" : "Las Limas"
    },
    {
      "lat" : 12.56266,
      "lng" : -84.08353,
      "municipio" : "KHL",
      "nombre" : "Las Maravillas"
    },
    {
      "lat" : 12.18316,
      "lng" : -83.83157,
      "municipio" : "KHL",
      "nombre" : "Loma de Mico"
    },
    {
      "lat" : 12.23565,
      "lng" : -83.7808,
      "municipio" : "KHL",
      "nombre" : "Los Angeles"
    },
    {
      "lat" : 12.29612,
      "lng" : -83.75777,
      "municipio" : "KHL",
      "nombre" : "Los Cinco"
    },
    {
      "lat" : 12.56606,
      "lng" : -84.11954,
      "municipio" : "KHL",
      "nombre" : "Luz de San Marcos"
    },
    {
      "lat" : 12.27896,
      "lng" : -83.73625,
      "municipio" : "KHL",
      "nombre" : "Manhattan"
    },
    {
      "lat" : 12.19993,
      "lng" : -83.97414,
      "municipio" : "KHL",
      "nombre" : "Neysi Ríos"
    },
    {
      "lat" : 12.41128,
      "lng" : -83.92941,
      "municipio" : "KHL",
      "nombre" : "Nueva Alianza"
    },
    {
      "lat" : 12.44155,
      "lng" : -84.03538,
      "municipio" : "KHL",
      "nombre" : "Nuevo Chontales"
    },
    {
      "lat" : 12.18294,
      "lng" : -84.04536,
      "municipio" : "KHL",
      "nombre" : "Salto Sam Brown"
    },
    {
      "lat" : 12.15528,
      "lng" : -83.97477,
      "municipio" : "KHL",
      "nombre" : "Sam Brown"
    },
    {
      "lat" : 12.52381,
      "lng" : -84.0152,
      "municipio" : "KHL",
      "nombre" : "San Pablo"
    },
    {
      "lat" : 12.23421,
      "lng" : -83.98717,
      "municipio" : "KHL",
      "nombre" : "San Ramón Nuevo"
    },
    {
      "lat" : 12.22409,
      "lng" : -84.03307,
      "municipio" : "KHL",
      "nombre" : "San Ramón Viejo"
    },
    {
      "lat" : 12.25607,
      "lng" : -83.8257,
      "municipio" : "KHL",
      "nombre" : "Santa Isabel"
    },
    {
      "lat" : 12.24096,
      "lng" : -84.01805,
      "municipio" : "KHL",
      "nombre" : "Son Cuan"
    },
    {
      "lat" : 13.02933,
      "lng" : -84.62172,
      "municipio" : "CRG",
      "nombre" : "Aguas Calientes"
    },
    {
      "lat" : 13.21786,
      "lng" : -84.01696,
      "municipio" : "CRG",
      "nombre" : "Anglo América"
    },
    {
      "lat" : 13.05084,
      "lng" : -84.47916,
      "municipio" : "CRG",
      "nombre" : "Apawas"
    },
    {
      "lat" : 13.24005,
      "lng" : -84.3874,
      "municipio" : "CRG",
      "nombre" : "Apawonta"
    },
    {
      "lat" : 13.06251,
      "lng" : -84.58569,
      "municipio" : "CRG",
      "nombre" : "Batitán"
    },
    {
      "lat" : 13.20373,
      "lng" : -84.0503,
      "municipio" : "CRG",
      "nombre" : "Betania"
    },
    {
      "lat" : 13.1415,
      "lng" : -84.7668,
      "municipio" : "CRG",
      "nombre" : "Betanis"
    },
    {
      "lat" : 13.1993,
      "lng" : -84.3669,
      "municipio" : "CRG",
      "nombre" : "Boca de Piedra"
    },
    {
      "lat" : 13.04351,
      "lng" : -84.30977,
      "municipio" : "CRG",
      "nombre" : "El Cañal"
    },
    {
      "lat" : 13.10409,
      "lng" : -84.23101,
      "municipio" : "CRG",
      "nombre" : "El Gallo"
    },
    {
      "lat" : 13.1769,
      "lng" : -84.7501,
      "municipio" : "CRG",
      "nombre" : "El Gamalote"
    },
    {
      "lat" : 13.12043,
      "lng" : -84.16369,
      "municipio" : "CRG",
      "nombre" : "El Guayabo"
    },
    {
      "lat" : 13.04704,
      "lng" : -84.72395,
      "municipio" : "CRG",
      "nombre" : "Estrella de la Vega del Río"
    },
    {
      "lat" : 13.02707,
      "lng" : -84.70063,
      "municipio" : "CRG",
      "nombre" : "Estrella Medalla Milagrosa"
    },
    {
      "lat" : 12.9464,
      "lng" : -84.64088,
      "municipio" : "CRG",
      "nombre" : "Feliciano"
    },
    {
      "lat" : 13.0916,
      "lng" : -84.575,
      "municipio" : "CRG",
      "nombre" : "Hachita"
    },
    {
      "lat" : 13.19772,
      "lng" : -84.08051,
      "municipio" : "CRG",
      "nombre" : "Kansas City"
    },
    {
      "lat" : 13.11498,
      "lng" : -84.214209,
      "municipio" : "CRG",
      "nombre" : "La Ceiba"
    },
    {
      "lat" : 12.96985,
      "lng" : -84.08048,
      "municipio" : "CRG",
      "nombre" : "La Concepción"
    },
    {
      "lat" : 12.89775,
      "lng" : -84.45237,
      "municipio" : "CRG",
      "nombre" : "La Palma"
    },
    {
      "lat" : 12.97337,
      "lng" : -84.18848,
      "municipio" : "CRG",
      "nombre" : "La Trinidad"
    },
    {
      "lat" : 13.22754,
      "lng" : -84.06983,
      "municipio" : "CRG",
      "nombre" : "Makantaka"
    },
    {
      "lat" : 13.24611,
      "lng" : -84.08692,
      "municipio" : "CRG",
      "nombre" : "Makantakita"
    },
    {
      "lat" : 13.12039,
      "lng" : -84.13213,
      "municipio" : "CRG",
      "nombre" : "Matagalpa"
    },
    {
      "lat" : 12.83111,
      "lng" : -84.58999,
      "municipio" : "CRG",
      "nombre" : "Mayawas"
    },
    {
      "lat" : 13.09419,
      "lng" : -84.25026,
      "municipio" : "CRG",
      "nombre" : "Muelle Real"
    },
    {
      "lat" : 13.07586,
      "lng" : -84.14623,
      "municipio" : "CRG",
      "nombre" : "Nueva Estrella"
    },
    {
      "lat" : 12.9023,
      "lng" : -84.519,
      "municipio" : "CRG",
      "nombre" : "Nuevo Amancecer"
    },
    {
      "lat" : 13.05292,
      "lng" : -84.2103,
      "municipio" : "CRG",
      "nombre" : "Nuevo San Antonio"
    },
    {
      "lat" : 13.04641,
      "lng" : -84.51685,
      "municipio" : "CRG",
      "nombre" : "Olea Olea"
    },
    {
      "lat" : 12.78077,
      "lng" : -84.60488,
      "municipio" : "CRG",
      "nombre" : "Oliwas"
    },
    {
      "lat" : 13.1506,
      "lng" : -84.5954,
      "municipio" : "CRG",
      "nombre" : "Poncaya"
    },
    {
      "lat" : 12.84741,
      "lng" : -84.49377,
      "municipio" : "CRG",
      "nombre" : "Río Silva"
    },
    {
      "lat" : 12.95721,
      "lng" : -84.54183,
      "municipio" : "CRG",
      "nombre" : "Sagrado Corazón"
    },
    {
      "lat" : 12.91372,
      "lng" : -84.68174,
      "municipio" : "CRG",
      "nombre" : "San Antonio"
    },
    {
      "lat" : 12.92584,
      "lng" : -84.53901,
      "municipio" : "CRG",
      "nombre" : "San Francisco Rancho Alegre"
    },
    {
      "lat" : 13.01593,
      "lng" : -84.13851,
      "municipio" : "CRG",
      "nombre" : "San José"
    },
    {
      "lat" : 12.8273,
      "lng" : -84.57138,
      "municipio" : "CRG",
      "nombre" : "San José del Arbolito"
    },
    {
      "lat" : 12.96057,
      "lng" : -84.47239,
      "municipio" : "CRG",
      "nombre" : "San Miguel Casa de Alto"
    },
    {
      "lat" : 13.2326,
      "lng" : -84.45061,
      "municipio" : "CRG",
      "nombre" : "San Miguel de la Esperanza"
    },
    {
      "lat" : 13.1897,
      "lng" : -84.5316,
      "municipio" : "CRG",
      "nombre" : "San Pablo Río 22"
    },
    {
      "lat" : 13.17146,
      "lng" : -84.20029,
      "municipio" : "CRG",
      "nombre" : "San Ramón"
    },
    {
      "lat" : 13.03166,
      "lng" : -84.19566,
      "municipio" : "CRG",
      "nombre" : "Santa Rita"
    },
    {
      "lat" : 13.19361,
      "lng" : -84.43925,
      "municipio" : "CRG",
      "nombre" : "Santo Domingo del Carmen"
    },
    {
      "lat" : 13.17525,
      "lng" : -84.13747,
      "municipio" : "CRG",
      "nombre" : "Siawas"
    },
    {
      "lat" : 13.07703,
      "lng" : -84.29511,
      "municipio" : "CRG",
      "nombre" : "Siksikwas"
    },
    {
      "lat" : 13.136,
      "lng" : -84.575,
      "municipio" : "CRG",
      "nombre" : "Tres Esquinas"
    },
    {
      "lat" : 13.00947,
      "lng" : -84.35085,
      "municipio" : "CRG",
      "nombre" : "Tumarin Indígena"
    },
    {
      "lat" : 12.98284,
      "lng" : -84.37826,
      "municipio" : "CRG",
      "nombre" : "Tumarin Mestizo"
    },
    {
      "lat" : 13.201,
      "lng" : -84.6398,
      "municipio" : "CRG",
      "nombre" : "Uliwas"
    },
    {
      "lat" : 13.1998,
      "lng" : -84.6585,
      "municipio" : "CRG",
      "nombre" : "Uliwasito"
    },
    {
      "lat" : 13.1174,
      "lng" : -84.15356,
      "municipio" : "CRG",
      "nombre" : "Walpa Daukra"
    },
    {
      "lat" : 13.11128,
      "lng" : -84.18681,
      "municipio" : "CRG",
      "nombre" : "La Cruz de Río Grande"
    },
    {
      "lat" : 12.426361,
      "lng" : -83.815694,
      "municipio" : "LAP",
      "nombre" : "Arenita # 3"
    },
    {
      "lat" : 12.37212,
      "lng" : -83.82999,
      "municipio" : "LAP",
      "nombre" : "Arenita Land Creak"
    },
    {
      "lat" : 12.3383,
      "lng" : -83.68948,
      "municipio" : "LAP",
      "nombre" : "Awas"
    },
    {
      "lat" : 12.55496,
      "lng" : -83.9552,
      "municipio" : "LAP",
      "nombre" : "Blue Lagoon"
    },
    {
      "lat" : 12.44843,
      "lng" : -83.73132,
      "municipio" : "LAP",
      "nombre" : "Brown Bank"
    },
    {
      "lat" : 12.77816,
      "lng" : -83.87741,
      "municipio" : "LAP",
      "nombre" : "Caño Wilson"
    },
    {
      "lat" : 12.68667,
      "lng" : -83.80833,
      "municipio" : "LAP",
      "nombre" : "Dachinal"
    },
    {
      "lat" : 12.643017,
      "lng" : -83.966317,
      "municipio" : "LAP",
      "nombre" : "El Castaño"
    },
    {
      "lat" : 12.6514,
      "lng" : -83.7669,
      "municipio" : "LAP",
      "nombre" : "El Cedro 1"
    },
    {
      "lat" : 12.67508,
      "lng" : -83.87403,
      "municipio" : "LAP",
      "nombre" : "El Cedro 2"
    },
    {
      "lat" : 12.56571,
      "lng" : -83.99266,
      "municipio" : "LAP",
      "nombre" : "El Fosforo"
    },
    {
      "lat" : 12.78129,
      "lng" : -83.9237,
      "municipio" : "LAP",
      "nombre" : "El Limon"
    },
    {
      "lat" : 12.81325,
      "lng" : -83.9627,
      "municipio" : "LAP",
      "nombre" : "El Mango"
    },
    {
      "lat" : 12.614583,
      "lng" : -84.018033,
      "municipio" : "LAP",
      "nombre" : "El Papelito"
    },
    {
      "lat" : 12.34929,
      "lng" : -83.79965,
      "municipio" : "LAP",
      "nombre" : "El Paraiso"
    },
    {
      "lat" : 12.49631,
      "lng" : -83.93964,
      "municipio" : "LAP",
      "nombre" : "El Pedregal"
    },
    {
      "lat" : 12.67883,
      "lng" : -83.955383,
      "municipio" : "LAP",
      "nombre" : "El Zapote"
    },
    {
      "lat" : 12.67868,
      "lng" : -83.79069,
      "municipio" : "LAP",
      "nombre" : "Fruta de Pan"
    },
    {
      "lat" : 12.33003,
      "lng" : -83.67381,
      "municipio" : "LAP",
      "nombre" : "Haulover"
    },
    {
      "lat" : 12.67598,
      "lng" : -83.73258,
      "municipio" : "LAP",
      "nombre" : "Kahka Creek"
    },
    {
      "lat" : 12.39695,
      "lng" : -83.72556,
      "municipio" : "LAP",
      "nombre" : "Kahkabila"
    },
    {
      "lat" : 12.649944,
      "lng" : -83.683611,
      "municipio" : "LAP",
      "nombre" : "La Batata"
    },
    {
      "lat" : 12.62795,
      "lng" : -83.953067,
      "municipio" : "LAP",
      "nombre" : "La Chiripa"
    },
    {
      "lat" : 12.48117,
      "lng" : -83.75277,
      "municipio" : "LAP",
      "nombre" : "La Fe"
    },
    {
      "lat" : 12.52711,
      "lng" : -83.96708,
      "municipio" : "LAP",
      "nombre" : "La Pachona/El Toronjal"
    },
    {
      "lat" : 12.73215,
      "lng" : -83.79065,
      "municipio" : "LAP",
      "nombre" : "La Patriota"
    },
    {
      "lat" : 12.63908,
      "lng" : -83.77522,
      "municipio" : "LAP",
      "nombre" : "La Quinta"
    },
    {
      "lat" : 12.73067,
      "lng" : -83.94311,
      "municipio" : "LAP",
      "nombre" : "La Tortuguita"
    },
    {
      "lat" : 12.52777,
      "lng" : -84.00892,
      "municipio" : "LAP",
      "nombre" : "Los Duartes"
    },
    {
      "lat" : 12.62258,
      "lng" : -83.75404,
      "municipio" : "LAP",
      "nombre" : "Los Laurales"
    },
    {
      "lat" : 12.65065,
      "lng" : -83.79192,
      "municipio" : "LAP",
      "nombre" : "Mahagany"
    },
    {
      "lat" : 12.56121,
      "lng" : -83.69122,
      "municipio" : "LAP",
      "nombre" : "Marshall Point"
    },
    {
      "lat" : 12.41211,
      "lng" : -83.92924,
      "municipio" : "LAP",
      "nombre" : "Nueva Alianza"
    },
    {
      "lat" : 12.53463,
      "lng" : -83.83318,
      "municipio" : "LAP",
      "nombre" : "Nueva Esperanza"
    },
    {
      "lat" : 12.55704,
      "lng" : -83.7142,
      "municipio" : "LAP",
      "nombre" : "Orinoco"
    },
    {
      "lat" : 12.68292,
      "lng" : -83.75983,
      "municipio" : "LAP",
      "nombre" : "Pihtutigni"
    },
    {
      "lat" : 12.4576,
      "lng" : -83.85705,
      "municipio" : "LAP",
      "nombre" : "Pondler"
    },
    {
      "lat" : 12.65792,
      "lng" : -83.74238,
      "municipio" : "LAP",
      "nombre" : "Pueblo Nuevo"
    },
    {
      "lat" : 12.731789,
      "lng" : -83.723656,
      "municipio" : "LAP",
      "nombre" : "Punta Cañon"
    },
    {
      "lat" : 12.76332,
      "lng" : -83.682515,
      "municipio" : "LAP",
      "nombre" : "Punta Fusil"
    },
    {
      "lat" : 12.34064,
      "lng" : -83.68552,
      "municipio" : "LAP",
      "nombre" : "Raitipura"
    },
    {
      "lat" : 12.31217,
      "lng" : -83.72896,
      "municipio" : "LAP",
      "nombre" : "Rocky Point"
    },
    {
      "lat" : 12.45968,
      "lng" : -83.9322,
      "municipio" : "LAP",
      "nombre" : "San Jose"
    },
    {
      "lat" : 12.51717,
      "lng" : -83.78001,
      "municipio" : "LAP",
      "nombre" : "San Vicente"
    },
    {
      "lat" : 12.594,
      "lng" : -83.8069,
      "municipio" : "LAP",
      "nombre" : "Santa Rita"
    },
    {
      "lat" : 12.69743,
      "lng" : -83.84077,
      "municipio" : "LAP",
      "nombre" : "Sawawas"
    },
    {
      "lat" : 12.45619,
      "lng" : -83.48686,
      "municipio" : "LAP",
      "nombre" : "Set Net Point"
    },
    {
      "lat" : 12.75857,
      "lng" : -83.73854,
      "municipio" : "LAP",
      "nombre" : "Sumi Lagoon"
    },
    {
      "lat" : 12.67281,
      "lng" : -83.54485,
      "municipio" : "LAP",
      "nombre" : "Tasbapounie"
    },
    {
      "lat" : 12.339405,
      "lng" : -83.670971,
      "municipio" : "LAP",
      "nombre" : "Laguna de Perlas"
    },
    {
      "lat" : 13.0231,
      "lng" : -84.7905,
      "municipio" : "PWA",
      "nombre" : "Aguacate"
    },
    {
      "lat" : 13.03173,
      "lng" : -84.93627,
      "municipio" : "PWA",
      "nombre" : "Banderita"
    },
    {
      "lat" : 13.04687,
      "lng" : -84.88869,
      "municipio" : "PWA",
      "nombre" : "Barrio Pobre"
    },
    {
      "lat" : 13.03610359738,
      "lng" : -84.8562379473838,
      "municipio" : "PWA",
      "nombre" : "Belén"
    },
    {
      "lat" : 12.97205,
      "lng" : -84.94809,
      "municipio" : "PWA",
      "nombre" : "Betania"
    },
    {
      "lat" : 12.9628,
      "lng" : -85.00193,
      "municipio" : "PWA",
      "nombre" : "Bilampi"
    },
    {
      "lat" : 12.75273,
      "lng" : -84.75315,
      "municipio" : "PWA",
      "nombre" : "Calderón"
    },
    {
      "lat" : 12.92915,
      "lng" : -84.981,
      "municipio" : "PWA",
      "nombre" : "Caño de Agua"
    },
    {
      "lat" : 12.98935,
      "lng" : -84.13355,
      "municipio" : "PWA",
      "nombre" : "Chorro de Agua"
    },
    {
      "lat" : 12.9328658902996,
      "lng" : -84.917368715662,
      "municipio" : "PWA",
      "nombre" : "Cooperativa San José"
    },
    {
      "lat" : 13.01174,
      "lng" : -85.09236,
      "municipio" : "PWA",
      "nombre" : "Cuatro Esquinas Las Lomas"
    },
    {
      "lat" : 12.85495,
      "lng" : -85.18152,
      "municipio" : "PWA",
      "nombre" : "David Tejada"
    },
    {
      "lat" : 12.79839,
      "lng" : -84.90983,
      "municipio" : "PWA",
      "nombre" : "El Achote"
    },
    {
      "lat" : 12.79617,
      "lng" : -85.13694,
      "municipio" : "PWA",
      "nombre" : "El Campo"
    },
    {
      "lat" : 12.98851,
      "lng" : -84.77064,
      "municipio" : "PWA",
      "nombre" : "El Negro"
    },
    {
      "lat" : 12.8700011167215,
      "lng" : -85.1561452618067,
      "municipio" : "PWA",
      "nombre" : "El Pavón"
    },
    {
      "lat" : 12.92966,
      "lng" : -85.0701,
      "municipio" : "PWA",
      "nombre" : "El Toro"
    },
    {
      "lat" : 12.82246,
      "lng" : -84.68266,
      "municipio" : "PWA",
      "nombre" : "Jorgito"
    },
    {
      "lat" : 13.10181,
      "lng" : -84.80391,
      "municipio" : "PWA",
      "nombre" : "Kaskita"
    },
    {
      "lat" : 13.07714,
      "lng" : -84.86021,
      "municipio" : "PWA",
      "nombre" : "Kepi"
    },
    {
      "lat" : 12.85752,
      "lng" : -85.04312,
      "municipio" : "PWA",
      "nombre" : "La Hermosa Malakawas"
    },
    {
      "lat" : 13.06407,
      "lng" : -85.08183,
      "municipio" : "PWA",
      "nombre" : "La Paila"
    },
    {
      "lat" : 12.95228,
      "lng" : -85.17662,
      "municipio" : "PWA",
      "nombre" : "La Pedrera"
    },
    {
      "lat" : 12.93335,
      "lng" : -85.13606,
      "municipio" : "PWA",
      "nombre" : "La Placa"
    },
    {
      "lat" : 12.78304,
      "lng" : -84.96301,
      "municipio" : "PWA",
      "nombre" : "La Toboba"
    },
    {
      "lat" : 12.89264,
      "lng" : -84.84047,
      "municipio" : "PWA",
      "nombre" : "Las Martinas"
    },
    {
      "lat" : 12.76263,
      "lng" : -84.89256,
      "municipio" : "PWA",
      "nombre" : "Las Minas"
    },
    {
      "lat" : 12.94664,
      "lng" : -85.08643,
      "municipio" : "PWA",
      "nombre" : "Los Alcantaras"
    },
    {
      "lat" : 12.82655,
      "lng" : -85.01868,
      "municipio" : "PWA",
      "nombre" : "Malakawas (Sector El Diamante)"
    },
    {
      "lat" : 12.8349613910386,
      "lng" : -85.0994582076154,
      "municipio" : "PWA",
      "nombre" : "Malakawas Asentamiento"
    },
    {
      "lat" : 12.7962,
      "lng" : -85.13693,
      "municipio" : "PWA",
      "nombre" : "Nuevo Amanecer"
    },
    {
      "lat" : 12.84951,
      "lng" : -84.89165,
      "municipio" : "PWA",
      "nombre" : "Okawas"
    },
    {
      "lat" : 12.86876,
      "lng" : -84.00738,
      "municipio" : "PWA",
      "nombre" : "Palsawas"
    },
    {
      "lat" : 12.99778,
      "lng" : -84.8612,
      "municipio" : "PWA",
      "nombre" : "Pedro Baca"
    },
    {
      "lat" : 12.90134,
      "lng" : -84.92845,
      "municipio" : "PWA",
      "nombre" : "Perro Mocho"
    },
    {
      "lat" : 12.82613,
      "lng" : -84.7688,
      "municipio" : "PWA",
      "nombre" : "Pueblo Nuevo-Las Delicias"
    },
    {
      "lat" : 12.94813,
      "lng" : -84.77958,
      "municipio" : "PWA",
      "nombre" : "Salto Grande"
    },
    {
      "lat" : 13.05441,
      "lng" : -84.73943,
      "municipio" : "PWA",
      "nombre" : "San Pedro del Norte"
    },
    {
      "lat" : 12.75957,
      "lng" : -84.80997,
      "municipio" : "PWA",
      "nombre" : "Santa Rosa"
    },
    {
      "lat" : 12.95159,
      "lng" : -84.93517,
      "municipio" : "PWA",
      "nombre" : "Ubú Norte"
    },
    {
      "lat" : 12.7381749896272,
      "lng" : -85.0116183253495,
      "municipio" : "PWA",
      "nombre" : "Villa Siquia"
    },
    {
      "lat" : 12.95228,
      "lng" : -85.17662,
      "municipio" : "PWA",
      "nombre" : "Wanawana"
    },
    {
      "lat" : 13.06144,
      "lng" : -85.00832,
      "municipio" : "PWA",
      "nombre" : "Wasayamba"
    },
    {
      "lat" : 12.95986,
      "lng" : -85.10547,
      "municipio" : "PWA",
      "nombre" : "Wilike Arriba"
    },
    {
      "lat" : 13.01277,
      "lng" : -85.12192,
      "municipio" : "PWA",
      "nombre" : "Wilikito"
    },
    {
      "lat" : 12.78856,
      "lng" : -85.12322,
      "municipio" : "PWA",
      "nombre" : "Bocana de Paiwas"
    },
    {
      "lat" : 12.01369469,
      "lng" : -83.76528123,
      "municipio" : "BEF",
      "nombre" : "Bluefields"
    },
    {
      "lat" : 12.16119206,
      "lng" : -84.21926208,
      "municipio" : "RMA",
      "nombre" : "El Rama"
    },
    {
      "lat" : 12.23853304,
      "lng" : -83.74701898,
      "municipio" : "KHL",
      "nombre" : "Kukra Hill"
    },
    {
      "lat" : 11.7227,  
      "lng" : -84.0332,
      "municipio" : "BEF",
      "nombre" : "Aguas Zarcas"
    }
]'''


comunidades = json.loads(json_com)

mun_shp = Path(__file__).resolve().parent / 'data' / 'lac_nic_l04_2006.SHP'

@transaction.atomic
def run(verbose=True):
  
  ds = DataSource(mun_shp)
  lyr = ds[0]
  count_mun = 0
  count_com = 0

  for feat in lyr:
    if feat.get('NAME2_') == 'Atlantico Sur':
      mpoly = GEOSGeometry(feat.geom.wkt)
      if mpoly.geom_type == 'Polygon':
        mpoly = MultiPolygon([mpoly])
      municipio = Municipio()
      nombre = feat.get('NAME1_')
      municipio.nombre = nombre if nombre != 'Kukrahill' else 'Kukra Hill'
      municipio.nombre_corto = codes[nombre]
      municipio.region = 'racs'
      municipio.area = feat.get('AREA_')
      municipio.mpoly = mpoly
      municipio.save()
      count_mun += 1

  print("Guardados: ",count_mun,"Municipios")

  for comu in comunidades:
    municipio = Municipio.objects.filter(nombre_corto=comu['municipio']).first()
    comunidad = Comunidad()
    comunidad.nombre = comu['nombre'].lower()
    comunidad.municipio = municipio
    comunidad.location = Point(comu['lng'],comu['lat'])
    comunidad.save()
    count_com += 1

  print("Guardadas: ",count_com,"Comunidades")
