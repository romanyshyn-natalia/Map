import folium
from parser import parse_file, convert_to_coordinates, neighbors


def create_map(dct, user_input):
    '''
    dict(), tuple -> ()
    Function for creating a map with all layers.
    '''
    map = folium.Map(location=user_input, zoom_start=3)
    tooltip = 'Click me!'

    fg1 = folium.FeatureGroup(name='Locations')
    fg2 = folium.FeatureGroup(name='Movies')
    fg3 = folium.FeatureGroup(name="Area")
    for key in dct:
        folium.Marker(user_input(), popup=key, tooltip=tooltip).add_to(map)
        fg1.add_child(folium.CircleMarker(location=[key[0], key[1]],
                                          radius=10,
                                          popup=key,
                                          color='red',
                                          fill_opacity=0.5))

        fg2.add_child(folium.Marker(location=[key[0], key[1]],
                                    popup=dct[key],
                                    icon=folium.Icon()))

        fg3.add_child(folium.GeoJson(data=open('world.json', 'r',
                                               encoding='utf-8-sig').read(),
                                     style_function=lambda x: {'fillColor': 'white'
                                     if x['properties']['AREA'] < 1000
                                     else 'blue' if 1000 <= x['properties']['AREA'] < 100000
                                     else 'green' if 100000 <= x['properties']['AREA'] < 1000000
                                     else 'purple'}))
    map.add_child(fg1)
    map.add_child(fg2)
    map.add_child(fg3)
    map.add_child(folium.LayerControl())
    map.save("Map_movies.html")


if __name__ == "__main__":
    year = input("Please enter a year you would like to have a map for: ")
    coordinates = input("Please enter your location (format: lat, long): ")
    coordinates = eval(coordinates)
    inf = convert_to_coordinates(parse_file(year))
    loc = neighbors(coordinates, inf)
    create_map(loc, coordinates)
