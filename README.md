# MichelleLiang_T2A2
## API Webserver Project: NightSky

### R1. Identification of the problem you are trying to solve by building this particular app.

Stargazing can be an exciting and fascinating hobby to learn. However the subject of astronomy is often difficult and confusing to navigate for beginners. With this app, I hope to  provide the general public with an easy and accessible way of understanding how to traverse the night skies by readily supplying timings and locations for celestial bodies and phenomenons in simple terms and descriptions. By making stargazing more straightforward and uncomplicated, there’s a greater ease of entry to learn sciences and astronomy whilst also ultimately serving as a reminder to everyone that you only really need to look up to see some of the universe's most beautiful wonders and gifts.  

### R2. Why is it a problem that needs solving?

Viewing astronomical events can be quite confusing as timings largely depend on where you are located on Earth. This particular API is designed for a specific target audience and aims to be managed and utilised by Victorians as it provides data specific to this location group. This way, there is no confusion about times and locations when viewing data. Further, many astronomy applications are often hard to navigate as they use confusing coordinates for locations, have millions of objects available for users to track, require telescopes and good map skills. This can be overwhelming for those new to stargazing. Thus, this application targets specifically those who are new or casual astronomers as well as the general public by providing simple descriptions and details of viewing locations/times and tracks significant objects such as the planets in our solar system and large stars that are visible to the naked eye without the need of telescopes. 

In addition, as someone who is new to a hobby, it is often hard to make local friends and meet new people, especially in this field as it is a niche hobby. To solve this problem, the app also acts as a platform to connect these new astronomers with fellow enthusiasts through an organised meetup feature. 


### R3. Why have you chosen this database system? What are the drawbacks compared to others?

PostgreSQL is the chosen database system which has a wide range of benefits to suit the needs and requirements of this project. It is a powerful open-source system used extensively in industry for its reliability, speed and efficacy. Firstly, postgres supports a large number of data types which include simple data types such as  numeric, string, boolean and datetime but can also support more complex data types such as JSONB (used to store and operate JSON objects) which is used extensively in this project. The data systems’ infrastructure involves use of constraints and data verification systems which ensure data integrity and reduces the risks of data loss. In addition, it also has a robust privilege management system for authentication and authorisation. These functionalities allow users to control who and what access is available to different parties. For this project in particular, there are login features which require passwords to be stored thus it’s essential for database administrators to have control over authorisation. Finally, postgres also supports third party extensions, tools and programming languages, one of which is python which is what will be used for the majority of the source code in this project. 

#### Drawbacks to alternative database systems: 

Postgres is not the best for real time data processing whereby DBMS such as Apache Kafke or StreamSQL would be more useful as they include functionalities that enable real time analytics.

MySQL database systems are designed to be more streamlined and simple so they are optimised for speed. This, smaller projects with simpler queries would benefit more from utilising the simplicity and increased processing speed of mySQL over postgres. 

One thing to note is that although MySQL has a simpler setup, because postgreSQL offers more tools to handle complex queries and data types in larger volumes, for future scalability of the project, it is worthwhile opting to use postgreSQL. Particularly for this project, using postgreSQL ensures that if in the future, the application is to expand its location scope to provide services to other regions besides Victoria, the database is able to handle growing volumes of data. 

A drawback of postgres against MongoDB is that it relies on relational data models. Hence if an application does not require relational data, a less rigid and more adaptable database system such as MongoDB may be better suited. This system does not require data to be stored in tabular form which relies on strict normalisation procoles which can bottleneck the development phase. Schemas are not so inflexible in that they do not need to be predefined as they do in relational databases. 


### R4. Identify and discuss the key functionalities and benefits of an ORM


Object relational mapping (ORM) is a programming tool for enabling a connection between relational database systems and object oriented programming languages. It involves converting the object into data to be stored, retrieved or reconstructed when required and through ORM, these changes made to the object are shared and updated to the database. Consequently, developers now have a method of working with data in the form of objects whilst data is stored and managed in a relational database using SQL.

Abstraction is the basis of ORM in that ORM tools allow manipulation of objects regardless of how they relate to their data source. A useful feature applicable to this project is the ability to map out relational databases with objects and tables that have one-to-many, many-to-many or one-to-one relationships. Further, embedded in ORMs is the ability to perform CRUD (creating, reading, updating, deleting) operations without directly using SQL using object oriented programming tools. 

#### Benefits of ORM:

Improves efficiency and productivity: Developers can prioritise app development and business logic over database concerns as database queries are handled by the ORM system. By abstracting the complexities when using databases, developers can focus on delivering high quality solutions and increase overall productivity. 

Promotes code reusability: Application logic and database are two separate systems which means developers can reuse code for similar database systems without concern for specific SQL language. 

Security Features: ORM systems have in-built security features which can prevent malicious input from affecting databases as well as features that allow users to set permission and access rules to prevent unauthorised access to data. 


### R5. Document all endpoints for your API


### R6. An ERD for your app 

### R7. Detail any third party services that your app will use

### R8. Describe your project models in terms of the relationships they have with each other


### R9. Discuss the database relations to be implemented in your application

Tables:

**A. users** : represents each user in the applications system. 

**B. diaries**: represent diary entries for each user where they can report sightings

**C. meetings**: represent organised meetups for stargazing that can be created by users

**D. groups**: a joining table to link meeting and users

Users have a **one to many** relationship with diary entries: they can write many diary entries but a diary entry belongs to one user. 

As users and meetups have a **many to many** relationship (multiple users can join multiple groups), a joining table (called groups) is required to connect the two. 

Groups have a **one-to-many** relationship with users as one group can have multiple members. Groups also have a one-to-many relationship with meetings as multiple meetings can belong to one group.


**E. entities**: lists the celestial entities available to see

**F. events** : lists the event for each celestial entity

Entity and events have a **one to many relationship** as entities can belong to multiple events but events can only have one entity

Meetups and events have a **one-to-one relationship** as each meetup can revolve around one event at a time. Note the event is optional (nullable) if the meetup is for an unlisted event. 


### R10. 


## Reference List

Arif, A. (2023) *How to Use Psycopg2: The PostgreSQL Adapter for Python, Timescale Blog.* Available at: https://www.timescale.com/blog/how-to-use-psycopg2-the-postgresql-adapter-for-python/ (Accessed: 07 December 2023). 

*Comparing MongoDB vs PostgreSQL (no date) MongoDB*. Available at: https://www.mongodb.com/compare/mongodb-postgresql (Accessed: 06 December 2023). 


Hoyos, M. (2019) *What is an ORM and Why You Should Use it, Medium*. Available at: https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a (Accessed: 06 December 2023). 

Hoang, N. (2023) *Bcrypt — A Beginner’s Guide, Medium.* Available at: https://medium.com/@CodeNameNoah/bcrypt-a-beginners-guide-e2293cc1eeb6 (Accessed: 07 December 2023). 

Justin  Ellingwood (no date) *PostgreSQL advantages: Benefits of using PostgreSQL, Prisma’s Data Guide*. Available at: https://www.prisma.io/dataguide/postgresql/benefits-of-postgresql (Accessed: 05 December 2023). 

Kanade, V. (2023) *What Is ORM? A Comprehensive Guide to Object-Relational Mapping, Spiceworks*. Available at: https://www.spiceworks.com/tech/data-management/articles/what-is-orm-a-comprehensive-guide-to-object-relational-mapping/#:~:text=ORM%20systems%20serve%20as%20a,in%20the%20RDBMS%20using%20SQL. (Accessed: 06 December 2023). 

Nguyen, M. (2020) *Marshmallow: Easy Serialization in Python, Knoldus Blogs*. Available at: https://blog.knoldus.com/marshmallow-easy-serialization-in-python/ (Accessed: 07 December 2023). 	

Oppermann, A. and Urwin, M. (2023) *What is object-relational mapping (ORM)?, Built In*. Available at: https://builtin.com/data-science/object-relational-mapping (Accessed: 05 December 2023). 

Saini, A. (2023) *An Easy introduction to Flask Framework for Beginners, Analytics Vidhya*. Available at: https://www.analyticsvidhya.com/blog/2021/10/flask-python/ (Accessed: 07 December 2023). 

Sharma, R. (2023) *MySQL vs Postgres: A Comprehensive Comparison of Two Leading Open-Source Databases, Discover the Key Differences Between MySQL and Postgres Databases*. Available at: https://www.sprinkledata.com/blogs/mysql-vs-postgresql-15-differences (Accessed: 05 December 2023). 


