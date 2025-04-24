
# from flask import Flask, render_template, request
# from tavily import TavilyClient
# from dotenv import load_dotenv
# import os

# load_dotenv()
# app = Flask(__name__)

# tavili_api_key = os.getenv("TAVILI_API_KEY")
# client = TavilyClient(tavili_api_key)

# @app.route("/", methods=["GET", "POST"])
# def chat():
#     chat_history = []

#     if request.method == "POST":
#         user_input = request.form["question"]

#         system_prompt = f"""
#         You are an assistant specialising in content from publicfinance.lk. If user greets, you can greet.
#         If the question is not about public finance or economics, reply “I'm here to answer only publicfinance.lk related questions 🙂”. 
#         Otherwise, make use of the latest year data in the website and answer in British English. Question: {user_input}
#         """

#         response = client.search(
#             query=system_prompt,
#             search_depth="advanced",
#             include_answer="advanced",
#             include_images=True,
#             include_image_descriptions=True,
#             include_raw_content=True,
#             include_domains=["https://publicfinance.lk/en"]
#         )

#         answer = response.get("answer", "")
#         urls = [res["url"] for res in response.get("results", [])][:3]

#         chat_history.append({
#             "question": user_input,
#             "answer": answer,
#             "urls": urls
#         })

#     return render_template("chat.html", chat_history=chat_history)

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

tavili_api_key = os.getenv("TAVILI_API_KEY")
client = TavilyClient(tavili_api_key)

@app.route("/")
def home():
    return render_template("chat.html", chat_history=[])

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data["question"]

    system_prompt = f"""
    You are an assistant specialising in content from publicfinance.lk. If user greets, you can greet.
    If the question is not about public finance or economics, reply “I'm here to answer only publicfinance.lk related questions 🙂”. 
    Otherwise, make use of the latest year data in the website and answer in British English. Question: {user_input}
    """

    response = client.search(
        query=system_prompt,
        search_depth="advanced",
        include_answer="advanced",
        include_images=True,
        include_image_descriptions=True,
        include_raw_content=True,
        include_domains=["https://publicfinance.lk/en"]
    )

    answer = response.get("answer", "")
    urls = [res["url"] for res in response.get("results", [])][:3]

    return jsonify({"answer": answer, "urls": urls})

if __name__ == "__main__":
    app.run(debug=True)
