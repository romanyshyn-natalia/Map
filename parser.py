from geopy.geocoders import Nominatim
from geopy.geocoders import Bing


def parse_file(year):
    '''
    int -> dict
    Function for reading and parsing a file.
    location - key, name of film - value
    >>> print(parse_file(2015))
    {'Burrard Civic Marina - 1655 Whyte Ave Vancouver British Columbia Canada': '"The Romeo Section" ', 
    'Clark Dr. & E 6th Ave. Mount Pleasant Vancouver British Columbia Canada': '"The Romeo Section" ', 
    'Jericho Beach Vancouver British Columbia Canada': '"The Romeo Section" '}
    '''
    dict_films = {}
    with open("locations.csv", "r") as f:
        data = [line.strip().split(",") for line in f.readlines() if "NO DATA" not in line and "add_info" not in line]
    for line in data:
        if str(year) == line[1]:
            if line[0] not in dict_films:
                dict_films[line[3]] = line[0]
    return dict_films


def convert_to_coordinates(dictionary):
    '''
    dict -> dict
    Function for converting string locations name to latitude and longitude of place, 
    where film was taken. Sorted for choosing only 10 nearest to the user points.


    >>> print(convert_to_coordinates({'Masai Mara Kenya': '"Yabanci: Hayati Kesfet" ', 
    'Serengeti National Park Tanzania': '"Yabanci: Hayati Kesfet" ', 
    'Amboseli National Park Kenya': '"Yabanci: Hayati Kesfet" ', 
    'Volcanoes National Park Rwanda': '"Yabanci: Hayati Kesfet" ', 
    'Lake Nakuru National Park Kenya': '"Yabanci: Hayati Kesfet" ', 
    'Akagera National Park Rwanda': '"Yabanci: Hayati Kesfet" ', 
    'Zanzibar Tanzania': '"Yabanci: Hayati Kesfet" ', 
    'Natural History Museum South Kensington London England UK': '"You_ Me and the Apocalypse" ', 
    'Minerals Gallery Natural History Museum London England UK': '"You_ Me and the Apocalypse" ', 
    'Mammals Gallery Natural History Museum London England UK': '"You_ Me and the Apocalypse" '}))

    {(-6.176829814910889, 39.223941802978516): '"Yabanci: Hayati Kesfet" ', 
    (-2.9072399139404297, 35.137760162353516): '"Yabanci: Hayati Kesfet" ', 
    (-2.6373651027679443, 37.24018859863281): '"Yabanci: Hayati Kesfet" ', 
    (-1.5808900594711304, 30.614669799804688): '"Yabanci: Hayati Kesfet" ', 
    (-1.5209300518035889, 35.337520599365234): '"Yabanci: Hayati Kesfet" ', 
    (-1.484179973602295, 29.507986068725586): '"Yabanci: Hayati Kesfet" ', 
    (-0.3076300024986267, 36.08195114135742): '"Yabanci: Hayati Kesfet" ', 
    (51.44438, -0.08782): '"You_ Me and the Apocalypse" ', 
    (51.498069763183594, -0.17406000196933746): '"You_ Me and the Apocalypse" '}
    '''
    dict_coordinates = {}
    geolocator = Bing(
        "AomOhTUAKsV-5fu4bzeuBtVlx5VeMi_M86P4gODXuCd6f7S2dquidP7Aj2xtDoS0")
    for key in dictionary:
        point = dictionary[key]
        try:
            latitude, longitude = geolocator.geocode(key, timeout=60)
            location = [latitude, longitude][1]
            dict_coordinates[location] = point
        except TypeError:
            continue
        except KeyError:
            continue
    return dict(sorted(dict_coordinates.items()))


def neighbors(coordinates, dct):
    '''
    tuple(), dict() -> dict()
    Function for finding the nearest locations to given.
    >>> print(neighbors((-6.176829814910889, 39.223941802978516), 
    {(-6.176829814910889, 39.223941802978516): '"Yabanci: Hayati Kesfet" ', 
    (-2.9072399139404297, 35.137760162353516): '"Yabanci: Hayati Kesfet" ', 
    (-2.6373651027679443, 37.24018859863281): '"Yabanci: Hayati Kesfet" ', 
    (-1.5808900594711304, 30.614669799804688): '"Yabanci: Hayati Kesfet" ', 
    (-1.5209300518035889, 35.337520599365234): '"Yabanci: Hayati Kesfet" ', 
    (-1.484179973602295, 29.507986068725586): '"Yabanci: Hayati Kesfet" ', 
    (-0.3076300024986267, 36.08195114135742): '"Yabanci: Hayati Kesfet" ', 
    (51.44438, -0.08782): '"You_ Me and the Apocalypse" ', 
    (51.498069763183594, -0.17406000196933746): '"You_ Me and the Apocalypse" '}))
    {(-6.176829814910889, 39.223941802978516): '"Yabanci: Hayati Kesfet" '}
    '''
    places = {}
    st = set()
    for key in dct:
        place = dct[key]
        try:
            if len(places) < 10:
                if place not in st:
                    st.add(place)
            if coordinates[0] - 1 <= key[0] <= coordinates[0] + 1 and \
                    coordinates[1] - 1 <= key[1] <= coordinates[1] + 1:
                places[key[0], key[1]] = place
            else:
                break
        except AttributeError:
            continue
        except ValueError:
            continue
    return places
