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
- Create the environment
  ```
  conda env create -f backend/environment.yml
  ```
- Install Package in editable mode
  ```
  pip install -e .
  ``` 
- Run `backend/app/services/YaleCoursePlannerKeyWordGenerator.py`
- Run the application with Uvicorn
  ```
  uvicorn backend.app.main:app --reload
  ```

## Current Pipeline
- Offline: Precompute word embeddings for all courses offline
- Online:
  1. Convert input formats of time and taken courses
  2. Filter based on time and taken courses
  3. Perform cosine similarity to find suitable courses
  4. Use LLM to finalize the output