import unittest
import json
import os
from backend.app.services.cos_sim_filter import CosSimFilter  # Adjust path as needed
import pathlib

class TestCosSimFilterWithEmbeddings(unittest.TestCase):

    def setUp(self):
        curr_path = pathlib.Path(__file__).parent.absolute()
        self.course_data_file = os.path.join(
            curr_path.parent.parent,
            'app/routers/yale_courses_keywords_fall_2024.json'
        )
        self.user_input_file = os.path.join(
            curr_path,
            'test_user_input_embeddings.json'
        )

        with open(self.course_data_file, 'r', encoding='utf-8') as f:
            self.course_data = json.load(f)

        self.cos_sim_filter = CosSimFilter(use_precomputed_embeddings=True)

    def get_user_input_data(self, prompt):
        """Retrieve embedding and must_include_course_title for a specific user input prompt from JSON."""
        with open(self.user_input_file, 'r', encoding='utf-8') as f:
            user_inputs = json.load(f)

        for entry in user_inputs:
            if entry['input'] == prompt:
                return entry['input_embedding'], entry['must_include_course_title']
        raise ValueError(f"No embedding found for prompt: {prompt}")

    def test_top_n_cos_sim_courses_for_game_developer(self):
        # Test for "I want to be a game developer" prompt
        user_prompt = "I want to be a game developer"
        user_input_embedding, must_include_course_title = self.get_user_input_data(user_prompt)

        n = 5

        top_courses = self.cos_sim_filter.get_top_n_cos_sim_courses_given_user_input_and_json_data(
            user_input=user_input_embedding,
            course_data=self.course_data,
            n=n,
            user_input_is_embedding=True
        )

        course_titles = [course['courseTitle'] for course in top_courses]
        self.assertIn(must_include_course_title, course_titles,
                      f"The course titled '{must_include_course_title}' should be in the top {n} courses.")


if __name__ == '__main__':
    unittest.main()