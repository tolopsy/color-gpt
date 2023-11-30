import json
from dotenv import dotenv_values
from flask import Flask, request, jsonify, render_template
import openai

config = dotenv_values(".env")

app = Flask(
    __name__,
    template_folder="templates",
    static_url_path="",
    static_folder="static"
)
openai.api_key = config["OPENAI_API_KEY"]

def get_colors(msg: str):
    prompt = f"""
    You are a color palette generating assistant that responds to text prompts for color palettes.
    Generate color palettes that fit theme, mood or instructions in the prompt.
    Desired Format: array of hexadecimal color codes representing the color palettes. Array should contain atleast one color code. Maximum of 8.
    For Example: ["#FFFFFF", "#F7CAC8"]

    Convert the following verbal description of a color palette into a list of colors: {msg}
    """
    response = openai.chat.completions.create(model="gpt-3.5-turbo-1106", messages=[{"role": "user", "content": prompt}])
    colors = json.loads(response.choices[0].message.content)
    return colors

    

@app.route("/colors", methods=["POST"])
def colors():
    data = request.get_json()
    query = data["query"]
    if not query:
        return jsonify(message="No query provided"), 400
    
    try:
        colors = get_colors(query)
    except Exception as e:
        return jsonify(message=f"Something went wrong during ai generation: {e}"), 500
    
    return {"colors": colors}



@app.route("/")
def index():
    return render_template("index.html")
