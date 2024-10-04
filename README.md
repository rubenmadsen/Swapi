
## Installation

Before you begin, ensure you have the following installed:

1. **Python**
2. **Docker**

### Install Required Python Packages

Install the necessary packages by running:

```bash
pip install requests
pip install psycopg2-binary
pip install pandas
pip install sqlalchemy 
pip install flask
```

Run the install file
```bash
./path/to/install.sh
```
Edit the crontab using:
``` bash
crontab -e
```
and add this line "0 2 * * * /usr/bin/python /path/to/main.py"

### Run api
```bash
run ./path/to/rest.sh
```
Open web browser and goto: http://localhost:4200/api/character_gravity