# Nasjonalbank-converter
#### Converts nasjonalbiblioteks språkbank 16khz dataset into something like libirispeechs format
```
swe_nor/{author_name}/{recording_session}/{recording}.wav
swe_nor/{author_name}/{recording_session}/texts

recording|text
```

This is a hack that i created with the intention of never showing anyone. Its javscripty python with random weirdness thrown into it. I am ashamed. it creates some empty folders and some folders with their recording session as authors. I just deleted those instead of fixing the code so some manual clean up is needed afterwards if you do not wish do fix yourself.

The extracted folders from Swedish and Norwegian has different naming conventions. The 0467 for Swedish is a dataset ID like 0463 is for Norwegian. This name id is repeated within the folder structures. Theres an adb folder which has the id in it. I grab the ID from the main folder name, but since the name of the folders follow a different naming convention i suggest renaming either of them into one naming convention and choosing the default parameter of

```python
def openFolderStations(folder, data, wavs, spls, lang="swe"):
```

to "swe" or "no" depending of which format you choose, i have no idea wich format the danish convention follows

swe:
```
"0467 sv train 1/", "0467 sv train 2/", "0467 sv train 3/", "0468 sv test/"
```

no:
```
"no.16khz.0463-1/", "no.16khz.0463-2/", "no.16khz.0463-3/", "no.16khz.0463-4/", "no.16khz.0464-testing/"]
```
Run it in the same path as the folders. Line 177-178 sets which folders to convert merge them or remove howevery you feel like. The paths works on ubuntu. This has no fancy threading. 1 core to rule them all.

### Swedish:
* sve.16khz.0467-1.tar.gz
* sve.16khz.0467-2.tar.gz
* sve.16khz.0467-3.tar.gz
* sve.16khz.0468.tar.gz

https://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-16&lang=en

### Norwegian:
* no.16khz.0463-1.tar.gz
* no.16khz.0463-2.tar.gz
* no.16khz.0463-3.tar.gz
* no.16khz.0463-4.tar.gz
* no.16khz.0464-testing.tar.gz

https://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-13&lang=en

### Danish(untested needs recoding depending on folder naming convention):
* da.16kHz.0565-1.tar.gz
* da.16kHz.0565-2.tar.gz
* da.16kHz.0611.tar.gz

https://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-19&lang=en
