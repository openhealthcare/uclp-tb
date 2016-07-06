As a Doctor
I need to record the details of the initial TB Assessment
So that we can understnad how to treat the patient.

Given that I am on a patient detail view for a new patient
When I click the TB Assessment button
Then I should be taken to a form that lets me enter details of the assessment.

Given that I am on the TB Assessment pathway
When I go to the Presentation & History step
Then I should be able to record the patient's Social History

Given that I am on the TB Assessment pathway
When I am on the final stage
When I click save
Then I should be taken to the Patient detail view
Then I should be able to see the information I entered on the Assessment pathway
