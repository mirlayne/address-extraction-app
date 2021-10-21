'''
Class corresponding to getAuthorities function in support.py module
'''


class GetAuthorities:
    # Dictionary mit allen Denkmalschutzbehörden erstellen
    # aus:
    # https://www.berlin.de/sen/kulteu/denkmal/organisation-des-denkmalschutzes/untere-denkmalschutzbehoerden/
    # https://www.berlin.de/sen/kulteu/denkmal/organisation-des-denkmalschutzes/landesdenkmalrat/
    # https://www.berlin.de/landesdenkmalamt/

    # Form ist Bezirk:Adresse

    @staticmethod
    def get_authorities(self):
        return {'Charlottenburg-Wilmersdorf': 'Hohenzollerndamm 174',
                'Friedrichshain-Kreuzberg': 'Yorckstrasse 4',
                'Lichtenberg': 'Alt-Friedrichsfelde 60',
                'Marzahn-Hellersdorf': 'Helene-Weigel-Platz 8',
                'Mitte': 'Müllerstrasse 146',
                'Neukölln': 'Karl-Marx-Strasse 83',
                'Pankow': 'Storkower Strasse 97',
                'Reinickendorf': 'Eichborndamm 215',
                'Spandau': 'Carl-Schurz-Strasse 2',
                'Steglitz-Zehlendorf': 'Kirchstrasse 1',
                'Tempelhof-Schöneberg': 'John-F-Kennedy-Platz',
                'Treptow-Köpenick': 'Alt-Köpenick 21',
                'Oberste Denkmalschutzbehörde': 'Brunnenstrasse 188-190',  # TODO: Ask for this
                'Oberste Denkmalschutzbehörde': 'Behrenstrasse 42',
                'Landesdenkmalamt': 'Klosterstrasse 47',
                'Senatsverwaltung für Stadtentwicklung und Wohnen': 'Württembergische Strasse 6'
                }
