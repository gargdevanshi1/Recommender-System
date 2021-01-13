# Recommender-System
### Objective – 
To create a recommender system, which recommends movies on the basis of popularity, plot, director, crew, IMdB ratings, etc.

### Description – 
We will initially give the user an option to enter a movie. If he chooses not to enter one, we will use a simple recommender system. In this, we will simply display the 10 most popular movies, based on IMdB ratings and popularity (calculated using a formula). But, if he does enter a movie, we will use a content-based recommender system. In this we will find movies similar to the one entered, based on various factors such as plot, director, crew, etc. After this, we will apply the simple recommender to it, in order to get the most popular ones among those which were short-listed.
In case the movie entered is incorrect (does not exist in our database/spelling error) then we will ask for the movie again.

### Scope – 
As of now, our code will work on the command line. But in the future a front end in the form of an android app, or a webpage can be made. Also, since we will be using just one database to compare the movies, the results may not be as accurate as those of professional sites.
