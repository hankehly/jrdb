# JRDB Document Types

Files handled in this repository are denoted with an asterisk (*)

#### SED（JRDB成績データ）*
This file superceeds SEC as the main JRDB成績データ file. It contains past race results. This is the same type of data you would find on a netkeiba db race page and should be the basis of your "contenders" table.

#### SEC（JRDB成績データ）
The predecessor to SED

#### SKB（JRDB成績拡張データ）*
This file contains extra 成績 data like "paddock comment." Each record in this file should correspond to a record in SED, so you can essentially join the 2 to form a single table.

#### SRB（JRDB成績レースデータ）*
This file contains a small amount of per-race (1 record per race) data, like corner positions and race comment. Corner positions can be inferred from SEC. Other parameters like トラックバイアス (the inner, mid, outer track condition for each of the 4 corners, etc..) could be useful. Because this is per-race data, it could be added to a races table.

#### SRA（JRDB成績レースデータ）
The predecessor to SRB

#### UKC（JRDB馬基本データ）*
This file contains horse basic information, like sex, hair color, names of mother and father, etc.. It is the "horses" table.

#### KYI（JRDB競走馬データ）*
This file superceeds KYH. It is updated on friday and saturday and contains 1 record per race horse. The data includes a wide variety of data like whether its’ the horses’ first time on a grass track, the keys to the previous 5 races, the weight carried and expected odds. This file seems to be similar to the netkeiba "race" page (the one you used during prediction)

#### KYH（JRDB競走馬データ）
The predecessor to KYI

#### KYG（JRDB競走馬データ）
The predecessory to KYH

#### ZEC（JRDB前走データ）
This contains the previous 5 races for a horse in the exact same format as SED. It is just a subset of data for convenience purposes I think.

#### ZKB（JRDB前走拡張データ）
This file, like ZEC, is a subset of the last 5 races for a given horse, but it contains the same data as SKB.

#### CZA（JRDB調教師データ）*
Trainer master table

#### CSA（JRDB調教師データ）
Exactly same description and format as CZA, but described as "差分(今週出走分,先週成績更新分)"

#### KZA（JRDB騎手データ）*
This file is essentially the "jockey" table.

#### KSA（JRDB騎手データ）
This file has the exact same description and contents as KZA, but is described as the "差分(今週出走分,先週成績更新分)"

#### MZA（JRDB抹消馬データ）*
A list of horse ids (血統登録番号) of horses who are no longer registered JRA race horses. Essentially, a list of horses that are no longer competing currently.

#### MSA（JRDB抹消馬データ）
Exact same as MZA; but listed as “差分”.. Not clear what this “difference” is..

#### OZ（JRDB基準オッズデータ）* 
単勝・複勝・連勝（馬蓮）オッズ 

#### OW（ワイド基準オッズデータ）* 
ワイドのオッズデータ

#### OU（馬単基準オッズデータ）*
馬単のオッズデータ

#### OT（３連複基準オッズデータ）*
三連複のオッズデータ
