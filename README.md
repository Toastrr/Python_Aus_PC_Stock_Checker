# Python_Aus_PC_Stock_Checker

This is an Python Application made to check stock on pc retailer websites in Austalia
This application sends a gmail from an gmail address to another when stock has changed
This Application Currently only support scorptec, pccg centrecom and pcpartpicker

Place Urls seperated by a space for each website into each text file
DO NOT EDIT THE JSON FILES
The respective text file are:
pccg_urls.txt
scorptec_urls.txt
centrecom_urls.txt
pcpartpicker_urls.txt


To setup gmail notification you need to edit the "gmail_settings.txt" file
IT IS HIGHLY RECOMMENDED TO USE ANOTHER GMAIL ACCOUNT AS IT IS STORED IN PLAINTEXT
Create an App Password to be used as a the password
Normal password WILL NOT work 
This is A link on how to do so: https://www.lifewire.com/get-a-password-to-access-gmail-by-pop-imap-2-1171882

Logging and verbose output can be activated by changing the respective variables to True

Troubleshooting:
1. Restart the program
2. Ensure you have the urls in the correct text files
3. Delete the json files and restart the program
4. If you are having email issues ensure you have used an app password with mail permission. (Note: only gmail works and using a burner account is reccomended)
5. Enable Verbose output and logging by changing those variable to True and create an Issue with those outputs copied and pasted