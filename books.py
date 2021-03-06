#!/usr/bin/python
# -*- coding: utf-8 -*-

from masechtot import MASECHTOT
import json

def _index_sefaria_labels(text):
    index = {}
    for amud_number in range(2, len(text)):
        daf_number = int(amud_number / 2) + 1
        daf_letter = ("a", "b")[amud_number % 2]
        index["%s%s" %(daf_number, daf_letter)] = text[amud_number]
    return index

class _EmptyMasechet(object):
    def __getitem__(self, x):
        return ()

class _Source(object):
    def __init__(self, json_file_paths, known_missing_masechtot = (), allow_missing = False):
        self.json_file_paths = json_file_paths
        self.cache = {}
        for missing_masechet in known_missing_masechtot:
            self.cache[missing_masechet] = _EmptyMasechet()
        self.allow_missing = allow_missing

    def __call__(self, masechet):
        if masechet not in self.cache:
            for file_path in self.json_file_paths:
                file_path.format(masechet=masechet)
                file_name = "sefaria-data/Talmud/Bavli/%s" % (file_path.format(masechet=masechet))
                try:
                    with open(file_name) as json_file:
                        self.cache[masechet] = _index_sefaria_labels(json.load(json_file)["text"])
                except FileNotFoundError:
                    continue

        if self.allow_missing:
            return self.cache.get(masechet, _EmptyMasechet())
        return self.cache[masechet]

class Books(object):
    def __init__(self):
        self.gemara = _Source(["{masechet}/Hebrew/William Davidson Edition - Aramaic.json"])
        self.gemara_english = _Source(["{masechet}/English/William Davidson Edition - English.json"])
        self.rashi = _Source(("{masechet}/Rashi/Hebrew/Vilna Edition.json",
                              "{masechet}/Rashi/Hebrew/WikiSource Rashi.json",
                              "{masechet}/Rashi/Hebrew/Wikisource Rashi.json"),
                             known_missing_masechtot = ["Tamid"])
        self.tosafot = _Source(("{masechet}/Tosafot/Hebrew/Vilna Edition.json",
                                "{masechet}/Tosafot/Hebrew/Vilna edition.json",
                                "{masechet}/Tosafot/Hebrew/WikiSource Tosafot.json",
                                "{masechet}/Tosafot/Hebrew/Wikisource Tosafot.json"),
                               known_missing_masechtot = ["Tamid"])
        self.rashba = _Source(["{masechet}/Rashba.json"], allow_missing=True)
        self.ramban = _Source(["{masechet}/Ramban.json"], allow_missing=True)

        self._masechet_name_index = {}
        for canonical_name, aliases in MASECHTOT.items():
            # TODO: Remove apostrophes
            self._masechet_name_index[canonical_name.lower()] = canonical_name
            for alias in aliases:
                self._masechet_name_index[alias.lower()] = canonical_name

        self._has_loaded_hebrew_masechet_names = False

    def canonical_masechet_name(self, name):
        original_name = name
        name = name.lower()
        if name in self._masechet_name_index:
            return self._masechet_name_index[name]
        if not self._has_loaded_hebrew_masechet_names:
            for hebrew, canonical in self._load_hebrew_masechet_names().items():
                self._masechet_name_index[hebrew] = canonical
            self._has_loaded_hebrew_masechet_names = True
            if name in self._masechet_name_index:
                return self._masechet_name_index[name]

        raise KeyError(original_name)

    def _load_hebrew_masechet_names(self):
        hebrew_names = {}
        for masechet in MASECHTOT.keys():
            file_name = "sefaria-data/Talmud/Bavli/%s/Hebrew/William Davidson Edition - Aramaic.json" % masechet
            hebrew_names[json.load(open(file_name))["heTitle"]] = masechet
        return hebrew_names
