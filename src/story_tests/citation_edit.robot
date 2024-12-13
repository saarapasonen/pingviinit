*** Settings ***
Documentation    Hyväksymistestit tarinalle: Käyttäjä pystyy muokkaamaan lisättyä viitettä
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations


*** Test Cases ***
A citation with optional fields can be added
    [Documentation]  Tämä testi varmistaa, että muokkaa-painikkeella käyttäjä pääsee uudelle sivulle muokkaamaan valitsemaansa lähdettä ja muokatut tiedot tallentuvat oikein
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
    Click Button  Lisää
    Click Link  Lista lisätyistä lähteistä
    Click Button  Muokkaa viitettä
    Page Should Contain  Muokkaa viitettä

    Input Text  author  Robin Hood
    Click Button  Muokkaa
    Page Should Contain  Robin Hood

