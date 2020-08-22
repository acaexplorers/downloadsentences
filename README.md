# downloadsentences
Input: 
inputwords.csv


Output: 
mp3 files in sentences folder
Text updated in words_list.csv

ORIGINAL WORKS WITH DOWNLOADING IN ENGLISH.

ERROR THAT NEEDS FIXING IS CHANGING THIS TO WORK WITH SPANISH.  WHEN I TRIED, THE OUTPUT WAS THE SAME FOR BOTH SENTENCES,

So missing the ___ part.

CHANGES I MADE

Line 37: 
        url = 'http://audio.tatoeba.org/sentences/spa/'+id+'.mp3'


Line 61:
    SITE_URL = 'https://tatoeba.org/spa/sentences/search?from=spa&to=eng&query=%3D{}'

*Also added %3D so that in Tatoeba it would show an = sign but that should not be the issue, and will help get a mroe exact search
