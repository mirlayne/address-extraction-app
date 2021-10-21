'''
Module corresponding to extractAdress.py from https://github.com/cfillies/semkibardoc
'''
import re

import numpy as np
from pymongo.collection import Collection
from spellchecker import SpellChecker

import schluesselregex as rex


class AddressExtraction:
    def find_addresses(self, col: Collection, supcol: Collection, lan: str):
        sup: dict = supcol.find_one()  # TODO: ask for this variable because it always retrieves the first element
                                        # in the collection and update it in line 43
        slist: list[str] = sup["streetnames"]

        slist = [s.lower() for s in slist]

        sp = self.get_spellcheck(lan, slist)
        # changes = []

        nlist = []
        xlist = []
        dlist = col.find()
        # for doc in col.find():
        #     dlist.append(doc)
        adcache = sup["adcache"]
        i = 0
        for doc in dlist:
            i = i + 1
            if i > 0 and "text" in doc:
                adrDict, adresse, adrName = self.get_address(
                    doc["text"], sp, adcache, slist, nlist, xlist)
                if not type(adresse) is list:
                    adresse = []
                print(len(nlist))
                # chg = {"doc": doc["_id"],
                #        "adrDict": adrDict, "adresse": adresse}
                print(i, " ", doc["file"], adrDict)
                col.update_one({"_id": doc["_id"]}, {
                    "$set": {"adrDict": adrDict, "adresse": adresse}})
        supcol.update_one({"_id": sup["_id"]}, {"$set": {"adcache": adcache}})
        print(len(nlist))
        textfile = open("n_file.txt", "w")  # TODO: ask for the use of this file
        for element in nlist:
            textfile.write(element + "\n")
        textfile.close()
        textfile = open("x_file.txt", "w")
        for element in xlist:
            textfile.write(element + "\n")
        textfile.close()
        # for chg in changes:
        #     col.update_one({"_id": chg[doc]}, {"$set": {"adrDict": chg["adrDict"], "adresse": chg["adresse"]}})

    def get_spellcheck(self, lan: str, words: list[str]) -> SpellChecker:
        sp = SpellChecker(language=lan, distance=1)
        sp.word_frequency.load_words(words)
        return sp

    def get_address(self, text_raw: str, typo_spellcheck: SpellChecker, adcache: any, streets: list[str], newaddr: list[str], ig_adr: list[str]):

        text_string: str = re.sub(
            "[a-zA-Z äÄöÖüÜß]+", lambda ele: " " + ele[0] + " ", text_raw)
        text: str = text_string.replace(
            '\\', ' ').replace('\ ', '').replace('_', ' ')
        text = "-".join(s.strip() for s in text.split("-"))  # Remove whitespaces around dashes

        # typoSpellcheck: SpellChecker = getSpellcheck()

        text_split = text.split()
        text_corr = []
        for word in text_split:
            text_corr.append(
                re.sub('str$|str.$|straße$|staße$|stasse$', 'strasse', word).lower())

        text = ' '.join(text_corr)

        text = text.replace('.', ' ').lower()
        trex = rex.getRegex(text)
        adr_name = trex.adresseUnvollstaendig
        adresse = trex.adresse

        adressen = {}

        for s in streets:
            sl = re.findall(s, text)
            for sl1 in sl:
                if not sl1 in adr_name:
                    f = text.find(sl1)
                    f1 = text[f:f+len(sl1)]
                    f2 = text[f+len(sl1)+1:f+len(sl1)+6]
                    if f2.find(".")>-1:
                        f2=f2[:f2.find(".")]
                    if f2.find(",")>-1:
                        f2=f2[:f2.find(",")]
                    if f2.find(" ")>-1:
                        f2=f2[:f2.find(" ")]
                    if f2.isnumeric():
                        f3 = f1 + " " + f2
                        # if (type(adresse) is list) and (adresse):
                        if not f3 in adresse:
                            adresse.append(f3)
                            newaddr.append(f3)
                            # print(adresse)
        adresse1 = []

        if (type(adresse) is list) and adresse:
            for adr in adresse:
                # try:
                # TODO: "/" und "-" haben in der Adressenangabe unterschiedliche Bedeutungen. In diesem Skript
                # wird das aber noch nicht berücktichtigt
                adr = adr.replace('/', '-')
                strassenNameOrig = re.findall(
                    '([a-zA-Z äÄöÖüÜß-]*)\d*.*', adr)[0].rstrip()

                streetname = re.sub(
                    'str$|str.$|straße$|staße$|stasse$', 'strasse', strassenNameOrig)
                haus_nummer = adr.replace(strassenNameOrig, '').replace(
                    ' ', '').replace('.', ' ').lstrip()

                if not streetname in streets:
                    if streetname.replace('trasse', 'traße') in streets:
                        streetname = streetname.replace('trasse', 'traße')
                    elif streetname.replace('traße', 'trasse') in streets:
                        streetname = streetname.replace('traße', 'trasse')
                    else:
                        if streetname in adcache:
                            streetname = adcache[streetname]
                        else:
                            nstrassen_name = self.corr_adresse_typo(
                                streetname, typo_spellcheck)
                            if nstrassen_name != streetname:
                                print(streetname, "->", nstrassen_name)
                                nstrassen_name = streetname
                            adcache[streetname] = nstrassen_name
                            streetname = nstrassen_name
                if not streetname in streets:
                    # Wenn eine Strasse nicht in der HIDA Strassenliste ist, sollte sie ignoriert werden
                    # print("Ignoring: " + streetname + " " + adr)
                    ig_adr.append(adr)
                    break
                if not streetname in adresse1:
                    adresse1.append(streetname)
                    adressen[streetname]={}

                if re.search(r'-\d{1,3}$', haus_nummer):
                    # Adresse beinhaltet mehrere Hausnummer: deshalb range aufsplitten und auflisten
                    haus_nummer_range = haus_nummer.rsplit(
                        ' ', 1)[-1].rsplit('-', 1)
                    if haus_nummer_range[1].isnumeric() and haus_nummer_range[0].isnumeric():
                        if int(haus_nummer_range[1])-int(haus_nummer_range[0]) > 0:
                            nr_range = np.arange(int(haus_nummer_range[0]), int(
                                haus_nummer_range[1])+2)  # WARNINg: +1 probably right
                            haus_nummer = [item for item in nr_range.astype(str)]

                elif '-' in haus_nummer:
                    indStrich = haus_nummer.find('-')
                    l = re.findall(r'\d+', haus_nummer[indStrich+1:])
                    if len(l) > 0:
                        haus_nummer_range = [haus_nummer[:indStrich], l[0]]
                        if int(haus_nummer_range[1])-int(haus_nummer_range[0]) > 0:
                            nr_range = np.arange(int(haus_nummer_range[0]), int(
                                haus_nummer_range[1])+2)  # WARNINg: +1 probably right
                            haus_nummer = [item for item in nr_range.astype(str)]
                elif '#' in haus_nummer:
                    indStrich = haus_nummer.find('#')
                    l = re.findall(r'\d+', haus_nummer[indStrich+1:])
                    if len(l) > 0:
                        haus_nummer_range = [haus_nummer[:indStrich], l[0]]
                        if int(haus_nummer_range[1])-int(haus_nummer_range[0]) > 0:
                            nr_range = np.arange(int(haus_nummer_range[0]), int(
                                haus_nummer_range[1])+2)  # WARNINg: +1 probably right
                            haus_nummer = [item for item in nr_range.astype(str)]
                haus_nummer_list = [haus_nummer] if isinstance(
                    haus_nummer, str) else haus_nummer
                haus_nummer_str = ''.join(haus_nummer_list)
                if streetname in adressen:
                    if haus_nummer_str in adressen[streetname]:
                        adressen[streetname][haus_nummer_str]['hausnummer'].extend(
                            haus_nummer_list)
                    else:
                        adressen[streetname] = {
                            haus_nummer_str: {'hausnummer': haus_nummer_list}}

        for key in adressen.keys():
            for innerKey in adressen[key].keys():
                adressen[key][innerKey]['hausnummer'] = list(
                    set(adressen[key][innerKey]['hausnummer']))

        return adressen, adresse1, []  # TODO: ask for the last returned parameter

    def corr_adresse_typo(self, strName: str, typoSpellcheck: SpellChecker):
        typocache = {}  # TODO: Ask for this variable because it was global in original module
        if strName in typocache:
            return typocache[strName]
        else:
            if typoSpellcheck.unknown([strName]):
                x = typoSpellcheck.correction(strName)
                if not x == strName:
                    print("Fixed:", x, strName)
                typocache[strName] = x
                return x
        # print(adrCorr + ' --> ' + corr)
        # print('alle Möglichkeiten:' + str(deutsch.candidates(word)))
        return strName  # TODO: Ask for the desired returning value because this one will never be returned
