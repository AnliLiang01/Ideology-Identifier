# app.py：Flask 后端服务
#更新python为3.9以上：brew install python@3.11
# 安装依赖（如果未安装）：pip install flask transformers beautifulsoup4 requests

from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# 初始化模型（适配中文）
classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli")

LABELS = ["女权倾向", "男权倾向", "厌女倾向", "左倾表达", "右倾表达", "情绪稳定性"]
KEYWORDS = {
    "女权倾向": ["平权", "独立", "打拳", "女权", "自主"],
    "男权倾向": ["传统家庭", "男主外", "领导力", "阳刚"],
    "厌女倾向": ["拜金", "天生劣等", "情绪化", "绿茶"],
    "左倾表达": ["人民", "反资本", "公有", "集体主义"],
    "右倾表达": ["自由市场", "反税", "精英", "个体"],
    "情绪稳定性": ["冷静", "理性", "暴躁", "骂人"]
}
MAX_TEXT_LENGTH = 2000


def extract_text_from_url(url):
    if any(x in url for x in ["weibo.com/u", "xiaohongshu.com"]):
        return "[不支持该类网页链接：微博主页、小红书等]"
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return f"[网页访问失败，状态码：{resp.status_code}]"
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, "html.parser")
        texts = soup.find_all("p")
        combined = " ".join([p.get_text().strip() for p in texts if len(p.get_text().strip()) > 10])
        return combined[:MAX_TEXT_LENGTH] if combined else "[网页内容为空或结构不支持]"
    except Exception as e:
        return f"[网页抓取失败：{str(e)}]"


def analyze_text(text):
    if len(text) > MAX_TEXT_LENGTH:
        return {"error": "输入文本超出长度限制（2000 字符），请缩短后重试。"}
    if text.startswith("[") and text.endswith("]"):
        return {"error": text}

    result = classifier(text, LABELS, multi_label=True)
    response = {}
    for label, score in zip(result['labels'], result['scores']):
        keywords_found = [kw for kw in KEYWORDS.get(label, []) if kw in text]
        response[label] = {
            "score": round(score * 100, 2),
            "keywords": keywords_found
        }
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    input_text = data.get("text", "").strip()
    if input_text.startswith("http"):
        text = extract_text_from_url(input_text)
    else:
        text = input_text
    result = analyze_text(text)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
