from flask import Flask, request, jsonify
from services import plan_generator
from services import assessment_generator  # if not already imported
from services import state_tracker
from services import feedback_generator

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
    

@app.route('/api/module-quiz', methods=['GET'])
def get_module_quiz():
    topic = request.args.get("topic", "Introduction to Python")
    try:
        questions = assessment_generator.generate_assessment(topic, 10)
        return jsonify({"questions": questions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/init', methods=['POST'])
def init_plan():
    data = request.json
    skill = data.get("skill")
    deadline = data.get("deadline")
    user_id = "demo-user"  # for now — single user
    plan = plan_generator.generate_daywise_plan(skill, deadline)
    state_tracker.init_user_state(user_id, plan)
    return jsonify({"user_id": user_id, "plan": plan})



@app.route('/api/submit-score', methods=['POST'])
def submit_score():
    data = request.json
    user_id = "demo-user"
    module_index = data.get("module")
    score = data.get("score")
    total = data.get("total")

    state_tracker.update_module_score(user_id, module_index, score, total)
    return jsonify({"status": "updated"})



@app.route('/api/final-quiz', methods=['GET'])
def final_quiz():
    skill = request.args.get("skill", "Python")
    questions = assessment_generator.generate_assessment(skill, 20)
    return jsonify({"questions": questions})
@app.route('/api/final-feedback', methods=['POST'])
def final_feedback():
    data = request.json
    skill = data.get("skill")
    score = data.get("score")
    total = data.get("total")

    # Call the revised generator that returns just feedback and topics
    feedback, suggested_topics = feedback_generator.generate_feedback_only(skill, score, total)

    return jsonify({
        "feedback": feedback,
        "suggested_topics": suggested_topics
    })

@app.route('/api/request-plan-update', methods=['POST'])
def request_plan_update():
    from services.plan_generator import generate_updated_plan  # create this
    data = request.json
    skill = data.get("skill")
    reason = data.get("reason")
    current_plan = data.get("current_plan", [])

    try:
        updated = generate_updated_plan(skill, reason, current_plan)
        return jsonify({ "updated_plan": updated })
    except Exception as e:
        return jsonify({ "error": str(e) }), 500

if __name__ == '__main__':
    app.run(debug=True)
