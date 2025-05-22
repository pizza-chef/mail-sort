# mail-sort
Note: Code last updated 2021. I have not updated to the latest Print Post pricing and plan since end of 2024.

This application is a Python GUI that accepts a mailing list in CSV, Text Tab Delimited or an Excel spreadsheet and sorts them for Australia Post's Print Post. Once sorted this application will output:
- A PDF that 
- A Label Plan that will be printed using the Visa Labels software provided for each tub
	- The program will determine how many labels to print for tubs based on dimensions and weight of each article

This application does not print the barcodes as given by their Address Matching Approval System as accreditation was way too expensive for a side project.
If you need barcodes (and more advanced features) you'll have to pay for actual software like DataTools Twins

## Deployment
As a basic means of deployment I have been creating an executable with the CreateExecutable.bat file.


## Configuring
When running the application there is a settings file that needs configuring to correctly points
to the Visa Labels executable for printing the labels.