*** Settings ***
Documentation    Hyväksymistestit tarinalle: Käyttäjä pystyy poistamaan lisätyn lähteen.
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Todos

*** Test Cases ***
A citation can be removed
    [Documentation]  Tämä testi varmistaa, että käyttäjä pystyy poistamaan valitsemansa lähteen
    ...            ja lähde poistuu näkyvistä listalta
    Go To  ${HOME_URL}
    Click Link  Luo uusi viite
    Select From List By Value  cite-select  book
    Click Button  Valitse
    Input Text  author  Kalle K.
    Input Text  title  Aliens
    Input Text  publisher  Nice books
    Input Text  year  2024
    Click Button  Lisää
    Click Link  Lista lisätyistä lähteistä
    Page Should Contain  Kalle K.
    Click Button  Poista viite
    Page Should Not Contain  Kalle K.
