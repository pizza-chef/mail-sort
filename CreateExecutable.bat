cd "C:/Users/Dylan/Documents/Twins 2.0/MailSort"
call venv\Scripts\activate.bat
pyinstaller --noconfirm --clean ^
			--distpath "C:/Users/Dylan/Documents/Twins 2.0/dist" ^
			--workpath "C:/Users/Dylan/Documents/Twins 2.0/build" ^
			--icon="images/app_icon.ico" ^
		MailSort.spec

