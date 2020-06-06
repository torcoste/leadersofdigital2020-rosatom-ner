#!/usr/bin/env python
# coding: utf8
"""
* Training: https://spacy.io/usage/training
* NER: https://spacy.io/usage/linguistic-features#named-entities
Compatible with: spaCy v2.1.0+
Last tested with: v2.2.4
"""
from __future__ import unicode_literals, print_function

import plac
import random
import warnings
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding


#          0        1           2            3             4            5      6               7         8
LABELS = ["ROLE", "CATEGORY", "EDUCATION", "EXPERIENCE", "MUST_KNOW", "DOC", "SUBORDINATION", "DUTIES", "RIGHTS", "GOAL", "ORG"]


TRAIN_DATA = [('Должностная инструкция копирайтера', {'entities': [(23, 34, 'ROLE')]}), ('Копирайтер относится к категории специалистов', {'entities': [(0, 10, 'ROLE'), (33, 45, 'CATEGORY')]}), ('На должность копирайтера назначается лицо, имеющее высшее профессиональное образование (журналистское, филологическое), опыт работы в рекламной сфере не менее 2-3 лет', {'entities': [(51, 118, 'EDUCATION'), (120, 166, 'EXPERIENCE')]}), ('3. Копирайтер должен знать:\u20283.1. Законодательство о рекламе, о защите прав потребителей, об авторском праве и смежных правах, об осуществлении предпринимательской деятельности.\u20283.2. Конъюнктуру рынка товаров, работ, услуг, в т.ч. рекламных услуг.\u20283.3. Теорию и практику рекламного маркетинга и менеджмента.\u20283.4. Принципы организации рекламной деятельности.\u20283.5. Общие и специальные требования к рекламе.\u20283.6. Способы, средства и носители рекламы.\u20283.7. Основы эстетики, этики, общей и специальной психологии, социологии, филологии.\u20283.8. Технику и основные инструменты составления рекламных текстов.\u20283.9. Основные принципы медиа-планирования.\u20283.10. Компьютер и рекламное программное обеспечение.\u20283.11. Основы трудового законодательства.\u20283.12. Правила и нормы охраны труда, техники безопасности, производственной санитарии и противопожарной защиты.', {'entities': [(33, 176, 'MUST_KNOW'), (182, 246, 'MUST_KNOW'), (252, 306, 'MUST_KNOW'), (312, 356, 'MUST_KNOW'), (362, 403, 'MUST_KNOW'), (409, 446, 'MUST_KNOW'), (452, 530, 'MUST_KNOW'), (536, 597, 'MUST_KNOW'), (603, 640, 'MUST_KNOW'), (647, 693, 'MUST_KNOW'), (700, 734, 'MUST_KNOW'), (741, 845, 'MUST_KNOW')]}), ('Основы трудового законодательства.', {'entities': [(7, 33, 'DOC')]}), ('Правила и нормы охраны труда, техники безопасности, производственной санитарии и противопожарной защиты.', {'entities': [(0, 28, 'DOC'), (30, 50, 'DOC'), (52, 78, 'DOC'), (81, 103, 'DOC')]}), ('Копирайтер подчиняется непосредственно креативному директору', {'entities': [(39, 60, 'SUBORDINATION')]}), ('II. Должностные обязанности \u2028\u2028Копирайтер:\u20281. В соответствии с медиа-планом создает слоганы (sloganeering), придумывает названия (naming), пишет сценарии для телевизионных роликов (scripting), сценарии для видео- и аудиорекламы, направленные на целевую аудиторию.\u20282. Разрабатывает контент (содержание) рекламы, рекламные тексты (в т.ч. на иностранном языке), пишет рекламные и PR-статьи.\u20283. Разрабатывает положительный имидж компании.\u20284. Обеспечивает информационное наполнение рекламы.\u20285. Организует презентацию слоганов, наименований, сценариев и статей руководству или представителям заказчиков.\u20286. Подготавливает новостные и пресс-релизы.\u20287. Создает «информационные поводы».\u20288. Подготавливает речь для публичных выступлений руководства компании на конференциях, пресс-клубах, телевидении, радио.\u20289. Осуществляет информационно-аналитическую и редакторскую работу.\u202810. Участвует в издании информационного бюллетеня.\u202811. Составляет отчеты о проделанной работе.', {'entities': [(45, 262, 'DUTIES'), (266, 386, 'DUTIES'), (390, 433, 'DUTIES'), (437, 484, 'DUTIES'), (488, 596, 'DUTIES'), (600, 640, 'DUTIES'), (644, 676, 'DUTIES'), (680, 796, 'DUTIES'), (801, 864, 'DUTIES'), (869, 915, 'DUTIES'), (920, 959, 'DUTIES')]}), ('III. Права \u2028\u2028Копирайтер имеет право:\u20281. На зачисление рекламных объявлений, текстов, пр. в свой личный портфолио как авторских разработок.\u20282. Требовать предоставления достоверной информации об объекте рекламы.\u20283. Требовать от руководства обеспечения организационно-технических условий, необходимых для исполнения должностных обязанностей.\u20284. Знакомиться с документами, определяющими его права и обязанности по занимаемой должности, критерии оценки качества исполнения должностных обязанностей.\u20285. Вносить на рассмотрение руководства предложения по совершенствованию работы, связанной с предусмотренными настоящей должностной инструкцией обязанностями.', {'entities': [(43, 138, 'RIGHTS'), (142, 209, 'RIGHTS'), (213, 338, 'RIGHTS'), (342, 493, 'RIGHTS'), (497, 651, 'RIGHTS')]}), ('IV. Ответственность \u2028\u2028Копирайтер привлекается к ответственности:\u20281. За ненадлежащее исполнение или неисполнение своих должностных обязанностей, предусмотренных настоящей должностной инструкцией, — в пределах, установленных действующим трудовым законодательством Российской Федерации.\u20282. За правонарушения, совершенные в процессе своей деятельности, — в пределах, установленных действующим административным, уголовным и гражданским законодательством Российской Федерации.\u20283. За причинение материального ущерба организации — в пределах, установленных законодательством РФ.', {'entities': []}), ('ДОЛЖНОСТНАЯ ИНСТРУКЦИЯ\u2028методиста - психолога', {'entities': [(23, 44, 'ROLE')]}), ('Методист психолог относится к категории специалистов', {'entities': [(0, 17, 'ROLE'), (40, 52, 'CATEGORY')]}), ('На должность методиста-психолога назначается лицо, имеющее высшее профессиональное образование и стаж педагогической работы от 5 лет и выше или стаж работы в должности методиста-психолога не менее 3 лет, или I квалификационную категорию', {'entities': [(59, 94, 'EDUCATION'), (97, 132, 'EXPERIENCE'), (144, 202, 'EXPERIENCE'), (208, 236, 'EXPERIENCE')]}), ('4.Методист – психолог должен знать:\u20284.1.Конституцию Российской Федерации.\u20284.2.Законы Российской Федерации, постановления и решения Правительства Российской Федерации и органов управления образованием по вопросам образования.\u20284.3.Требования государственных образовательных стандартов по педагогической психологии.\u20284.4.Основные приемы и методы работы по профилю специальности.\u20284.5.Педагогику, психологию, коррекционную педагогику и психологию, клиническую психологию. \u20284.6.Современные подходы в организации психологического сопровождения для обеспечения психического и психологического здоровья всех участников образовательного процесса.\u20284.7 Принципы и порядок разработки учебно-программной документации, учебных планов, образовательных программ и другой учебно-методической документации.\u20284.9.Постановления, распоряжения; инструкции, приказы по организации и функционированию психологической службе системы образования.\u20284.10.Основы трудового законодательства.', {'entities': [(40, 72, 'MUST_KNOW'), (78, 224, 'MUST_KNOW'), (229, 312, 'MUST_KNOW'), (317, 374, 'MUST_KNOW'), (379, 467, 'MUST_KNOW'), (471, 635, 'MUST_KNOW'), (640, 785, 'MUST_KNOW'), (791, 917, 'MUST_KNOW'), (923, 957, 'MUST_KNOW')]}), ('Методист-психолог непосредственно заведующему методическим отделом', {'entities': [(34, 66, 'SUBORDINATION')]}), ('II. Должностные обязанности.\u2028\u2028Методист-психолог:\u2028\u20281.Оказывает помощь педагогическим работникам в определении содержания, форм, методов и средств по обеспечению психологической адаптации учащихся и воспитанников ОУ.\u20282.Принимает участие в разработке методических и информационных материалов, диагностике, прогнозировании и планировании подготовки, переподготовки и повышения квалификации педагогов-психологов ОУ.\u20283.Организует методическую работу районных психологических центров. \u20284.Разрабатывает предложения по организации эффективности работы районных психологических центров.\u20285.Обобщает результаты деятельности районных психологических центров. \u20286.Анализирует и координирует деятельность районных психологических центров. \u20287.Обеспечивает взаимодействие районных психологических центров с другими структурами городской психологической службы.\u20288.Воспринимает и ретранслирует информацию по передовым направлениям педагогической психологии.\u20289.Информирует районные методические кабинеты и образовательные учреждения о современных тенденциях в практической психологии.\u202810.Оказывает помощь в планировании деятельности районных психологических центров.\u202811.Оказывает консультативную и практическую помощь сотрудникам районных психологических центров.\u202812.Организует и координирует работу методистов районных психологических центров.\u202813.Разрабатывает необходимую документацию по функционированию психологических центров районов.\u2028', {'entities': [(52, 214, 'DUTIES'), (217, 410, 'DUTIES'), (413, 478, 'DUTIES'), (481, 576, 'DUTIES'), (579, 646, 'DUTIES'), (649, 722, 'DUTIES'), (726, 842, 'DUTIES'), (845, 937, 'DUTIES'), (940, 1063, 'DUTIES'), (1067, 1145, 'DUTIES'), (1149, 1242, 'DUTIES'), (1246, 1323, 'DUTIES'), (1327, 1418, 'DUTIES')]}), ('III.Права.\u2028\u2028Методист-психолог имеет право:\u20281.Участвовать в обсуждении и решении вопросов деятельности Центра и отдела, а также кафедр и учебных подразделений.\u20282.Запрашивать от руководителей структурных подразделений и иных специалистов информацию и документы, необходимые для выполнения своих должностных обязанностей.\u20283.Бесплатно пользоваться услугами библиотеки, вычислительного центра, информационных фондов учебных и научных подразделений Центра. \u20284.Требовать от администрации Центра и заведующего отделом организационного и материально-технического обеспечения своей деятельности, а также оказания содействия в исполнении своих должностных обязанностей и прав.\u20285.Обжаловать приказы и распоряжения администрации Центра в установленном законодательством порядке.\u20286.Выносить на рассмотрение совета Центра вопросы, связанные с совершенствованием учебного процесса и повышением качества подготовки и переподготовки методистов-психологов.', {'entities': [(45, 158, 'RIGHTS'), (161, 318, 'RIGHTS'), (321, 450, 'RIGHTS'), (454, 666, 'RIGHTS'), (668, 765, 'RIGHTS'), (768, 937, 'RIGHTS')]}), ('IV. Ответственность.\u2028\u2028Методист-психолог несет ответственность:\u20281.За ненадлежащее исполнение или неисполнение своих должностных обязанностей, предусмотренных настоящей должностной инструкцией, - в пределах, определенных действующим трудовым законодательством Российской Федерации.\u20282.За правонарушения, совершенные в процессе осуществления своей деятельности, - в пределах, определенных действующим административным, уголовным и гражданским законодательством Российской Федерации.\u20283.За причинение материального ущерба – в пределах, определенных действующим трудовым и гражданским законодательством Российской Федерации.', {'entities': []}), ('Должностная инструкция техника-лаборанта', {'entities': [(23, 40, 'ROLE')]}), ('Должностные обязанности. \u2028Выполняет под руководством более квалифицированного специалиста анализы и испытания по определению химического состава и основных свойств материалов в соответствии с требованиями стандартов и технических условий. Принимает технологические пробы и образцы для проведения анализов и испытаний. Оформляет результаты анализов и испытаний, ведет их учет, составляет техническую документацию по выполняемым лабораторией работам. Своевременно извещает соответствующие подразделения предприятия о результатах анализов и испытаний. Осуществляет вспомогательные и подготовительные операции по проведению особо сложных лабораторных работ. Принимает участие в разработке новых методов химических анализов, механических испытаний, отбора технологических проб, металлографических исследований. Следит за исправным состоянием установок, приборов, инструмента и другого лабораторного оборудования, выполняет простую регулировку его и вносит необходимые исправления в техническую документацию в соответствии с полученными результатами анализов и испытаний. ', {'entities': [(26, 238, 'DUTIES'), (239, 317, 'DUTIES'), (318, 449, 'DUTIES'), (449, 548, 'DUTIES'), (549, 653, 'DUTIES'), (654, 805, 'DUTIES'), (806, 1066, 'DUTIES')]}), ('Должен знать: \u2028документы, стандарты, положения, инструкции и другие руководящие материалы по проведению лабораторных анализов и испытаний; основные технологические процессы и режимы производства; оборудование лаборатории и правила его эксплуатации; правила оформления технической документации на проведенные лабораторные анализы и испытания; основы трудового законодательства; основы экономики, научной организации труда, организации производства; правила внутреннего трудового распорядка; правила и нормы охраны труда, техники безопасности, производственной санитарии и противопожарной защиты. ', {'entities': [(15, 137, 'MUST_KNOW'), (139, 194, 'MUST_KNOW'), (196, 247, 'MUST_KNOW'), (249, 340, 'MUST_KNOW'), (342, 375, 'MUST_KNOW'), (377, 446, 'MUST_KNOW'), (448, 593, 'MUST_KNOW')]}), ('Требования к квалификации. \nТехник-лаборант I категории: среднее специальное (техническое) образование и стаж работы в должности техника-лаборанта II категории не менее 2 лет. \nТехник-лаборант II категории: среднее специальное (техническое) образование и стаж работы в должности техника или других должностях, замещаемых специалистами со средним специальным образованием, не менее 2 лет. \nТехник-лаборант: среднее специальное (техническое) образование без предъявления требований к стажу работы.', {'entities': [(28, 174, 'EDUCATION'), (177, 386, 'EDUCATION'), (389, 494, 'EDUCATION')]})]







@plac.annotations(
    model=("Model name. Defaults to blank 'ru' model.", "option", "m", str),
    new_model_name=("New model name for model meta.", "option", "nm", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)
def main(model=None, new_model_name="rosatom-docs", output_dir='./model', n_iter=150):
    """Set up the pipeline and entity recognizer, and train the new entity."""
    random.seed(0)
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("ru")  # create blank Language class
        print("Created blank 'ru' model")
    # Add entity recognizer to model if it's not in the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner)
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe("ner")

    for label in LABELS:
        ner.add_label(label)  # add new entity label to entity recognizer

    if model is None:
        optimizer = nlp.begin_training()
    else:
        optimizer = nlp.resume_training()
    move_names = list(ner.move_names)
    # get names of other pipes to disable them during training
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    # only train NER
    with nlp.disable_pipes(*other_pipes) and warnings.catch_warnings():
        # show warnings for misaligned entity spans once
        warnings.filterwarnings("once", category=UserWarning, module='spacy')

        sizes = compounding(1.0, 4.0, 1.001)
        # batch up the examples using spaCy's minibatch
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            batches = minibatch(TRAIN_DATA, size=sizes)
            losses = {}
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
            print("Losses", losses)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.meta["name"] = new_model_name  # rename model
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)


if __name__ == "__main__":
    plac.call(main)