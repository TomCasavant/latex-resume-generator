import json
from string import Template

from resume_tools.resume import Resume, ResumeDecoder


class LaTeXResume:
    def __init__(self, resume_data: Resume, tex_template):
        self.resume = resume_data
        self.tex_template = tex_template

    def generate_resume(self):
        with open(self.tex_template, 'r') as tex_file:
            template = Template(tex_file.read())

        with open('output/resume.tex', 'w') as output_resume:
            self.fill_resume(output_resume, template)

    def format_education(self):
        education = ""
        for edu in self.resume.education:
            education += "\\resumeSubheading\n"
            education += f"{{{edu.name}}}{{{edu.location}}}\n"
            education += f"{{{edu.degree[0].pretty_print()}}}{{{edu.dates.month_year()}}}\n"
        return education

    def format_employment(self):
        employment = ""
        for emp in self.resume.employment:
            employment += "\\resumeSubheading\n"
            employment += f"{{{emp.title}}}{{{emp.location}}}\n"
            employment += f"{{{emp.company}}}{{{emp.dates.month_year()}}}\n"
            employment += f"\\resumeItemListStart\n\\resumeDescription\n{{{emp.description}}}\n\\resumeItemListEnd\n"
        return employment

    def format_projects(self):
        projects = ""
        for project in self.resume.projects:
            projects += f"\\resumeSubItem{{{project.name}}}\n"
            projects += f"{{{project.description}}}{{{project.source}}}\n"
        return projects

    def escape_string(self, string):
        return string.replace('#', '\\#')

    def format_skills(self):
        advanced_skills = [self.escape_string(s.name) for s in self.resume.skills if s.level == "Advanced"]
        intermediate_skills = [self.escape_string(s.name) for s in self.resume.skills if s.level == "Intermediate"]
        basic_skills = [self.escape_string(s.name) for s in self.resume.skills if s.level == "Beginner"]
        skills = f"\\item{{\\textbf{{Advanced Skills}}{{: {','.join(advanced_skills)}}}\n}}"
        skills += f"\\item{{\\textbf{{Intermediate Skills}}{{: {','.join(intermediate_skills)}}}\n}}"
        skills += f"\\item{{\\textbf{{Beginner Skills}}{{: {','.join(basic_skills)}}}\n}}"
        return skills

    def fill_resume(self, output_resume, template):
        education = self.format_education()
        employment = self.format_employment()
        # data = dict(first_name='Tom', last_name='Casavant', email='tfcasavant@gmail.com', website='www.tomcasavant.com', phone_number='+1 (917) 888-8888')
        data = dict(name=self.resume.name, email=self.resume.email, website=self.resume.website,
                    phone_number=self.resume.phone.pretty_print(), education=education, employment=employment)
        # Add projects
        data = dict(data, projects=self.format_projects())
        data = dict(data, programming_skills=self.format_skills())
        output_resume.write(template.substitute(data))


if __name__ == '__main__':
    resume = Resume(json.load(open('data/resume_data.json'), cls=ResumeDecoder))
    resume.sort_employment_by_date()
    latex_resume = LaTeXResume(resume, 'templates/resume_template.tex')
    latex_resume.generate_resume()
