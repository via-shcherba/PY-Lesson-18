import unittest
from unittest.mock import patch
import json
from job_parser import get_vacancies, analyze_vacancies 

class TestJobParser(unittest.TestCase):

    @patch('job_parser.requests.get')
    def test_get_vacancies(self, mock_get):
        mock_response = {
            'items': [
                {'name': 'Python Developer',
                 'salary': {'from': 1000, 'to': 2000},
                 'key_skills': [{'name': 'python'}, {'name': 'django'}]},
                {'name': 'Senior Python Developer',
                 'salary': {'from': 2000, 'to': 3000},
                 'key_skills': [{'name': 'python'}, {'name': 'flask'}]},
                {'name': 'Junior Python Developer',
                 'salary': {'from': 500, 'to': 1000},
                 'key_skills': [{'name': 'python'}, {'name': 'sqlalchemy'}]}
            ]
        }

        mock_get.return_value.json.return_value = mock_response
        
        result = get_vacancies('python developer', 213)
        
        self.assertIn('items', result)
        self.assertEqual(len(result['items']), 3)

    def test_analyze_vacancies(self):
        vacancies = [
            {'name': 'Python Developer',
             'salary': {'from': 1000, 'to': 2000},
             'key_skills': [{'name': 'python'}, {'name': 'django'}]},
            {'name': 'Senior Python Developer',
             'salary': {'from': 2000, 'to': 3000},
             'key_skills': [{'name': 'python'}, {'name': 'flask'}]},
            {'name': 'Junior Python Developer',
             'salary': {'from': 500, 'to': 1000},
             'key_skills': [{'name': 'python'}, {'name': 'sqlalchemy'}]}
        ]

        result = analyze_vacancies(vacancies)
        
        self.assertEqual(result['total_vacancies'], 3)
        self.assertAlmostEqual(result['average_salary'], 1167)

        requirements = result['requirements']
        print('requirements')
        print(requirements)
        self.assertIn({'name': 'Python Developer', 'count': 1, 'persent': 33.33}, requirements)
        self.assertIn({'name': 'Senior Python Developer', 'count': 1, 'persent': 33.33}, requirements)
        self.assertIn({'name': 'Junior Python Developer', 'count': 1, 'persent': 33.33}, requirements)

if __name__ == '__main__':
    unittest.main()