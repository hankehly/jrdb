**※ = files that should be used**

### JRDB成績データ（SED）※
This file superceeds SEC as the main JRDB成績データ file. It contains past race results. This is the same type of data you would find on a netkeiba db race page and should be the basis of your "contenders" table.

### JRDB成績データ（SEC）
The predecessor to SED

### JRDB成績拡張データ（SKB）※
This file contains extra 成績 data like "paddock comment." Each record in this file should correspond to a record in SED, so you can essentially join the 2 to form a single table.

### JRDB成績レースデータ（SRB）※
This file contains a small amount of per-race (1 record per race) data, like corner positions and race comment. Corner positions can be inferred from SEC. Other parameters like トラックバイアス (the inner, mid, outer track condition for each of the 4 corners, etc..) could be useful. Because this is per-race data, it could be added to a races table.

### JRDB成績レースデータ（SRA）
The predecessor to SRB

### JRDB馬基本データ（UKC）※
This file contains horse basic information, like sex, hair color, names of mother and father, etc.. It is the "horses" table.

### JRDB競走馬データ（KYI）※
This file superceeds KYH. It is updated on friday and saturday and contains 1 record per race horse. The data includes a wide variety of data like whether its’ the horses’ first time on a grass track, the keys to the previous 5 races, the weight carried and expected odds. This file seems to be similar to the netkeiba "race" page (the one you used during prediction)

### JRDB競走馬データ（KYH）
The predecessor to KYI

### JRDB競走馬データ（KYG）
The predecessory to KYH

### JRDB前走データ（ZEC）
This contains the previous 5 races for a horse in the exact same format as SED. It is just a subset of data for convenience purposes I think.

### JRDB前走拡張データ（ZKB）
This file, like ZEC, is a subset of the last 5 races for a given horse, but it contains the same data as SKB.

### JRDB調教師データ（CZA）※
Trainer master table

### JRDB調教師データ（CSA）
Exactly same description and format as CZA, but described as "差分(今週出走分,先週成績更新分)"

### JRDB騎手データ（KZA）※
This file is essentially the "jockey" table.

### JRDB騎手データ（KSA）
This file has the exact same description and contents as KZA, but is described as the "差分(今週出走分,先週成績更新分)"

### JRDB抹消馬データ（MZA）※
A list of horse ids (血統登録番号) of horses who are no longer registered JRA race horses. Essentially, a list of horses that are no longer competing currently.

### JRDB抹消馬データ（MSA）
Exact same as MZA; but listed as “差分”.. Not clear what this “difference” is..
