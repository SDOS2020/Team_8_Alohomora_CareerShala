import json


def load_option_from_json(option_json, from_question, class_dict: dict):
    optionClass = class_dict['Option']
    option = optionClass.objects.create(body=option_json["body"], question=from_question)
    option.save()
    if option_json["continuation_questionnaire"] is not None:
        questionnaire_json = option_json["continuation_questionnaire"]
        load_questionnaire_from_json(questionnaire_json, option, class_dict)


def load_question_from_json(question_json, from_questionnaire, class_dict: dict):
    questionClass = class_dict['Question']
    question = questionClass.objects.create(body=question_json["body"], multiselect=question_json["multiselect"],
                                            questionnaire=from_questionnaire)
    question.save()
    for option_json in question_json["option"]:
        load_option_from_json(option_json, question, class_dict)


def load_questionnaire_from_json(questionnaire_json, from_option, class_dict: dict):
    questionnaireClass = class_dict['Questionnaire']
    questionnaire = questionnaireClass.objects.create(name=questionnaire_json["name"], root=questionnaire_json["root"])
    if from_option is not None:
        from_option.continuation_questionnaire = questionnaire
        from_option.save()
    for question_json in questionnaire_json["question"]:
        load_question_from_json(question_json, questionnaire, class_dict)


def generate_questionnaire(apps, schema_editor):
    questionnaireClass = apps.get_model('questionnaire', 'Questionnaire')
    questionClass = apps.get_model('questionnaire', 'Question')
    optionClass = apps.get_model('questionnaire', 'Option')
    class_dict = {
        'Questionnaire': questionnaireClass,
        'Question': questionClass,
        'Option': optionClass
    }
    questionnaires_json_file_name = 'questionnaires.json'
    with open(questionnaires_json_file_name, encoding='utf-8') as f:
        root_questionnaire_json = json.load(f)
        load_questionnaire_from_json(root_questionnaire_json, None, class_dict)