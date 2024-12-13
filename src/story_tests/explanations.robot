*** Settings ***
Documentation    Hyväksymistestit tarinalle: Käyttäjä pystyy painamaan viitettä ja löytää silloin selityksen mitä sillä meinataan.
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations


*** Test Cases ***
A explanation can be found when citation type is clicked
    [Documentation]  Tämä testi varmistaa, että kun lisää viitettä ja painaa viitteen tyyppiä ilmestyy selitys mitä kyseisellä tyypillä meinataan
    Go To  ${HOME_URL}
    Click Link  Luo uusi viite
    Select From List By Value  cite-select  book
    Click Button  Valitse
    Click Element  xpath=//summary[text()='Key:']




