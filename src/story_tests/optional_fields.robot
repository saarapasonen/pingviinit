*** Settings ***
Documentation    Hyväksymistestit tarinalle: Käyttäjä voi lisätä lähteen lomakkeella, jossa on myös valinnaisia kenttiä
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations


*** Test Cases ***
A citation with optional fields can be added
    [Documentation]  Tämä testi varmistaa, että käyttäjä voi lisätä lähteitä valinnaisilla kentillä
    ...            ja tiedot tallentuvat tietokantaan.
    Go To  ${HOME_URL}
    Click Link  Luo uusi viite
    Select From List By Value  cite-select  book
    Click Button  Valitse
    Input Text  key  ShiningKing1977
    Input Text  author  Stephen King
    Input Text  title  The Shining
    Input Text  publisher  Doubleday
    Input Text  year  1977
    Input Text  edition  1st
    Input Text  series  Horror
    Click Button  Lisää
    Click Link  Lista lisätyistä lähteistä
    Page Should Contain  Stephen King
    Page Should Contain  The Shining
    Page Should Contain  Doubleday
    Page Should Contain  1977
    Page Should Contain  1st
    Page Should Contain  Horror