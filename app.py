
from playsound import playsound
from flask import Flask, Response, redirect, request, render_template, url_for
from googletrans import Translator
from gtts import gTTS
from langchain_community.llms import Ollama

from wtforms import Form, validators, StringField
import time


cached_llm = Ollama(model="llama3")

translator = Translator()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



timestr = time.strftime("%H%M%S")

class UploadText(Form):
    mytext = StringField(validators=[validators.InputRequired()])

@app.route('/', methods=('GET','POST'))
def index():
    form = UploadText(request.form)
    if request.method =='POST' and form.validate():
        print("Post /llm called")

        query = form.mytext.data

        response = cached_llm.invoke(query)

        speak = gTTS(response)

        speak.save("static/result.mp3" )

        string = timestr
        response_answer = {"answer": response}
        return redirect(url_for('result', var=string))
        



    form.mytext.data = ""
    return render_template('index.html', form=form)

    

@app.route('/result/<var>', methods=['GET', 'POST'])
def result(var):
    form = UploadText(request.form)
    if request.method =='POST' and form.validate():

        query = form.mytext.data

        response = cached_llm.invoke(query)

        speak = gTTS(response)

        speak.save("static/result.mp3" )


        response_answer = {"answer": response}
        return redirect(url_for('result', var=time.strftime("%H%M%S")))
        



    form.mytext.data = ""
    return render_template('index.html', form=form)


def start_app():
    app.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == "__main__":
    start_app()
