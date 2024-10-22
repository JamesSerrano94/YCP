# Yale Career Pathway Planner
## Welcome to Yale CourseMap

![Screenshot 2024-09-21 at 5 24 31 PM](https://github.com/user-attachments/assets/7510d73a-5369-4729-8729-0334b69e289a)

## Front End Setup
- Install Node.js
- cd to Frontend folder
  ```
  cd frontend
  ```
- Run npm install and then run npm start
  ```
  npm install
  npm start
  ```
- should be able to see it running locally on port 3000

## Frontend Test
```
npm test
```

## Back End Setup
- Install Conda or Mamba
- Navigate to the back end folder
  ```
  cd backend
  ```
- Create the environment
  ```
  conda env create -f environment.yml
  ```
- Navigate to the backend folder
  ```
  cd backend
  ```
- Run `app/services/YaleCoursePlannerKeyWordGenerator.py`
- Run the application with Uvicorn
  ```
  uvicorn app.main:app --reload
  ```
