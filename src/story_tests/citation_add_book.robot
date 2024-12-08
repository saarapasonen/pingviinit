*** Settings ***
Documentation    Hyväksymistestit tarinalle: Käyttäjä voi lisätä book-muotoisen lähteen lomakkeella
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations


*** Test Cases ***
A book citation can be added
    [Documentation]    Tämä testi varmistaa, että käyttäjä voi lisätä book-muotoisen lähteen.
    ...    Lomakkeessa on pakolliset kentät "author", "title", "publisher" ja "year".
    ...    Kun lomake täytetään ja lähetetään, lähde tallentuu tietokantaan ja näkyy listassa.
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
    Page Should Contain  Aliens
    Page Should Contain  Nice books
    Page Should Contain  2024