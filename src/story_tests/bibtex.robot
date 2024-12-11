*** Settings ***
Documentation    Hyväksymistestit tarinalle: Käyttäjä voi generoida Bibtex-tiedoston yhtä nappia painamalla.
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations



*** Test Cases ***
A cite is visible in bibtex form
    [Documentation]  Tämä testi varmistaa, että lähteet muuttuvat oikeaan bibtex muotoon.
    Go To  ${HOME_URL}
    Click Link  Luo uusi viite
    Select From List By Value  cite-select  book
    Click Button  Valitse
    Input Text  author  Stephen King
    Input Text  title  The Shining
    Input Text  publisher  Doubleday
    Input Text  year  1977
    Click Button  Lisää
    Click Link  Lista lisätyistä lähteistä
    Click Link  Bibtex muodossa
    ${bibtex}=  Get Text  //div[@id='content']

    Should Contain  ${bibtex}  author = \"Stephen King\",
    Should Contain  ${bibtex}  title = \"The Shining\",
    Should Contain  ${bibtex}  publisher = \"Doubleday\",
    Should Contain  ${bibtex}  year = \"1977\"

A bibtex cite can be copied
    [Documentation]  Tämä testi varmistaa, että käyttäjä pystyy kopioimaan bibtex-tiedoston leikepöydälle.
    Go To  ${HOME_URL}
    Click Link  Luo uusi viite
    Select From List By Value  cite-select  book
    Click Button  Valitse
    Input Text  author  Stephen King
    Input Text  title  The Shining
    Input Text  publisher  Doubleday
    Input Text  year  1977
    Click Button  Lisää
    Click Link  Lista lisätyistä lähteistä
    Click Link  Bibtex muodossa
    Click Button  Kopioi
    Handle Alert  action=ACCEPT  timeout=10s

A bibtex file can be downloaded
    [Documentation]  Tämä testi varmistaa, että käyttäjä pystyy yhtä nappia painamalla generoimaan
...               bibtex tiedoston sivustolle lisätyistä lähteistä
    Go To  ${HOME_URL}
    Click Link  Luo uusi viite
    Select From List By Value  cite-select  book
    Click Button  Valitse
    Input Text  author  Stephen King
    Input Text  title  The Shining
    Input Text  publisher  Doubleday
    Input Text  year  1977
    Click Button  Lisää
    Click Link  Lista lisätyistä lähteistä
    Click Link  Bibtex muodossa
    Click Button  Lataa BibTeX
