## Identification of the problem you are trying to solve by building this particular app.
## Why is it a problem that needs solving?

[hypothetical scenario of old business practices trying to update.]

In our laboratory all lab tests are documented on various excel spreadsheets.
The way it is set up allows all who have access to the document to create, amend and view all records. The problem this creates is a lack of data integrity and protection as all have access to, for example, falsify data or delete historical data which is both valuble in an informative sense, and a legal obligation to keep. This needs to be resolved to maintain data integrity and customer trust, as well as upholding legal obligations. 

Besides maintaining data integrity, this system has no ability to keep track of accountability for data -- there is no record of who has made what records or amendments. By creating users we serve dual purposes; being able to assign permissions for who only needs to view data, and who needs to enter and amend data and we create traceability in data input and updates. 

The final reason for this database is data validation -- with excel it's very easy for your finger to slip and put an incorrect value in, and have no way to be able to correct this accurately in future. If we have defined parameters for data entry, then we have more assurance that the data entered is correct and less likely to be a typing mistake. 

----

## Why have you chosen this database system. What are the drawbacks compared to others?

The main problems I am looking to address is data integrity, tracability & validation. Relational databases are a simple yet effective way to create robust data storage. Data must be consistent across tables and cannot be duplicated, and allows for data normalization which breaks down information effectively to reduce storage size while increasing accuracy & integrity. Relational databases are able to simplify complex queries which I plan to implement when joining tables together. Along with the advantages of relational databases specifically, both SQL and PostgreSQL are very mature technology with rich documentation which will assist me when creating a database on my own, and gives the opportunity to accurately search for required material. Security for relational databases is also simple and effective to implement, allowing only authorized users to access or manipulate data making it extremely effective at securing the data. 

The drawbacks of relational databases are mainly arround scalability. Due to the data being stored in tabular form, the relational database requires a lot more physical memory than other database systems, especially when involving multiple servers. If the database was to grow significantly it'll cause performance and availability issues in the future. The other issue is too many relationships or complex relationships begin to cost more storage space, and becomes difficult to represent the relationships, and again slow down performance of the database. 

While there is drawbacks of this database system, they are not as much of a concern as for a small business there is not a current concern of outgrowing the databases effectiveness and there will not be an excessive volume of data, along with simple relationships and therefore should not impact performance. 

----

## Identify and discuss the key functionalities and benefits of an ORM

Object Relational Mapping is used to connect Object Orientated Programming (in this project, this is Python) to relational databases (SQL). There are quite a few ORM's to choose from, with the most common being SQLalchemy, Django and SQLObject. SQLalchemy is considered one of the best due to its simplicity in syntax and ease of implementation, and is considered a mature & high functioning arcitecture for SQL with great documentation and support available, making it the best choice for someone beginning/learning to code. As ORMs handle the logic to interact with databases it allows for complex queries to be simplified and implemented faster, decreasing the total production time for the project and makes functions easily modularized by defining repeatedly used functions -- an advantage of using python over SQL. 

ORM tools are also used to add a layer of security to SQL databases, for example by reducing the possibility of SQL injection attacks. By not directly handling SQL queries and instead through an ORM medium the overall reduction of SQL queries presents less opportunities for SQL injection attacks, and in combination with data validation it dramatically narrows the scope for what can actually be added to the database. It also allows for the simple implementation of user verification, allowing only those with registered accounts and permission to perform functions that would allow for SQL injections further limiting access to the database, increasing overall security. In this application, only staff member that need access to inserting data are going to recieve the permission, while others can only view it, which will be done through python to apply to SQLalcemy functions. 

----

## Document all endpoints for your API

endpoint                    | verb   | description
------                      | ------ | -------
url/register                | POST   | create a user
url/login                   | POST   | login to your account
url/users                   | GET    | get a list of all users
url/user/[id]               | GET    | get the information of a user
url/user/[id]               | PUT    | update the information of a user
url/user/[id]               | DELETE | delete a user
url/results                 | GET    | get a list of all results
url/results                 | POST   | insert a lab result
url/results/[id]            | GET    | get a single lab result
url/results/[id]            | PUT    | update a lab result
url/results/[id]            | DELETE | delete a lab result
url/products                | GET    | get a list of app products and info
url/products                | POST   | make a product
url/products/[id]           | GET    | get a single product
url/products/[id]           | PUT    | update a product's info
url/products/[id]           | DELETE | delete a product
url/products_results/[id]   | GET    | get all results for a specific product.
url/user_results/[id]       | GET    | get a list of all results from a specific user.

----

## An ERD for your app

![](./Resources/planned_ERD.png)

----

## 	Detail any third party services that your app will use


Plan below; to be detailed when completed. 
Flask -- Blueprint, request, Flask
Marshamllow - fields,
flask_sqlalchemy - SQLAlchemy
flask_marshmallow - Marshmallow
os
jwt


```* Jairo: Everything that needs to be installed in flask to run your application, anything for ORM, authentication, database connection, libraries installed are third party services. ```


----

## 	Describe your projects models in terms of the relationships they have with each other


```Explain the models and relationships involved in the database based on the Flask / SQLAlchemy / etc code that you've implemented ```

----

## 	Discuss the database relations to be implemented in your application

This application has three entities: Users, Lab_results and Products. Each lab result needs to be submitted by a specific user who has lab permission. Each user can do multiple lab reports, but each lab report must only be done by one user making it a one-to-many relationship. Each lab result is also done on one product, but each product can have multiple lab results making it another one-to-many relationship. 


----

## Describe the way tasks are allocated and tracked in your project

Originally the tasks I imagined were laid out in Trello with individual ideas put out, but when I began writing the endpoints I realized these were succinct about the functions I specifically had in mind and reworked the trello board so suit the list of functions. The original set up has: background setup to do, functions that don't require permissions, and non-essential functions. On top of this, a lot of functions I had ideas I thought were cool but not essentially part of the MVP, so in the comments of some essential functions are things to potentially come back to later... it looked like this. ![](./Resources/trello_first_draft.png)

After jotting these in I realized my biggest concerns for workload are going to be:
 -     1) Creating permission for lab staff to only access certain features. <br>
 -     2) To make each account only able to specifically edit their user details, and their own lab results.

 This made me re-evaluate how I want to organize workload so I can prioritize the more complicated things first, before the code is already complicated and harder to follow, the fewer connections should make it easier to set up. So I then organized them in waves, and adjusted bug testing to also include the potential extensions I might want to add in future in essential features. It now looks like this: ![](./Resources/trello_second_draft.png)

This way helps me understanding a lot about what I need to do, the order and the progress I've made. The priority is ordered from 1 to 3, and in each wave the logical order is laid out from top to bottom making it very easy to find where I'm up to and how far I've progressed as I go along. It's ordered so every prerequisite is met beforehand, but also the more complex things are made as early as possible when there's fewer interactions to worry about when debugging, this way what I am most concerned with getting working is done as early as possible -- the specific token interactions. Afterwards in the second wave, I will have a mixture of specific token and lab-permission required, which should be easier as just a boolean value in a table, and finally the last wave is finishing up the last table and should be much easier to manage independently. 

The final last items are less about creating tables, but reading specific information from multiple tables, and are left until the end as they require all tables to be filled, and more technical information about table joining that the rest do not need. Extension items are at the very end of that list. 
