from django.db import IntegrityError

from jrdb.models import Horse, HairColorCode, HorseSymbol, RacetrackCode
from jrdb.templates.parse import parse_date, parse_int_or, filter_na
from jrdb.templates.template import Template

import numpy as np


class UKC(Template):
    """
    http://www.jrdb.com/program/Ukc/ukc_doc.txt
    """
    name = 'JRDB馬基本データ（UKC）'
    items = [
        ['pedigree_reg_num', '血統登録番号', None, '8', 'X', '1', None],
        ['name', '馬名', None, '36', 'X', '9', '全角１８文字'],
        ['sex', '性別コード', None, '1', '9', '45', '1:牡,2:牝,3,セン'],
        ['hair_color_code', '毛色コード', None, '2', '9', '46', 'コード表参照'],
        ['horse_symbol', '馬記号コード', None, '2', '9', '48', 'コード表参照'],
        ['sire_name', '父馬名', None, '36', 'X', '50', '全角１８文字'],
        ['dam_name', '母馬名', None, '36', 'X', '86', '全角１８文字'],
        ['damsire_name', '母父馬名', None, '36', 'X', '122', '全角１８文字'],
        ['birthday', '生年月日', None, '8', '9', '158', 'YYYYMMDD'],
        ['sire_birth_yr', '父馬生年', None, '4', '9', '166', 'YYYY 血統キー用'],
        ['dam_birth_yr', '母馬生年', None, '4', '9', '170', 'YYYY 血統キー用'],
        ['damsire_birth_yr', '母父馬生年', None, '4', '9', '174', 'YYYY 血統キー用'],
        ['owner_name', '馬主名', None, '40', 'X', '178', '全角２０文字'],
        ['owner_racetrack_code', '馬主会コード', None, '2', '99', '218', '競馬場毎にある。場コードと同じ'],
        ['breeder_name', '生産者名', None, '40', 'X', '220', '全角２０文字'],
        ['breeding_loc_name', '産地名', None, '8', 'X', '260', '全角４文字'],
        ['is_retired', '登録抹消フラグ', None, '1', '9', '268', '0:現役,1:抹消'],
        ['data_saved_on', 'データ年月日', None, '8', '9', '269', 'YYYYMMDD'],  # same as filename date
        ['sire_genealogy_code', '父系統コード', None, '4', '9', '277', None],
        ['damsire_genealogy_code', '母父系統コード', None, '4', '9', '281', None],
        ['reserved', '予備', None, '6', 'X', '285', 'スペース'],
        ['newline', '改行', None, '2', 'X', '291', 'ＣＲ・ＬＦ']
    ]

    def clean(self):
        df = self.df.drop(columns=['data_saved_on', 'reserved', 'newline'])

        df.name = df.name.str.strip()
        df.sex = df.sex.astype(int).map({1: Horse.MALE, 2: Horse.FEMALE, 3: Horse.CASTRATED})

        hair_color_codes = {code.key: code.id for code in HairColorCode.objects.filter(key__in=df.hair_color_code)}
        df['hair_color_code_id'] = df.hair_color_code.map(hair_color_codes).astype(int)
        df.drop(columns=['hair_color_code'], inplace=True)

        horse_symbols = {symbol.key: symbol.id for symbol in HorseSymbol.objects.filter(key__in=df.horse_symbol)}
        df['symbol_id'] = df.horse_symbol.map(horse_symbols).astype('Int64')
        df.drop(columns=['horse_symbol'], inplace=True)

        df.sire_name = df.sire_name.str.strip()
        df.dam_name = df.dam_name.str.strip()
        df.damsire_name = df.damsire_name.str.strip()
        df.birthday = df.birthday.apply(parse_date, args=('%Y%m%d',))
        df.sire_birth_yr = df.sire_birth_yr.astype(int)
        df.dam_birth_yr = df.dam_birth_yr.astype(int)
        # damsire_birth_yr is missing sometimes..
        df.damsire_birth_yr = df.damsire_birth_yr.str.strip().apply(parse_int_or, args=(np.nan,)).astype('Int64')
        df.owner_name = df.owner_name.str.strip()

        racetrack_codes = {code.key: code.id for code in RacetrackCode.objects.filter(key__in=df.owner_racetrack_code)}
        df['owner_racetrack_code_id'] = df.owner_racetrack_code.map(racetrack_codes).astype('Int64')
        df.drop(columns=['owner_racetrack_code'], inplace=True)

        df.breeder_name = df.breeder_name.str.strip()
        df.breeding_loc_name = df.breeding_loc_name.str.strip()
        df.is_retired = df.is_retired.astype(int).astype(bool)

        return df

    def persist(self):
        df = self.clean()
        for row in df.to_dict('records'):
            obj = filter_na(row)
            try:
                Horse.objects.create(**obj)
            except IntegrityError:
                Horse.objects.filter(code=obj['pedigree_reg_num']).update(**obj)
