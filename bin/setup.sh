


RED='\033[0;31m'
WHITE='\033[00m'
WARNING='\033[93m'
SUCCESS='\033[92m'

echo "If there are any problems with the script you can always find this script in bin/setup.sh and install it manually"
echo "Find the section of your hardware (OS) and run the script in order"

PYTHON_REF=$(source ./bin/python.sh) # change path if necessary
if [[ "$PYTHON_REF" == "NoPython" ]]; then
    echo "${RED} Python3.7+ is not installed. ${WHITE}"
    exit 1
fi

source ./bin/node.sh



# Make sure nodeJS is installed
if  ! isNodeInstalled ; then
    echo -e "${RED}Node is not install ${WHITE}"
    exit 1
fi

# PYTHON_REF is python or python3
$PYTHON_REF -c "print('Python requirement satisfied >=3.7+')";
if [  ! -f package.json ] || [ ! -f requirements.txt ]; then
    echo "${WARNING}Make sure to run this command from the root directory of the repo.${WHITE}"
    exit 1
    
fi

# for linux installisation
if [[ "$OSTYPE" == "linux"* ]]; then
echo "Detecting OS: $OSTYPE";

# activate python virtual environment
echo "Activating python virtual environment"
python3 -m venv venv
source ./venv/bin/activate

# install packages from requirements.txt
echo "Installing packages from requirements.txt..."
pip install -r requirements.txt

# install node packages
echo "Installing node packages from package.json..."
npm install

# create dummy sqlite3 database
echo "Creating dummy sqlite3 database..."
touch db.sqlite3

# create a clone copy of setting
echo "Cloning settings from source to local_settings..."
cp ./setting/settings.py ./setting/local_settings.py 

# run migrations
echo "Running migrations..."
./manage.py migrate

echo "Your setup is complete! If there are any problems, make sure to install fix or install the required dependencies and rerun this script again"
echo "run npm run dev to build JS files, when you're done, you can now run the web server"
echo "run ./manage.py runserver and go to http://localhost:8000 to see the web server"
fi


# for OSX installisation
if [[ "$OSTYPE" == "darwin"*]]; then
echo "Detecting OS: $OSTYPE";

# activate python virtual environment
echo "Activating python virtual environment"
python3 -m venv venv
source ./venv/bin/activate

# install packages from requirements.txt
echo "Installing packages from requirements.txt..."
pip install -r requirements.txt

# install node packages
echo "Installing node packages from package.json..."
npm install

# create dummy sqlite3 database
echo "Creating dummy sqlite3 database..."
touch db.sqlite3

# create a clone copy of setting
echo "Cloning settings from source to local_settings..."
cp ./setting/settings.py ./setting/local_settings.py 

# run migrations
echo "Running migrations..."
./manage.py migrate

echo "Your setup is complete! If there are any problems, make sure to install fix or install the required dependencies and rerun this script again"
echo "run npm run dev to build JS files, when you're done, you can now run the web server"
echo "run ./manage.py runserver and go to http://localhost:8000 to see the web server"
fi


# for window installisation
if [[ "$OSTYPE" == "msys"*]]; then
echo "Detecting OS: $OSTYPE";

# activate python virtual environment
echo "Activating python virtual environment"
py -m venv venv || python -m venv venv
venv\Scripts\activate

# install packages from requirements.txt
echo "Installing packages from requirements.txt..."
pip install -r requirements.txt

# install node packages
echo "Installing node packages from package.json..."
npm install

# create dummy sqlite3 database
echo "Creating dummy sqlite3 database..."
touch db.sqlite3

# create a clone copy of setting
echo "Cloning settings from source to local_settings..."
cp ./setting/settings.py ./setting/local_settings.py 

# run migrations
echo "Running migrations..."
./manage.py migrate

echo "Your setup is complete! If there are any problems, make sure to install fix or install the required dependencies and rerun this script again"
echo "run npm run dev to build JS files, when you're done, you can now run the web server"
echo "run ./manage.py runserver and go to http://localhost:8000 to see the web server"
fi