# JRDB Document Types

Files handled in this repository are denoted with an asterisk (*)

#### SED（JRDB成績データ）*
This file supersedes SEC as the main JRDB成績データ file. It contains past race results. This is the same type of data you would find on a netkeiba db race page and should be the basis of your "contenders" table.
＊ The "種別" keys in the description file are incorrect. The correct declaration values are found in the [larger code list](http://www.jrdb.com/program/jrdb_code.txt).
木	17:00

#### SEC（JRDB成績データ）
The predecessor of SED
木	17:00

#### SKB（JRDB成績拡張データ）*
This file contains extra 成績 data like "paddock comment." Each record in this file should correspond to a record in SED, so you can essentially join the 2 to form a single table.
木	17:00

#### SRB（JRDB成績レースデータ）*
This file contains a small amount of per-race (1 record per race) data, like corner positions and race comment. Corner positions can be inferred from SEC. Other parameters like トラックバイアス (the inner, mid, outer track condition for each of the 4 corners, etc..) could be useful. Because this is per-race data, it could be added to a races table.
木	17:00

#### SRA（JRDB成績レースデータ）
The predecessor of SRB
木	17:00

#### CZA（JRDB調教師データ）*
Trainer master table
木	19:00

#### CSA（JRDB調教師データ）*
Most recent (2 week) updates to trainer master table (CZA). Same format as CZA.
木	19:00

#### KZA（JRDB騎手データ）*
This file is essentially the "jockey" table.
木	19:00

#### KSA（JRDB騎手データ）*
Most recent (2 week) updates to trainer master table (KZA). Same format as KZA.
木	19:00

#### MZA（JRDB抹消馬データ）*
A list of horse ids (血統登録番号) of horses who are no longer registered JRA race horses. Essentially, a list of horses that are no longer competing currently.
木	19:00

#### MSA（JRDB抹消馬データ）
Most recent updates (probably 2 weeks like other diff files) of MZA master
木	19:00

#### KYI（JRDB競走馬データ）*
This file supersedes KYH. It is updated on friday and saturday and contains 1 record per race horse. The data includes a wide variety of data like whether its’ the horses’ first time on a grass track, the keys to the previous 5 races, the weight carried and expected odds. This file seems to be similar to the netkeiba "race" page (the one you used during prediction)
金土	19:00

#### KYH（JRDB競走馬データ）
The predecessor of KYI
金土	19:00

#### KYG（JRDB競走馬データ）
The predecessor of KYH
金土	19:00

#### KKA（JRDB競走馬拡張データ）
WIP
金土	19:00
 
#### UKC（JRDB馬基本データ）*
This file contains horse basic information, like sex, hair color, names of mother and father, etc.. It is the "horses" table.
金土	19:00

#### JOA（JRDB情報データ）
WIP
金土	19:00

#### OZ（JRDB基準オッズデータ）* 
単勝・複勝・連勝（馬蓮）オッズ 
金土	19:00

#### OW（ワイド基準オッズデータ）* 
ワイドのオッズデータ
金土	19:00

#### OU（馬単基準オッズデータ）*
馬単のオッズデータ
金土	19:00

#### OT（３連複基準オッズデータ）*
三連複のオッズデータ
金土	19:00

#### OV（３連単基準オッズデータ）*
３連単のオッズデータ
金土	19:00

#### ZEC（JRDB前走データ）
This contains the previous 5 races for a horse in the exact same format as SED. It is just a subset of data for convenience purposes I think.
金土	19:00

#### ZKB（JRDB前走拡張データ）
This file, like ZEC, is a subset of the last 5 races for a given horse, but it contains the same data as SKB.
金土	19:00

#### KAB（JRDB開催データ）*
馬場・天候予想等の開催に対するデータ
金土	19:00
 
#### KAA（JRDB開催データ）
The predecessor of KAB
金土	19:00

#### BAC（レース番組情報）*
Details about a specific race. Contains the datetime of each race.
金土	19:00
 
#### BAB（レース番組情報）
The predecessor of BAC
金土	19:00

#### CYB（JRDB調教分析データ）*
とあるレースのとある馬の調教データ（調教距離、調教量評価など）
金土	19:00
 
#### CYA（JRDB調教分析データ）
The predecessor of CYB
金土	19:00

#### CHA（JRDB調教分析データ）
WIP
金土	19:00

#### TYB（JRDB直前情報データ）
WIP
土日	17:00

#### HJC（JRDB払戻情報データ）
WIP
土日	17:00

#### HJA（JRDB払戻情報データ）
WIP
土日	17:00
