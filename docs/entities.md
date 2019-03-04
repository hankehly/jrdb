# Entities

#### Contender
- SED
- SKB
- (KYI will be used for prediction?)

#### Race
- SRB

#### Horse
- UKC
- MZA (or separate this to a "deregistered horses" table)

#### Trainer
- CZA

#### Jockey
- KZA

#### ?? (1:m racetrack/race?)
- KAB

#### Racetrack
- ??

#### Genealogy
- http://www.jrdb.com/program/keito_code.txt



| table name | docs used | relationships |
|:-|:-|:-|
|horses|UKC, MZA||
|races|srb||
|contenders|SED, SKB\[, KYI\]||
|trainers|CZA||
|jockeys|KZA||
|racetracks|||
||KAB|1:M(Racetrack/Race?)|
