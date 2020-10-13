**SDOS Group-8**

Gaurav Agarwal (2017288)

Prince Sachdeva (2017080)

Reeshabh Kumar Ranjan (2017086)

# Alohomora CareerShala

**[1.0 Introduction](#10-introduction)**

[1.1 Purpose of the project](#11-purpose-of-the-project)

[1.2 Scope of Project](#12-scope-of-project)

[1.3 Glossary](#13-glossary)

[1.4 Abbreviations](#14-abbreviations6)

[1.5 References](#15-references)

**[2.0 Description](#20-description)**

[2.1 System Environment](21-system-environment)

[2.2 Functional Requirements Specification](#22-functional-requirements-specification)

[2.2.1 Students](#221-students)

[2.2.2 Industry Expert](#222-industry-expert)

[2.2.3 Administrator](#223-administrator)

[2.3 User Characteristics](#23-user-characteristics)

[2.4 Non-Functional Requirements](#24-non-functional-requirements)

#

# 1.0 Introduction

## 1.1 Purpose of the project

The purpose of this document is to provide a detailed overview of a career guidance portal. It will describe each page that the users can navigate to, the options present on them, the behaviour of the system from various types of inputs/situations. This document is intended for both the sponsors and the developers of the system.

## 1.2 Scope of Project

This web portal will guide the users to know about their career interests and how they can proceed to achieve their dream career. One type of users of this system would be mostly students from government schools who do not get much guidance about career interests. The other users of this system would be industry experts who can mentor the students to pursue their dream career.

Students will enter their interests on the portal and based on their interests, they will get certain projects or tasks from the experts of that field of interest. These projects will motivate students to develop more interest in that field and then they can choose to follow more projects or change their field of interest. The ultimate goal of this project is to create a web interface that will instil confidence in the students to allow them to make an informed decision about their career field.

Industry experts will add projects or tasks on the portal and add tags to them which would specify the field of interests. Students will be able to see these projects and do them if they interest them.

##

## 1.3 Glossary

| **Term** | **Definition** |
| --- | --- |
| Developer | The person who is assigned the task to work on a subset of the project aiming to build the system. For example, frontend-engineer, backend-engineer etc. |
| Sponsor | The person who is interested in the development of the project provides regular advice but is not the developer. |
| Student | The class of customers who will use the portal to get career-related advice. |
| Expert | The class of customers who are specialised/experienced in their field (career), and want to provide feedback/advice to students. |
| Institute | The class of customers which represents an institute. An institute will provide their own guidance content and will be able to post the same on some part of the website allocated to them. |
| Streams | Field of interest for students - like medicine, aeronautics, physicists etc. |

## 1.4 Abbreviations

| **Abbreviation** | **Full-Form** |
| --- | --- |
| CCP | Career Counselling Path (sub-system) |
| CM | Career Management (sub-system) |
| SM | Site Management (sub-system) |

## 1.5 References

&quot;SRS Example - MSU CSE.&quot; [SRS Example](http://www.cse.msu.edu/~chengb/RE-491/Papers/SRSExample-webapp.doc).

#

# 2.0 Description

## 2.1 System Environment

There are majorly three types of users:

1. **Students:** Students will interact with the CCP (career-counselling path sub-system). This has interfaces that allow a student to:
    1. answer a small questionnaire that will help the system customize their dashboard as per their interests.
    2. browse various career paths (with their descriptions), view articles/videos and available projects related to each path.
    3. continue their career path based on the choices they make for the current activity.
    4. ask queries to experts regarding a particular field or a project.
    5. see other students&#39; projects and comment/review on them.
2. **Industry Expert:** Industry experts will interact with the CM (content-management sub-system) and CCP. This has interfaces that allow an expert to
    1. Post content in the relevant sections. For example, an aerospace engineer will post his/her content in the career section meant for aerospace engineering.
    2. Reply to queries asked by the students in CCP.
3. **Admin:** Administrators will interact with the SM (site-management sub-system). This has interfaces that allow an admin to
    1. View each part of the website that can be accessed publicly by any student. This means that admin cannot view pages that display temporary drafts of posts by students, experts.
    2. Exercise moderation powers. This includes, but is not limited to temporarily banning students and experts.
    3. Access parts/pages of the website meant for posting core-site related content. This includes announcements (for example, related to feature updates, etc).

## 2.2 Functional Requirements Specification

This section outlines the activities for each of the users separately.

### 2.2.1 Students

1. When a student accesses the portal for the first time, he/she can click on the Student button in the Home Page (fig 1) and go through a set of questions regarding their field of interest.
    1. Questionnaire (3 categories of questions):

        1. I have a specific interest in which I want to build my career?
            1. Give a list of interests we have opportunities for.
        2. I want a job as soon as possible
            1. Questions about kinds of jobs based on interest to differentiate between. For eg. Sales, Data entry, Admin etc.
        3. I am confused
            1. Do you want to learn a skill to discover an opportunity?
            2. Do you want to make a choice based on ease of getting a job?
            3. Do you want to explore exciting new options for careers?

1. While the student answers the questions related to their field of interests,
    1. Field of interests will be narrowed down to specific domains according to the choices of the students.
    2. Different resources (video, articles, blogs, activities etc.) will be provided to them to get a deeper understanding of their chosen interests.
2. When a student is returning to the portal, he/she can click on the sign-in button in the Home Page (fig 1) and continue the career path.
3. To register on the portal, a student will
    1. enter basic details including name, age, gender, school/college.
    2. enter his/her mobile number or email account and an OTP will be generated to verify the same.
4. Students will be frequently prompted to register on the portal if they are not already registered so that they can continue any time later.
5. A student can re-start the path from the beginning anytime, which would again start with answering questionnaires as shown earlier.
6. After completing the questionnaire, a student can check out the courses recommended by the portal based on their answers filled in the questionnaire.
7. If a student has not started a project/task, he/she can choose one from the project lists of a particular field. They can check out the projects listed down by the experts and do them if interested.
8. A registered student can comment under the project sections on their current portal if they have any doubts.
9. A registered student can view other portals which are not in his/her field of interest but could not add posts, or comments on the posts of other portals.
10. A student after completing a project or task will have to submit an evaluation which could be a quiz, feedback, project implementation in the form of documents (essay, article, coding scripts) etc.

### 2.2.2 Industry Expert

1. When the expert accesses the portal for the first time, they can click on the signup button to join the website.
    1. In the signup process, the expert will need to answer some technical questions that will identify their profession. For example, if the expert wants to sign up as a lawyer, he/she will need to provide his/her graduation details and other experience related questions.
    2. They will also need to provide some sort of verification.
    3. Finally, to confirm their contact details (email/phone), they need to verify it via OTP mechanism.
2. Once registered, the expert will need to login to view the website content as a registered expert.
3. On login, a dashboard page will show up. This dashboard will contain all the relevant information for the expert. It includes:
    1. A view for the stream related to their field of expertise. For example, a Lawyer will see recent posts posted in the Law category.
    2. An option to add a new post in the above stream. This will allow the lawyer to post text, images, attach documents, website links, and a combination of the same.
    3. Experts will be able to remove posts that are reported to them by the community subscribed to the corresponding stream.
4. Option to interact with the students via. This includes:
    1. Answering specific doubts that questions have regarding the corresponding field.
    2. This interaction will happen in a chat-type environment.
5. Experts will be able to add resources (project ideas, reference material etc).
6. Experts will also be able to request the addition of new questions in the questionnaire.

### 2.2.3 Administrator

1. Administrators will be pre-registered. This means, their account will already be created beforehand, and they just need to set a new password using a unique link sent to their email id.
2. Administrators will see a dashboard upon login. This dashboard will contain the following:
    1. A graphical representation of statistics - including messages posted per day, per week, per month etc.
    2. A concise report of all the unattended reports (of inappropriate behaviour by someone on the portal). They can take action based on the reports such as warning/banning the reported user.
    3. A view showing requests to add new questions in the questionnaire.
3. Administrators will be able to set up/modify the questionnaire using the UI.
4. They will be able to manage streams.
    1. Adding a new stream.
    2. Deleting an existing stream.
    3. Editing stream details - name, cover image, etc.
5. Administrators will have the ability to verify an expert from their end and then assign them to a stream.
6. He/she will be able to view everything a student or an expert can view, except unposted drafts.

## 2.3 User Characteristics

The Student is expected to be able to use the Internet and search engine. They should be able to fill surveys as well. They should know how to use an email.

The Industry Experts are expected to be able to use the Internet and search engine as well as know how to use an email service.

Admin should be able to do everything described above.

## 2.4 Non-Functional Requirements

The website will be hosted on a server with high internet speed. The time of accessing the website would depend on the network speed at the user&#39;s end.

The platform is architecture as well as Device independent i.e. it can run on any OS as well as devices like phones, laptops etc. as long as they support browsers.
