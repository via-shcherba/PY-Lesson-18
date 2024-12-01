import requests
import json
from collections import Counter

def get_vacancies(keyword, region):
    url = f"https://api.hh.ru/vacancies"
    params = {
        'text': keyword,
        'area': region,
        'per_page': 100,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def sum_list_elements(elements):
    sum = 0
    for elem in elements:
        if elem:
            sum += elem
    return sum

def analyze_vacancies(vacancies):   
    original_vacancies = [] 
    for vacancy in vacancies:
        original_vacancies.append(
            vacancy['name']
        )
    
    salaries = [vacancy['salary']['from'] for vacancy in vacancies if vacancy.get('salary')]    
    avg_salary = sum_list_elements(salaries) / len(salaries) if salaries else 0
    
    count_requirements = Counter(original_vacancies)
    total_vacancies = len(count_requirements.items())
    requirements = []
    for keyword, count in count_requirements.items():
        percent = (count / total_vacancies) * 100 if total_vacancies else 0
        requirements.append({'name': keyword, 'count': count, 'persent': round(percent, 2)})
   
    return {
        'total_vacancies': total_vacancies,
        'average_salary': round(avg_salary),
        'requirements': requirements
    }

def main():
    keywords = ['python developer', 'жестянщик']
    region = 113  # Россия

    overall_results = []

    for keyword in keywords:
        vacancies_data = get_vacancies(keyword, region)
        vacancies = vacancies_data['items']
        analysis_result = analyze_vacancies(vacancies)
        
        overall_results.append({
            'keywords': keyword,
            'count': analysis_result.get('total_vacancies', ''),
            'average_salary': analysis_result.get('average_salary',''),
            'requirements': analysis_result.get('requirements','')
        })
        
    with open('vacancy_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(overall_results, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()