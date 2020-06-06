#!/usr/bin/env python
# coding: utf8
from __future__ import unicode_literals, print_function

import plac
import spacy

TEST_TEXT = """
    Должностная инструкция методиста-психолога 
Утверждаю: Директор МОУ повышения квалификации Центра развития образования    ДОЛЖНОСТНАЯ ИНСТРУКЦИЯ методиста - психолога   I.Общие положения  1.Методист психолог относится к категории специалистов. 2.На должность методиста-психолога назначается лицо, имеющее высшее профессиональное образование и стаж педагогической работы от 5 лет и выше или стаж работы в должности методиста-психолога не менее 3 лет, или I квалификационную категорию. 3.Назначение на должность методиста-психолога и освобождение от должности производится приказом директора Центра. 4.Методист – психолог должен знать: 4.1.Конституцию Российской Федерации. 4.2.Законы Российской Федерации, постановления и решения Правительства Российской Федерации и органов управления образованием по вопросам образования. 4.3.Требования государственных образовательных стандартов по педагогической психологии. 4.4.Основные приемы и методы работы по профилю специальности. 4.5.Педагогику, психологию, коррекционную педагогику и психологию, клиническую психологию.  4.6.Современные подходы в организации психологического сопровождения для обеспечения психического и психологического здоровья всех участников образовательного процесса. 4.7 Принципы и порядок разработки учебно-программной документации, учебных планов, образовательных программ и другой учебно-методической документации. 4.9.Постановления, распоряжения; инструкции, приказы по организации и функционированию психологической службе системы образования. 4.10.Основы трудового законодательства. 5.Методист-психолог непосредственно заведующему методическим отделом.   II. Должностные обязанности.  Методист-психолог:  1.Оказывает помощь педагогическим работникам в определении содержания, форм, методов и средств по обеспечению психологической адаптации учащихся и воспитанников ОУ. 2.Принимает участие в разработке методических и информационных материалов, диагностике, прогнозировании и планировании подготовки, переподготовки и повышения квалификации педагогов-психологов ОУ. 3.Организует методическую работу районных психологических центров.  4.Разрабатывает предложения по организации эффективности работы районных психологических центров. 5.Обобщает результаты деятельности районных психологических центров.  6.Анализирует и координирует деятельность районных психологических центров.  7.Обеспечивает взаимодействие районных психологических центров с другими структурами городской психологической службы. 8.Воспринимает и ретранслирует информацию по передовым направлениям педагогической психологии. 9.Информирует районные методические кабинеты и образовательные учреждения о современных тенденциях в практической психологии. 10.Оказывает помощь в планировании деятельности районных психологических центров. 11.Оказывает консультативную и практическую помощь сотрудникам районных психологических центров. 12.Организует и координирует работу методистов районных психологических центров. 13.Разрабатывает необходимую документацию по функционированию психологических центров районов.     III.Права.  Методист-психолог имеет право: 1.Участвовать в обсуждении и решении вопросов деятельности Центра и отдела, а также кафедр и учебных подразделений. 2.Запрашивать от руководителей структурных подразделений и иных специалистов информацию и документы, необходимые для выполнения своих должностных обязанностей. 3.Бесплатно пользоваться услугами библиотеки, вычислительного центра, информационных фондов учебных и научных подразделений Центра.  4.Требовать от администрации Центра и заведующего отделом организационного и материально-технического обеспечения своей деятельности, а также оказания содействия в исполнении своих должностных обязанностей и прав. 5.Обжаловать приказы и распоряжения администрации Центра в установленном законодательством порядке. 6.Выносить на рассмотрение совета Центра вопросы, связанные с совершенствованием учебного процесса и повышением качества подготовки и переподготовки методистов-психологов.  IV. Ответственность.  Методист-психолог несет ответственность: 1.За ненадлежащее исполнение или неисполнение своих должностных обязанностей, предусмотренных настоящей должностной инструкцией, - в пределах, определенных действующим трудовым законодательством Российской Федерации. 2.За правонарушения, совершенные в процессе осуществления своей деятельности, - в пределах, определенных действующим административным, уголовным и гражданским законодательством Российской Федерации. 3.За причинение материального ущерба – в пределах, определенных действующим трудовым и гражданским законодательством Российской Федерации.   С должностными обязанностями ознакомлена и принимаю их к исполнению.  ___________________ ____________ (подпись) (инициалы, фамилия)  «_____» _____________ 200.. г.
    """

def main(model='./model', text=TEST_TEXT):
    nlp = spacy.load(model)  # load existing spaCy model
    print("Loaded model '%s'" % model)
    
    # test the trained model
    doc = nlp(text)

    result = []
    for ent in doc.ents:
        print(ent.label_, ent.text)
        result.append(dict(label=ent.label_, text=ent.text))

    return result


if __name__ == "__main__":
    plac.call(main)