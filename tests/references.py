### Joe Doe - astro.com reference
# born on Tu., 27 February 1990
# in Izmir, TUR, 27e09, 38n25
# Time 9:15 a.m.
# Univ.Time 7:15

from datetime import datetime

BIRTH_DATE = datetime(1990, 2, 27, 7, 15)
BIRTH_LOCATION = (27.09, 38.25)
BIRTH_LOCATION_DETAILED = (27.150, 38.4167)

# Planet data: Planet, Sign, Longitude, House, Speed, Latitude, Declination
# 'sign' anahtarı, testlerin doğru çalışması için eklenmiştir.
PLANETS = {
    'Sun': {
        'sign': 'Pisces',
        'longitude': '8°26\'3"',
        'house': 11,
        'speed': '1°0\'18"',
        'latitude': '0°0\'0"',
        'declination': '8°24\'30"S'
    },
    'Moon': {
        'sign': 'Aries',
        'longitude': '4°13\'13"',
        'house': 12,
        'speed': '14°31\'46"',
        'latitude': '3°53\'7"',
        'declination': '5°14\'33"N'
    },
    'Mercury': {
        'sign': 'Aquarius',
        'longitude': '22°41\'34"',
        'house': 11,
        'speed': '1°37\'1"',
        'latitude': '2°2\'16"S',
        'declination': '15°52\'41"S'
    },
    'Venus': {
        'sign': 'Capricorn',
        'longitude': '27°8\'57"',
        'house': 10,
        'speed': '35\'46"',
        'latitude': '5°16\'34"N',
        'declination': '15°33\'11"S'
    },
    'Mars': {
        'sign': 'Capricorn',
        'longitude': '20°53\'21"',
        'house': 9,
        'speed': '44\'5"',
        'latitude': '0°44\'5"S',
        'declination': '22°32\'44"S'
    },
    'Jupiter': {
        'sign': 'Cancer',
        'longitude': '0°49\'7"',
        'house': 3,
        'speed': '30"',
        'latitude': '0°0\'57"N',
        'declination': '23°27\'21"N'
    },
    'Saturn': {
        'sign': 'Capricorn',
        'longitude': '21°57\'34"',
        'house': 10,
        'speed': '5\'36"',
        'latitude': '0°13\'58"N',
        'declination': '21°25\'20"S'
    },
    'Uranus': {
        'sign': 'Capricorn',
        'longitude': '8°42\'55"',
        'house': 9,
        'speed': '2\'13"',
        'latitude': '0°17\'5"S',
        'declination': '23°26\'25"S'
    },
    'Neptune': {
        'sign': 'Capricorn',
        'longitude': '13°56\'53"',
        'house': 9,
        'speed': '1\'30"',
        'latitude': '0°50\'59"N',
        'declination': '21°52\'0"S'
    },
    'Pluto': {
        'sign': 'Scorpio',
        'longitude': '17°46\'5"',
        'house': 7,
        'speed': '-17"',
        'latitude': '15°42\'59"N',
        'declination': '2°0\'28"S'
    },
    'Mean Node': {
        'sign': 'Aquarius',
        'longitude': '15°25\'39"',
        'house': 10,
        'speed': '-3\'11"',
        'latitude': '0°0\'0"',
        'declination': '16°12\'45"S'
    },
    'True Node': {
        'sign': 'Aquarius',
        'longitude': '16°23\'26"',
        'house': 11,
        'speed': '-3\'7"',
        'latitude': '0°0\'0"',
        'declination': '15°55\'34"S'
    },
    'Chiron': {
        'sign': 'Cancer',
        'longitude': '10°45\'34"',
        'house': 3,
        'speed': '-1\'26"',
        'latitude': '7°4\'26"S',
        'declination': '15°57\'16"N'
    }
}

# Houses data: House, Sign, Longitude, Declination
HOUSES = {
    1: {
        'sign': 'Taurus',
        'longitude': '6°6\'37"',
        'declination': '13°33\'35"N'
    },
    2: {
        'sign': 'Gemini',
        'longitude': '6°42\'16"',
        'declination': '21°25\'55"N'
    },
    3: {
        'sign': 'Gemini',
        'longitude': '29°30\'52"',
        'declination': '23°26\'30"N'
    },
    4: {
        'sign': 'Cancer',
        'longitude': '21°3\'30"',
        'declination': '21°47\'36"N'
    },
    5: {
        'sign': 'Leo',
        'longitude': '15°54\'13"',
        'declination': '16°4\'17"N'
    },
    6: {
        'sign': 'Virgo',
        'longitude': '19°47\'58"',
        'declination': '4°2\'24"N'
    },
    7: {
        'sign': 'Scorpio',
        'longitude': '6°6\'37"',
        'declination': '13°33\'35"S'
    },
    8: {
        'sign': 'Sagittarius',
        'longitude': '6°42\'16"',
        'declination': '21°25\'55"S'
    },
    9: {
        'sign': 'Sagittarius',
        'longitude': '29°30\'52"',
        'declination': '23°26\'30"S'
    },
    10: {
        'sign': 'Capricorn',
        'longitude': '21°3\'30"',
        'declination': '21°47\'36"S'
    },
    11: {
        'sign': 'Aquarius',
        'longitude': '15°54\'13"',
        'declination': '16°4\'17"S'
    },
    12: {
        'sign': 'Pisces',
        'longitude': '19°47\'58"',
        'declination': '4°2\'24"S'
    }
}

# Element and modality distributions (Bu bölüm 'sign' verisini çıkarmak için kullanıldı)
DISTRIBUTIONS = {
    'Fire': {
        'Cardinal': ['Moon'],
        'Fixed': [],
        'Mutable': []
    },
    'Earth': {
        'Cardinal': ['Venus', 'Mars', 'Saturn', 'Uranus', 'Neptune', 'MC'],
        'Fixed': ['AC'],
        'Mutable': []
    },
    'Air': {
        'Cardinal': [],
        'Fixed': ['Mercury', 'True Node'],
        'Mutable': []
    },
    'Water': {
        'Cardinal': ['Jupiter', 'Chiron'],
        'Fixed': ['Pluto'],
        'Mutable': ['Sun']
    }
}

# Aspects data: (Planet1, Planet2): 'Aspect Type Orb'
ASPECTS = {
    # Sun aspects
    ('Mars', 'Sun'): {'type': 'Semisquare', 'orb': '2°33s'},
    ('Jupiter', 'Sun'): {'type': 'Trine', 'orb': '-7°37s'},
    ('Saturn', 'Sun'): {'type': 'Semisquare', 'orb': '1°28s'},
    ('Uranus', 'Sun'): {'type': 'Sextile', 'orb': '-0°17a'},
    ('Neptune', 'Sun'): {'type': 'Sextile', 'orb': '-5°31a'},
    ('Pluto', 'Sun'): {'type': 'Trine', 'orb': '-9°20a'},
    ('Chiron', 'Sun'): {'type': 'Trine', 'orb': '2°20a'},
    ('AC', 'Sun'): {'type': 'Sextile', 'orb': '-2°20a'},
    ('MC', 'Sun'): {'type': 'Semisquare', 'orb': '2°23a'},

    # Moon aspects
    ('Mars', 'Moon'): {'type': 'Quintile', 'orb': '1°20s'},
    ('Jupiter', 'Moon'): {'type': 'Square', 'orb': '-3°24s'},
    ('Saturn', 'Moon'): {'type': 'Quintile', 'orb': '0°16s'},
    ('Uranus', 'Moon'): {'type': 'Square', 'orb': '-4°30a'},
    ('Neptune', 'Moon'): {'type': 'Square', 'orb': '-9°44a'},
    ('Pluto', 'Moon'): {'type': 'Sesquiquadrate', 'orb': '1°27s'},
    ('Chiron', 'Moon'): {'type': 'Square', 'orb': '6°32a'},
    ('AC', 'Moon'): {'type': 'Semisextile', 'orb': '1°53s'},
    ('MC', 'Moon'): {'type': 'Quintile', 'orb': '1°10a'},

    # Mercury aspects
    ('Mars', 'Mercury'): {'type': 'Semisextile', 'orb': '1°48s'},
    ('Jupiter', 'Mercury'): {'type': 'Trine', 'orb': '8°08a'},
    ('Saturn', 'Mercury'): {'type': 'Semisextile', 'orb': '0°44s'},
    ('Uranus', 'Mercury'): {'type': 'Semisquare', 'orb': '-1°01a'},
    ('Pluto', 'Mercury'): {'type': 'Square', 'orb': '4°55s'},
    ('AC', 'Mercury'): {'type': 'Quintile', 'orb': '1°25s'},
    ('MC', 'Mercury'): {'type': 'Semisextile', 'orb': '1°38a'},

    # Venus aspects
    ('Mars', 'Venus'): {'type': 'Conjunction', 'orb': '6°16a'},
    ('Saturn', 'Venus'): {'type': 'Conjunction', 'orb': '5°11s'},
    ('AC', 'Venus'): {'type': 'Square', 'orb': '8°58s'},
    ('MC', 'Venus'): {'type': 'Conjunction', 'orb': '6°05a'},

    # Mars aspects
    ('Saturn', 'Mars'): {'type': 'Conjunction', 'orb': '1°04a'},
    ('Neptune', 'Mars'): {'type': 'Conjunction', 'orb': '6°56s'},
    ('Pluto', 'Mars'): {'type': 'Sextile', 'orb': '3°07s'},
    ('MC', 'Mars'): {'type': 'Conjunction', 'orb': '0°10s'},

    # Jupiter aspects
    ('Uranus', 'Jupiter'): {'type': 'Opposition', 'orb': '-7°54s'},
    ('Pluto', 'Jupiter'): {'type': 'Sesquiquadrate', 'orb': '1°57a'},
    ('True Node', 'Jupiter'): {'type': 'Sesquiquadrate', 'orb': '-0°34a'},
    ('Chiron', 'Jupiter'): {'type': 'Conjunction', 'orb': '9°56a'},
    ('AC', 'Jupiter'): {'type': 'Sextile', 'orb': '-5°18s'},

    # Saturn aspects
    ('Neptune', 'Saturn'): {'type': 'Conjunction', 'orb': '8°01s'},
    ('Pluto', 'Saturn'): {'type': 'Sextile', 'orb': '4°11s'},
    ('MC', 'Saturn'): {'type': 'Conjunction', 'orb': '0°54a'},

    # Uranus aspects
    ('Neptune', 'Uranus'): {'type': 'Conjunction', 'orb': '5°14a'},
    ('Chiron', 'Uranus'): {'type': 'Opposition', 'orb': '-2°03a'},
    ('AC', 'Uranus'): {'type': 'Trine', 'orb': '-2°36a'},

    # Neptune aspects
    ('Pluto', 'Neptune'): {'type': 'Sextile', 'orb': '-3°49a'},
    ('Chiron', 'Neptune'): {'type': 'Opposition', 'orb': '-3°11s'},
    ('AC', 'Neptune'): {'type': 'Trine', 'orb': '-7°50a'},
    ('MC', 'Neptune'): {'type': 'Conjunction', 'orb': '7°07s'},

    # Pluto aspects
    ('True Node', 'Pluto'): {'type': 'Square', 'orb': '-1°23s'},
    ('Chiron', 'Pluto'): {'type': 'Trine', 'orb': '7°01s'},
    ('MC', 'Pluto'): {'type': 'Sextile', 'orb': '3°17s'},

    # True Node aspects
    ('Chiron', 'True Node'): {'type': 'Biquintile', 'orb': '0°22s'},

    # Chiron aspects
    ('AC', 'Chiron'): {'type': 'Sextile', 'orb': '4°39a'}
}
