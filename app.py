import os
from flask import Flask,request, jsonify

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        goals = dict(title="Цели", content=["обеспечение конкурентных преимуществ [org]Общества[/org] за счет создания эффективной кадровой политики, позволяющей формировать команду высококвалифицированных специалистов, развивать и мотивировать персонал к рациональному и эффективному труду"])
        tasks = dict(title="Задачи", content=["Разработка и внедрение кадровой политики предприятия", "Подбор, адаптация, расстановка, закрепление персонала", "Повышение профессионального уровня сотрудников", "Мотивация персонала", "Обеспечение эффективного использования персонала", "Постановка и контроль системы учета движения персонала", "Обеспечение здоровых и безопасных условий труда", "Обеспечение соблюдения норм трудового законодательства"])
        edu_req = dict(title="Требования к образованию", content=["Высшее образование (экономическое, инженерно – экономическое, психологическое)", "стаж работы на руководящих должностях не менее 2 лет"])
        skills = dict(title="Требования к квалификации", content=["Аналитические, организационные и коммуникативные навыки.", "Владение программным пакетом 1С – «Зарплата и кадры», MS Office на уровне уверенного пользователя", "Опыт организации корпоративных мероприятий, владение методиками социологических и социально –психологических методик  диагностики персонала"])
        mustknow = dict(title="Должен знать", content=["[doc]Руководящие и нормативные документы, касающиеся работы предприятий торговли[/doc]", "[doc]Законодательные и нормативные правовые акты[/doc], [doc]методические материалы[/doc], касающиеся вопросов труда и социального развития", "[doc]Трудовое законодательство[/doc]", "Экономику, социологию и психологию труда"])
        personal_quals = dict(title="Класс", content="Руководитель.")

        data = dict(
            role="Начальник отдела по управлению персоналом"
            category="Руководитель"
            content=[goals, tasks, edu_req, skills, mustknow, personal_quals]
            )
        response = jsonify(data)
        response.status_code = 200
        return response # Returns the HTTP response
    else:
        return "Send a POST-request with data"

if __name__ == '__main__':
    app.run()