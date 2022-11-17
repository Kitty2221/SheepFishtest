# Setup

#### Before running project

- Create local env file
- Build containers
- Run project
- 
#### Create local env file

Just run `make test_env`


#### Build containers

`docker-compose -f docker-compose-dev.yml build`


#### Run project

`docker-compose -f docker-compose-dev.yml up`


#### When project is running

- Apply db migrations `make migrations`
- Create superuser `make test_user`. After that you will be able to login into Admin
- Be happy!

#### Create new app

`make app name=<app_name>`

#### All commands you can find in `Makefile`

### Project description
The service receives information about a new order, creates checks in the database for all printers of the point specified in the order, and sets asynchronous tasks for generating PDF files for these checks. If the point does not have any printer - returns an error. If receipts for this order have already been created, it returns an error (the order number is passed).
An asynchronous worker using wkhtmltopdf to generate a PDF file from an HTML template.


