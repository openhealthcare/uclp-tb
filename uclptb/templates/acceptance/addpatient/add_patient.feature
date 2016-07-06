As a User
I need to add a Patient
So that I can start to record details about their care

Given that I am logged in to the application
When I click the Add Patient button
Then I should be taken to the Add Patient referral route

Given that I am on the Add Patient screen
When I enter the hospital number of a new patient
When I enter the patient demographics
Then the system should create a new patient
