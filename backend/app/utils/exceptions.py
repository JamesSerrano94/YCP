class CourseNumberNotFoundError(Exception):
    """
    Raised when the course number is not found in the course list.
    """
    def __init__(self, message, missing_course_number):
        self.message = message
        self.missing_course_number = missing_course_number
class LLMRecommenderError(Exception):
    """
    Raised when the LLM recommender encounters an error.
    """
    pass


