# HackTheCloud 2.0 - 404 Not Found team

### Members: [Jason Li](https://jasonli0616.dev/), [Amogh Turaga](https://joelwillams2021.github.io/Bootstrap_CV_Website/), [Raghav Paratkar](https://github.com/raghavparatkar), [Evan Dennison](https://github.com/Redennison)

## About the project
This is a project made for the [Hack The Cloud 2.0](https://www.hackthefog.com) hackathon. It is a concept website to find freelance tutors. Check out our [Devpost page](https://devpost.com/software/tutor-center) and [submission video](https://youtu.be/1SJ6DS6xrlk) for more info!

# From our Devpost submission:
## Inspiration

Our inspiration came from the increasing pressure that students are subject to without a way to reliably find a source to help them learn and the lack of opportunities that students and freelance tutors have to showcase their abilities and strengthen their repertoire.

## What it does

TutorCenter is a website that allows anyone easy access to tutors, filtered by subject and grade level to help streamline their experience. It also helps teachers and students build their skills by allowing them to become tutors and assist students in need at the same time. Furthermore, the website rewards tutors for good work by displaying the tutors that have the highest reviews at the top to allow them to further grow their private business.

## How we built it

Before actually coding, we discussed the concept and the necessities to make the website work, like a database to register, sign in, become a tutor, and write reviews to accurately rate each tutor. Then once we started to code, we used Flask, Python and HTML to make a simple landing page with a navigation bar and buttons to register and sign in. After linking the sign-in and login pages in the nav bar, we then made a database to store the sign in credentials to cross reference the input email and password every time the user signed back in. Then, we focused on displaying the tutors based on what filters were on, ranking them from highest rating to the lowest. For each specific tutor, we created another HTML file and formatted the file using the database that corresponds to the tutor, and it contains the profile image, rating, name, contact information, what/who they teach and their ratings. After we added a function to rate the tutor and add an in-depth explanation as to why, we added another registration link in the nav bar to allow users to become a tutor by inputting their information, as well as the subject and grade they teach.

## Challenges we ran into

The first challenge we ran into was identifying if an image url submitted was valid, which was solved by researching more into the request library in Python and using request.head() to check if the headers of the image were png, jpeg or jpg. Another recurring issue was initializing the databases and separating testing and production databases, which we solved by going through the code and systematically troubleshooting and modifying each part that could have changed the desired outcome.

## Accomplishments that we're proud of

We were able to effectively use the data in the database and synthesized models to create functions that we thought were useful. We were also proud that we had the collaboration and development skills necessary to make an end product that looks professional.

## What we learned

We learned the importance of collaboration in a high pressure and timed environment to increase productivity and morale, since that helped us make an end product that all of us are proud of. We also learned a lot more about SQL databases as that was crucial for our application to be successful.

## What's next for Tutor Center

Expanding to more platforms to get more people interested in tutoring or learning, as well as allowing users to update their information and delete their accounts.