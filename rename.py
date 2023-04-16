import os

# I downloaded the world flags from this great source
# https://www.welt-flaggen.de/herunterladen/bilder
# They were named after the country code, so I had to rename them
# I used ChatGPT to generate the file names list below
# It skipped a few countries (Palestine, Taiwan, etc.) so I renamed them manually


file_names = {
    "ad": "Andorra",
    "ae": "Vereinigte Arabische Emirate",
    "af": "Afghanistan",
    "ag": "Antigua und Barbuda",
    "ai": "Anguilla",
    "al": "Albanien",
    "am": "Armenien",
    "ao": "Angola",
    "aq": "Antarktis",
    "ar": "Argentinien",
    "as": "Amerikanisch-Samoa",
    "at": "Österreich",
    "au": "Australien",
    "aw": "Aruba",
    "ax": "Åland-Inseln",
    "az": "Aserbaidschan",
    "ba": "Bosnien und Herzegowina",
    "bb": "Barbados",
    "bd": "Bangladesch",
    "be": "Belgien",
    "bf": "Burkina Faso",
    "bg": "Bulgarien",
    "bh": "Bahrain",
    "bi": "Burundi",
    "bj": "Benin",
    "bl": "St. Barthélemy",
    "bm": "Bermuda",
    "bn": "Brunei Darussalam",
    "bo": "Bolivien",
    "bq": "Bonaire, Sint Eustatius und Saba",
    "br": "Brasilien",
    "bs": "Bahamas",
    "bt": "Bhutan",
    "bv": "Bouvetinsel",
    "bw": "Botswana",
    "by": "Weißrussland",
    "bz": "Belize",
    "ca": "Kanada",
    "cc": "Kokosinseln",
    "cd": "Kongo (Demokratische Republik)",
    "cf": "Zentralafrikanische Republik",
    "cg": "Kongo",
    "ch": "Schweiz",
    "ci": "Elfenbeinküste",
    "ck": "Cookinseln",
    "cl": "Chile",
    "cm": "Kamerun",
    "cn": "China",
    "co": "Kolumbien",
    "cr": "Costa Rica",
    "cu": "Kuba",
    "cv": "Kap Verde",
    "cw": "Curaçao",
    "cx": "Weihnachtsinsel",
    "cy": "Zypern",
    "cz": "Tschechien",
    "de": "Deutschland",
    "dj": "Dschibuti",
    "dk": "Dänemark",
    "dm": "Dominica",
    "do": "Dominikanische Republik",
    "dz": "Algerien",
    "ec": "Ecuador",
    "ee": "Estland",
    "eg": "Ägypten",
    "eh": "Westsahara",
    "er": "Eritrea",
    "es": "Spanien",
    "et": "Äthiopien",
    "fi": "Finnland",
    "fj": "Fidschi",
    "fk": "Falklandinseln",
    "fm": "Mikronesien",
    "fo": "Färöer",
    "fj": "Fidschi",
    "fi": "Finnland",
    "fr": "Frankreich",
    "gf": "Französisch-Guayana",
    "pf": "Französisch-Polynesien",
    "tf": "Französische Süd- und Antarktisgebiete",
    "ga": "Gabun",
    "gm": "Gambia",
    "ge": "Georgien",
    "gh": "Ghana",
    "gi": "Gibraltar",
    "gd": "Grenada",
    "gr": "Griechenland",
    "gl": "Grönland",
    "gp": "Guadeloupe",
    "gu": "Guam",
    "gt": "Guatemala",
    "gg": "Guernsey",
    "gn": "Guinea",
    "gw": "Guinea-Bissau",
    "gy": "Guyana",
    "ht": "Haiti",
    "hm": "Heard- und McDonald-Inseln",
    "hn": "Honduras",
    "hk": "Hongkong",
    "in": "Indien",
    "id": "Indonesien",
    "ir": "Iran",
    "iq": "Irak",
    "ie": "Irland",
    "im": "Isle of Man",
    "is": "Island",
    "il": "Israel",
    "it": "Italien",
    "jm": "Jamaika",
    "jp": "Japan",
    "ye": "Jemen",
    "je": "Jersey",
    "jo": "Jordanien",
    "ky": "Kaimaninseln",
    "kh": "Kambodscha",
    "cm": "Kamerun",
    "ca": "Kanada",
    "cv": "Kap Verde",
    "kz": "Kasachstan",
    "qa": "Katar",
    "ke": "Kenia",
    "kg": "Kirgisistan",
    "ki": "Kiribati",
    "cc": "Kokosinseln",
    "co": "Kolumbien",
    "km": "Komoren",
    "cd": "Kongo (Dem. Rep.)",
    "cg": "Kongo (Rep.)",
    "kp": "Korea (Nord)",
    "kr": "Korea (Süd)",
    "hr": "Kroatien",
    "cu": "Kuba",
    "kw": "Kuwait",
    "la": "Laos",
    "ls": "Lesotho",
    "lv": "Lettland",
    "lb": "Libanon",
    "lr": "Liberia",
    "ly": "Libyen",
    "li": "Liechtenstein",
    "lt": "Litauen",
    "lu": "Luxemburg",
    "mo": "Macao",
    "mg": "Madagaskar",
    "mw": "Malawi",
    "my": "Malaysia",
    "mv": "Malediven",
    "ml": "Mali",
    "mt": "Malta",
    "ma": "Marokko",
    "mh": "Marshallinseln",
    "mq": "Martinique",
    "mr": "Mauretanien",
    'mu': 'Mauritius',
    'yt': 'Mayotte',
    'mx': 'Mexiko',
    'fm': 'Mikronesien',
    'md': 'Moldawien',
    'mc': 'Monaco',
    'mn': 'Mongolei',
    'me': 'Montenegro',
    'ms': 'Montserrat',
    'mz': 'Mosambik',
    'mm': 'Myanmar',
    'na': 'Namibia',
    'nr': 'Nauru',
    'np': 'Nepal',
    'nc': 'Neukaledonien',
    'nz': 'Neuseeland',
    'ni': 'Nicaragua',
    'ne': 'Niger',
    'ng': 'Nigeria',
    'nu': 'Niue',
    'mp': 'Nördliche Marianen',
    'kp': 'Nordkorea',
    'no': 'Norwegen',
    'om': 'Oman',
    'at': 'Österreich',
    'tl': 'Osttimor',
    'pk': 'Pakistan',
    'pw': 'Palau',
    'pa': 'Panama',
    'pg': 'Papua-Neuguinea',
    'py': 'Paraguay',
    'pe': 'Peru',
    'ph': 'Philippinen',
    'pn': 'Pitcairninseln',
    'pl': 'Polen',
    'pt': 'Portugal',
    'pr': 'Puerto Rico',
    're': 'Réunion',
    'rw': 'Ruanda',
    'ro': 'Rumänien',
    'ru': 'Russland',
    'sb': 'Salomonen',
    'zm': 'Sambia',
    'ws': 'Samoa',
    'sm': 'San Marino',
    'st': 'São Tomé und Príncipe',
    'sa': 'Saudi-Arabien',
    'se': 'Schweden',
    'ch': 'Schweiz',
    'sn': 'Senegal',
    'rs': 'Serbien',
    'sc': 'Seychellen',
    'sl': 'Sierra Leone',
    'zw': 'Simbabwe',
    'sg': 'Singapur',
    'sx': 'Sint Maarten',
    'sk': 'Slowakei',
    'si': 'Slowenien',
    'so': 'Somalia',
    'es': 'Spanien',
    'lk': 'Sri Lanka',
    'bl': 'St. Barthélemy',
    'sh': 'St. Helena',
    'kn': 'St. Kitts und Nevis',
    'lc': 'St. Lucia',
    'mf': 'St. Martin',
    'pm': 'St. Pierre und Miquelon',
    'vc': 'St. Vincent und die Grenadinen',
    'za': 'Südafrika',
    'sd': 'Sudan',
    'gs': 'Südgeorgien und die Südlichen Sandwichinseln',
    'kr': 'Südkorea',
    'ss': 'Südsudan',
    'sr': 'Suriname',
    'sj': 'Svalbard und Jan Mayen',
    'sz': 'Swasiland',
    'sy': 'Syrien',
    'tj': 'Tadschikistan',
    "tz": "Tansania",
    "th": "Thailand",
    "tl": "Timor-Leste",
    "tg": "Togo",
    "tk": "Tokelau",
    "to": "Tonga",
    "tt": "Trinidad und Tobago",
    "td": "Tschad",
    "cz": "Tschechien",
    "tn": "Tunesien",
    "tr": "Türkei",
    "tm": "Turkmenistan",
    "tc": "Turks- und Caicosinseln",
    "tv": "Tuvalu",
    "ug": "Uganda",
    "ua": "Ukraine",
    "hu": "Ungarn",
    "uy": "Uruguay",
    "uz": "Usbekistan",
    "vu": "Vanuatu",
    "va": "Vatikanstadt",
    "ve": "Venezuela",
    "ae": "Vereinigte Arabische Emirate",
    "us": "Vereinigte Staaten von Amerika",
    "gb": "Vereinigtes Königreich",
    "vn": "Vietnam",
    "wf": "Wallis und Futuna",
    "cx": "Weihnachtsinsel",
    "eh": "Westsahara",
    "cf": "Zentralafrikanische Republik",
    "cy": "Zypern"
}

# Directory where the files to be renamed are stored
directory = "images/h160"

# Iterate over all files in the directory
for filename in os.listdir(directory):
    # Get the full path of the file
    file_path = os.path.join(directory, filename)

    # Split the filename and extension
    filename, extension = os.path.splitext(filename)

    # Check if the file is in the dictionary of old and new names
    if filename in file_names:
        # Get the new file name from the dictionary
        new_file_name = file_names[filename]
        # Rename the file
        os.rename(file_path, os.path.join(directory, new_file_name + extension))
        print("Renamed " + filename + " to " + new_file_name)