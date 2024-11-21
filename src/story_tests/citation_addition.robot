*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Todos

*** Test Cases ***
A book citation can be added
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

An article citation can be added
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

An inproceedings citation can be added
    Go To  ${HOME_URL}
    Click Link  Luo uusi viite
    Select From List By Value  cite-select  inproceedings
    Click Button  Valitse
    Input Text  author  Kalle K.
    Input Text  title  Aliens
    Input Text  booktitle  Dogs
    Input Text  year  2024
    Click Button  Lisää
    Click Link  Lista lisätyistä lähteistä
    Page Should Contain  Kalle K.
    Page Should Contain  Aliens
    Page Should Contain  Dogs
    Page Should Contain  2024