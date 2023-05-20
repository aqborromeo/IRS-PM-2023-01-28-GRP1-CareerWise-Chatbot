### [ Practice Module ] IRS-PM-2023-01-28-GRP1-myUpskill-Chatbot

Testing main branch protection
## SECTION 1 : PROJECT TITLE
## myUpSkillbot - Career Planner

<img src="SystemCode/src/frontend/src/assets/images/robot-dialog.png"
     style="float: left; margin-right: 0px;" />

---

## SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT

With the rise of technology and advancements in artificial intelligence, 
chatbots have become increasingly popular in various industries, including 
education.

“A chatbot is a software application that aims to mimic human conversation 
through text or voice interactions, typically online” as defined on Wikipedia. 
They can be programmed to understand and respond to specific queries, making 
them an ideal tool for helping individuals choose courses that align with 
their preference, interests or expertise.

By using myUpskill Chatbot, individuals can easily choose to input either 
their interests or domain of expertise and receive tailored career path 
recommendations based on their responses. myUpskill Chatbots can also provide 
additional information about courses, such as course descriptions, and 
university options and potential compensation range. 

Utilising the various techniques that were taught to us in the Intelligent 
Reasoning Systems (IRS) modules. The team has set out to build a sizable 
knowledge base by matching Singapore base datasets into Occupational 
Information Network (O*Net) Database. Further details can be seen in 
the Knowledge Modelling section of the documentation.

The benefits of using myUpskill Chatbots for career path selection include
convenience, accessibility, and personalised recommendations. myUpskill 
Chatbots can be potentially accessed through a variety of platforms, 
including social media, messaging apps, and websites (but for this project
implementation the team have created a python flask base application 
hosted in Amazon Web Service). This makes it easier for individuals to 
receive initial course recommendations on the go, without the need for 
lengthy research or face to face consultations.

Overall, aim to have myUpskill Chatbots to be a valuable tool for helping 
individuals choose career path based on their interests or expertise. We 
hope to provide a convenient and personalised way to receive career 
recommendations, making the career path selection process more accessible 
and efficient. As technology continues to evolve, it is likely that chatbots
 will become an increasingly important part of education and career path selection.

---

## SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID (MTech Applicable)  | Work Items (Who Did What) | Email (Optional) |
| :------------ |:---------------:| :-----| :-----|
| Borromeo, Angelie Quiapo | A0270177A | Project Manager and Documentation| angelieqborromeo@gmail.com |
| Chua Jack Yune | A0269363U | Main Developer | jckynchua@yahoo.com |
| Nilothpal Bhattacharya | E1113631 |  | e1113631@u.nus.edu |
| Kwatt Ivy | E1113633 | Secondary Developer| kwattivy@gmail.com|

---

## SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO

[myUpskill_Chatbot_System_Design](https://drive.google.com/file/d/1d9SQSdmppO11if0RIS2ST-YUo0UrSKm2/view?usp=share_link)
[myUpskill_Chatbot_Marketing_Video](https://drive.google.com/file/d/1jbRNkvWKwGsyzUAT6mFrdXZBotPiXnhT/view?usp=share_link)
---

## SECTION 5 : USER GUIDE

`Refer to appendix <Installation & User Guide> in project report at Github Folder: ProjectReport`

This video intends to guide the user in installing and configuring myUpskill Chabot in local machine.
[Intallation and User Guide](https://drive.google.com/file/d/1QjMueGh3bZSc4L2dDPmJNDtVucLNg6eA/view?usp=share_link)


### [ 1 ] To run the system in other/local machine:
### Install additional necessary libraries. This application works in python 3.10 only.
### Postgres Database needs to be installed in your workstation 

> Download Postgres Database and install [PostgreSQL_Download](https://www.postgresql.org/download/)

> Clone the Github repository of myUpskill Chatbot.  $ git clone https://github.com/aqborromeo/IRS-PM-2023-01-28-GRP1-myUpskill-Chatbot.git

> Configuring the front-end. $ cd IRS-PM/IRS-PM-2023-01-28-GRP1-myUpskill-Chatbot/SystemCode/src/frontend

> $ cp .env.myupskil .env

> $ source .env

> For prodedure in installing NodeJS and NPM follow [Installation Procedure](https://learn.microsoft.com/en-us/microsoft-edge/visual-studio-code/microsoft-edge-devtools-extension/install) prior to running the below commands.

> $ npm install

> $ npm run serve

> $ npm run build

> Configuring the backend. $ cd IRS-PM/IRS-PM-2023-01-28-GRP1-myUpskill-Chatbot/SystemCode/src/backend

> $ cp .env.myupskil .env

> $ source .env

> open and virtual env that has python 3.10 (refer to the System Setup Video for Reference).

> pip install poetry

> poetry install

> alembic upgrade head

> flask seed run

> flask run


> **Go to URL using web browser to access the frontend and register an account**  http://localhost:8080/ 

---
## SECTION 6 : PROJECT REPORT / PAPER

`Refer to project report at Github Folder: ProjectReport`

**Recommended Sections for Project Report / Paper:**
- Executive Summary 
- Project Description & Objectives 
- Knowledge Modeling
- Project Solution and Architecture
- Project Scope (Assumptions, System Features and Limitation)
- Project Conclusions and Improvements
- Bibliography
- Appendix of report: Interview with Subject Matter Expert
- Appendix of report: Survey Results
- Appendix of report: Installation and User Guide

---
## SECTION 7 : MISCELLANEOUS

`Refer to Github Folder: Miscellaneous`

### CareerJouney_Survey_Result_14052023.xlsx
* Results of survey
* Insights derived, which were subsequently used in our system

---

### <<<<<<<<<<<<<<<<<<<< End of Template >>>>>>>>>>>>>>>>>>>>

---

**This [Machine Reasoning (MR)](https://www.iss.nus.edu.sg/executive-education/course/detail/machine-reasoning "Machine Reasoning") course is part of the Analytics and Intelligent Systems and Graduate Certificate in [Intelligent Reasoning Systems (IRS)](https://www.iss.nus.edu.sg/stackable-certificate-programmes/intelligent-systems "Intelligent Reasoning Systems") series offered by [NUS-ISS](https://www.iss.nus.edu.sg "Institute of Systems Science, National University of Singapore").**

**Lecturer: [GU Zhan (Sam)](https://www.iss.nus.edu.sg/about-us/staff/detail/201/GU%20Zhan "GU Zhan (Sam)")**

[![alt text](https://www.iss.nus.edu.sg/images/default-source/About-Us/7.6.1-teaching-staff/sam-website.tmb-.png "Let's check Sam' profile page")](https://www.iss.nus.edu.sg/about-us/staff/detail/201/GU%20Zhan)

**zhan.gu@nus.edu.sg**
