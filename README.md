<img src="https://github.com/adigapranava/PCUBE/blob/master/static/images/favicon2.png?raw=true">

# PCUBE  
<br>
An E-commerce Website designed using Django. Similar to OLX but with some extra features and fun.

## KeyPoints
* User can post a product for Sale setting a minimum price for it
* Other User who are intrested about the product can bid for it
* The Owner gets the notification about the bid and can sell to anyone he wishes.

## Other Features
* Real time notification
* Filtering product based on BRAND, TYPE, PRICE
* Notification on individual product
* Ask Question about the Product


## Installation 
1. `git clone https://github.com/adigapranava/PCUBE.git`
2. `cd PCUBE`
3. `docker-compose up`

## OR

1. Fork and Clone
    <ol>
    <li>Fork PCUBE, the Repository</li>
    <li>Clone the repo to your System</li>
    </ol>


2. Create a Virtual Environment for the Project

    In Windows
    ```bash
    python -m venv venv
    
    venv\Scripts\activate
    ```

    In Ubuntu/MacOS
    ```bash
    python -m virtualenv venv
    
    source venv/bin/activate
    ```
   
    If you are giving a different name then `venv`, then please mention it in `.gitigonre` first

3. Install all the requirements

    ```bash
    pip install -r requirements.txt
    ```

4. Checkout to develop branch
     ```git
    git status
    git pull
    git branch
    git checkout develop
    
    ```

5. Create a super user.
    In django if you want to access admin page, you need to create an account first.
    ```djangotemplate
    python manage.py createsuperuser
    ```
   Then select your username and password.

6. Run server
    ```bash
    python manage.py runserver
    ```
7. Do the Development and send me a PR referencing the issue.


