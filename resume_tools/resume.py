import json
from datetime import datetime

# Read in a json file as a class
# The structure of the json file is:
'''
{
    "name":str,
    "email":str,
    "phone":str,
    "website":str,
    "education": [
        {
        "type":str,
        "name":str,
        "location":str,
        "degree": [
            {
            "type":str,
            "name":str
            }
        ],
        "dates":{
            "start":"YYYY-MM-DD",
            "end":"YYYY-MM-DD"
        },
        "gpa": int,
        "courses": [
            {
            "name":str,
            "description:str,
            }
        ],
      }
    ],
    "employment": [
        {
        "title":str,
        "company":str,
        "location":str,
        "dates": {
            "start":"YYYY-MM-DD",
            "end":"YYYY-MM-DD"
        },
        "description":str,
        }
    ],
    "skills": [
        {
        "name":str,
        "level":str,
        "description":str
        }
    ],
    "achievements": [
        {
        "name":str,
        "description":str,
        "date":"YYYY-MM-DD"
        }
    ],
    "activities": [
        {
        "name":str,
        "positions": [str],
        "description":str
        }
    ],
    "projects": [
        {
        "name":str,
        "source":str,
        "description":str,
        "languages": [str]
        }
    ]
}
'''


class SimpleDate:
    def __init__(self, start, end):
        self.start = datetime.strptime(start, '%Y-%m-%d')
        if end != "PRESENT":
            self.end = datetime.strptime(end, '%Y-%m-%d')
        else:
            self.end = "PRESENT"

    def __str__(self):
        return self.month_year()

    def month_year(self):
        start_month_year = self.start.strftime('%B %Y')
        if self.end != "PRESENT":
            end_month_year = self.end.strftime('%B %Y')
        else:
            end_month_year = "PRESENT"
        return start_month_year + " - " + end_month_year

    def __repr__(self):
        return self.month_year()


class Degree:
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def __str__(self):
        return self.pretty_print()

    def pretty_print(self):
        return f"{self.type} of {self.name}"


class Education:

    def __init__(self, data):
        self.type = data['type']
        self.name = data['name']
        self.location = data['location']
        self.degree = [Degree(d['type'], d['name']) for d in data['degree']]
        self.dates = SimpleDate(data['dates']['start'], data['dates']['end'])
        self.gpa = data['gpa']
        self.courses = data['courses']

    def __str__(self):
        return self.name + " - " + str(self.dates)

    def __repr__(self):
        return f"Education({self.name}, {str(self.dates)})"


class Employment:
    def __init__(self, data):
        self.title = data['title']
        self.company = data['company']
        self.location = data['location']
        self.dates = SimpleDate(data['dates']['start'], data['dates']['end'])
        self.description = data['description']

    def __str__(self):
        return self.title + " - " + self.company + " - " + str(self.dates)

    def __repr__(self):
        return f"Employment({self.title}, {self.company})"


class Skill:
    def __init__(self, data):
        self.name = data['name']
        self.level = data['level']
        self.description = data['description']

    def __str__(self):
        return self.name + " - " + self.level

    def __repr__(self):
        return f"Skill({self.name}, {self.level})"


class Achievement:
    def __init__(self, data):
        self.name = data['name']
        self.description = data['description']
        self.date = data['date']

    def __str__(self):
        return self.name + " - " + str(self.date)

    def __repr__(self):
        return f"Achievement({self.name}, {str(self.date)})"


class Activity:
    def __init__(self, data):
        self.name = data['name']
        self.positions = data['positions']
        self.description = data['description']

    def __str__(self):
        return self.name + " - " + self.description

    def __repr__(self):
        return f"Activity({self.name}, {self.description})"


class Project:
    def __init__(self, data):
        self.name = data['name']
        self.source = data['source']
        self.description = data['description']
        self.languages = data['languages']

    def __str__(self):
        return self.name + " - " + self.description

    def __repr__(self):
        return f"Project({self.name}, {self.description})"


class ResumeDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dict):
        # vars(self).update(dict)
        if 'education' in dict:
            dict['education'] = [Education(data) for data in dict['education']]
        if 'employment' in dict:
            dict['employment'] = [Employment(data) for data in dict['employment']]
        if 'skills' in dict:
            dict['skills'] = [Skill(data) for data in dict['skills']]
        if 'achievements' in dict:
            dict['achievements'] = [Achievement(data) for data in dict['achievements']]
        if 'activities' in dict:
            dict['activities'] = [Activity(data) for data in dict['activities']]
        if 'projects' in dict:
            dict['projects'] = [Project(data) for data in dict['projects']]

        return dict


class PhoneNumber:
    def __init__(self, number):
        self.number = number

    def __str__(self):
        return self.number

    def __repr__(self):
        return f"PhoneNumber({self.number})"

    def pretty_print(self):
        # Return number in (xxx) xxx-xxxx format
        return f"({self.number[:3]}) {self.number[3:6]}-{self.number[6:]}"


class Resume:
    def __init__(self, data):
        self.name = data['name']
        self.email = data['email']
        self.phone = PhoneNumber(data['phone'])
        self.website = data['website']
        self.education = data['education']
        self.employment = data['employment']
        self.skills = data['skills']
        self.achievements = data['achievements']
        self.activities = data['activities']
        self.projects = data['projects']

    def get_education(self):
        education = ""
        for edu in self.education:
            education += f"({edu.type}) {edu.name} ({edu.location}): {edu.dates.month_year}\n"
        return education

    def get_employment(self):
        employment = ""
        for emp in self.employment:
            employment += f"{emp.title} ({emp.company} - {emp.location}): {emp.dates.month_year}\n"
        return employment

    def get_skills(self):
        skills = ""
        for skill in self.skills:
            skills += f"{skill.name} ({skill.level}): {skill.description}\n"
        return skills

    def get_achievements(self):
        achievements = ""
        for achievement in self.achievements:
            achievements += f"{achievement.name}: {achievement.description} ({achievement.date})\n"
        return achievements

    def get_activities(self):
        activities = ""
        for activity in self.activities:
            activities += f"{activity.name} ({', '.join(activity.positions)}): {activity.description}\n"
        return activities

    def get_projects(self):
        projects = ""
        for project in self.projects:
            projects += f"{project.name} ({project.source}): {project.description} ({', '.join(project.languages)})\n"
        return projects

    def get_resume(self):
        self.sort_employment_by_date()
        resume = ""
        resume += f"Name: {self.name}\n"
        resume += f"Email: {self.email}\n"
        resume += f"Phone: {self.phone}\n"
        resume += f"Website: {self.website}\n"
        resume += f"Education:\n{self.get_education()}\n"
        resume += f"Employment:\n{self.get_employment()}\n"
        resume += f"Skills:\n{self.get_skills()}\n"
        resume += f"Achievements:\n{self.get_achievements()}\n"
        resume += f"Activities:\n{self.get_activities()}\n"
        resume += f"Projects:\n{self.get_projects()}\n"
        return resume

    def sort_employment_by_date(self):
        """
        Sort the employment list by date in reverse order
        :return:
        """
        self.employment.sort(key=lambda x: x.dates.start, reverse=True)

    def __str__(self):
        return self.get_resume()
