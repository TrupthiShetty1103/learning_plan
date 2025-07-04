from flask import Flask, request, jsonify
from services import plan_generator, assessment_generator, feedback_generator, state_tracker
from services import code_executor

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    data = request.json
    skill = data.get("skill")
    deadline = data.get("deadline")
    try:
        plan = plan_generator.generate_daywise_plan(skill, deadline)
        return jsonify({"plan": plan})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/init', methods=['POST'])
def init_plan():
    data = request.json
    skill = data.get("skill")
    deadline = data.get("deadline")
    user_id = "demo-user"
    plan = plan_generator.generate_daywise_plan(skill, deadline)
    state_tracker.init_user_state(user_id, plan)
    return jsonify({"user_id": user_id, "plan": plan})

@app.route('/api/module-quiz', methods=['GET'])
def get_module_quiz():
    topic = request.args.get("topic")
    try:
        questions = assessment_generator.generate_assessment(topic, 10)
        return jsonify({"questions": questions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/module-coding', methods=['GET'])
def get_module_coding():
    topic = request.args.get("topic")
    try:
        questions = assessment_generator.generate_coding_questions(topic, 2)
        return jsonify({"coding_questions": questions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/execute-code', methods=['POST'])
def execute_code():
    data = request.json
    code = data.get("code")
    test_input = data.get("test_input", "")
    res = code_executor.execute_user_code(code, test_input)
    return jsonify(res)

@app.route('/api/final-quiz', methods=['GET'])
def final_quiz():
    skill = request.args.get("skill")
    questions = assessment_generator.generate_assessment(skill, 20)
    return jsonify({"questions": questions})

@app.route('/api/final-feedback', methods=['POST'])
def final_feedback():
    data = request.json
    skill = data.get("skill")
    score = data.get("score")
    total = data.get("total")
    feedback, suggested_topics = feedback_generator.generate_feedback_only(skill, score, total)
    return jsonify({"feedback": feedback, "suggested_topics": suggested_topics})

@app.route('/api/request-plan-update', methods=['POST'])
def request_plan_update():
    data = request.json
    skill = data.get("skill")
    reason = data.get("reason")
    current_plan = data.get("current_plan", [])
    try:
        updated = plan_generator.generate_updated_plan(skill, reason, current_plan)
        return jsonify({"updated_plan": updated})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
