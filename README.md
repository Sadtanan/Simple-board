# Simple Board

A simple web board application built with Flask and SQLite. You can create, read, update, and delete posts; search and sort the list; and view posts with pagination (10 per page).


## How to run the project

1. Clone repository
   git clone https://github.com/yourname/Simple-board.git
   cd Simple-board

2. Create virtual environment
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Initialize database
   python init_db.py

5. Run application
   python app.py

6. Open browser
   http://127.0.0.1:5000


## 3 difficulties faced and how I solved them

1. Understanding how Flask works (coming from React + Node/Express)
   I usually work with React, Node, Express, and MySQL, so the DB part was familiar, but Flask confused me—I didn’t know where the “controller” was, and I had a hard time grasping that the backend renders the UI (templates) and sends full HTML to the front. I got past it by treating each route function as the controller (it handles the request, talks to the DB, and chooses what to send back) and by thinking of Jinja templates as server-side rendering: the server fills in the template with data and sends the resulting HTML to the browser, unlike React where the server sends JSON and the client builds the UI.

2. Pagination with search and sort
   Keeping the current search query and sort order when changing pages was tricky. I solved it by always passing q, sort, and page in the URL and using them in every link (pagination, sort links, and form action), so the backend could rebuild the same filtered and sorted list for each page.

3. Using confirm() before delete
   The requirement was to use confirm() before deleting a post. I implemented it by adding onclick="return confirm('Are you sure you want to delete this post?);" to the delete link. If the user clicks OK, the link is followed and the post is deleted; if they click Cancel, return false prevents the navigation so no request is sent.


## What I thought about most and why

I thought most about how the index page should behave with search, sort, and pagination together (e.g. what happens when you search then change sort, or change page). I wanted the URL to always reflect the current view so that refreshing or sharing the link shows the same results, and so that “Back” and links keep the user in a predictable state. That’s why I focused on encoding q, sort, and page in the URL and using them in every relevant link and form.


## What I would like to improve

- User accounts and permissions : Only allow authors to edit/delete their own posts.
- Rich text : Let writers format post content with different font sizes, colors, bold, italic, etc.
- Pagination UX : For many pages, show something like “1 2 3 … 10” instead of listing every page number.

