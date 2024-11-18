*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Todos

*** Test Cases ***
At start there are no todos
    Go To  ${HOME_URL}
    Title Should Be  ? app
    
