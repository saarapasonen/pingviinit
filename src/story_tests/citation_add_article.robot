*** Settings ***
Documentation    Hyväksymistestit tarinalle: Käyttäjä voi lisätä article-muotoisen lähteen lomakkeella
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Todos


*** Test Cases ***
An article citation can be added
    [Documentation]    Tämä testi varmistaa, että käyttäjä voi lisätä article-muotoisen lähteen.
    ...    Lomakkeessa on pakolliset kentät "author", "title", "journal" ja "year".
    ...    Kun lomake täytetään ja lähetetään, lähde tallentuu tietokantaan ja näkyy listassa.
    Go To  ${HOME_URL}
    Click Link  Luo uusi viite
    Select From List By Value  cite-select  article
    Click Button  Valitse
    Input Text  author  Kalle K.
    Input Text  title  Aliens
    Input Text  journal  Nice journal
    Input Text  year  2024
    Click Button  Lisää
    Click Link  Lista lisätyistä lähteistä
    Page Should Contain  Kalle K.
    Page Should Contain  Aliens
    Page Should Contain  Nice journal
    Page Should Contain  2024