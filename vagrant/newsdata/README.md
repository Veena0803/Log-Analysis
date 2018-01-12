# Log Analysis Project
#### Description
This project is part of the Udacity Full Stack Nanodegree program which demonstrates the features of SQL & Python. This project helps in building a reporting tool from a fictional news database using PostgreSQL to discover what the user prefers reading. It also contains news articles written by various authors and the server log for the news site. This project would address the questions such as the most popular articles, authors of all time and the days when there were more than 1% failed requests. 

### Prerequistes:
Following are the prerequistes to run this project. Please click on the link for the instructions on how to install the various components:
  - [Python2](https://www.python.org/downloads/)
  - [Vagrant](https://www.vagrantup.com/docs/installation/)
  - [Virtual Box](https://www.virtualbox.org/)

### Project Setup:
1. Install Vagrant and Virtual Box from the links above.
2. Download the data for this project [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).
3. Extract the contents of this file. Within the "newsdata" folder, exists the necessary "newsdata.sql" file.

### Launching the VM:
- Using the following command launch the Vagrant VM inside the Vagrant sub-folder which was downloaded from the [repository](https://github.com/udacity/fullstack-nanodegree-vm): 
     `$ vagrant up`
- To log in the VM:
     `$ vagrant ssh`
- cd /vagrant/ 
- ls to find the sub-directory "newsdata"
- To run the project type the following command:
`python newsQueries.py`
**Note**: Follow the steps in "Setting up the DB" before executing the above statement.
### Setting up the DB:
- When setting up the DB, the first time use the following command:
`psql -d news -f newsdata.sql`
- Further connections can be setup by using the command `psql -d news`
### Creating views:
- In order to figure out the days which had more than 1% errors create two views using these queries:
```sql
  CREATE OR REPLACE VIEW log_view AS
  SELECT status, date(time) AS day
  FROM log;
```
```sql
CREATE OR REPLACE VIEW final_log_view AS
SELECT time::date, 100 * (sum(case when status != '200 OK' then 1 else 0 end)::
float / count(day)::float)
AS test 
FROM log_view 
GROUP BY time::date;
```
### Technologies Used:
- Python
- SQL
