 
## About Virtcomp

Virtcomp is totally different from other business simulation games. It offers a new and better experience. It is the playground where you actually compete with each other. There would be no advantages over other players, it will just be completely based on your skills. 

## Running virtcomp on your local machine
This is the unstable version of VirtComp, it only provides sample data so some of them might not be accurate and you cannot pull the data from origin source (it will result in error if you try ). Virtcomp uses Django, a popular python web framework. To run virtcomp on your local machine. There are many prequesities:

1. You need to have all the required modules installed (except a fews)
2. You must have a database driver (or use sqlite)
3. Redis for caching
4. Python 3.7+ and NodeJS (recommended v14)

If you are only intended to run the web server. You only need modules in requirements.txt files. If you want to run extra modules such as for training dataset purpose for machine learning usage. You must installed it manually. It is located in app/core/services/requirements.txt. For Google API requests (not needed)

```sh
$ pip install -r requirements.txt
```
However if you want to test the full version, you must install packages listed in ```app/core/services/requirements.txt```.

Sample data available in csv_data directory. Otherwise, you will need to pull those from public google sheet of your choice but with same format. You may also be aware that if you use your custom csv (sheets) tests may not work as expected. To enable pulling from google sheet, set USE_DIRECT_SHEETS_DOWNLOAD to True.

Few things before running the server, **MAKE SURE YOU ARE IN THE WORKING DIRECTORY**:
1. Migrate the database
```sh
$ ./manage.py migrate
```
2. Load sample data first or pulling it from google sheet

```sh
$ ./manage.py load_data
```

3. Javascript. For development purpose.
```sh
$ npm run dev
```

4. SECRET_KEY (set your secret key or use the sample provided one, optional)
Settings are located in setting directory. Change if you want. Keep in mind that you will need to create a copy version of settings.py or rename it as local_settings.py. Or things will not work

5. Make sure you have a database server up and running. (recommend PostgresQL)

6. Run the server
```sh
$ ./manage.py runserver
```

## Alternative Installation
1. Fork this repository 
2. Open your terminal and `cd` to your `~/your_folder` folder
3. Clone your fork into the `~/your_folder` folder, by running the following command *replace your username into {your_username} slot*:
    ```bash
    git clone git@github.com:{your_username}/virtComp
    ```
4. CD into the new directory you just created:
    ```bash
    cd virtComp
    ```
5. Run ```setup.sh``` script in bin folder:
    ```bash
    ./bin/setup.sh
    ```
    In case you encounter errors such as `command not found` or `permission denied` you may need to follow these steps to make the file executable in order to solve your problem:
    ```bash
    sudo chmod +x ./bin/setup.sh
    ./bin/setup.sh
    ```

    This will also create a sqlite database file. To change to other database engine, you will need to change the configurations in setting.

## Testing

```
$ ./manage.py test
```
Tested with python 3.7, 3.8, 3.9. NodeJS version used v14
