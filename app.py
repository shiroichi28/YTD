from flask import Flask, redirect,request,render_template,session,url_for,send_file
from pytube import YouTube
from io import BytesIO

app=Flask(__name__)
app.secret_key = "super secret key"

@app.route("/", methods=["GET","POST"])
def home():
    if request.method=="POST":
        session['link']=request.form.get('link')
        try:
            url=YouTube(session['link'])
            url.check_availability()
        except:
            return render_template('error.html')
        return render_template('download.html',url=url)
            

    return render_template('home.html')
@app.route("/download", methods=["GET","POST"])
def download_video():
        if request.method=="POST":
             buffer=BytesIO()
             url=YouTube(session['link'])
             list=request.form.get('list')
             video=url.streams.get_by_itag(list)
             video.stream_to_buffer(buffer)
             buffer.seek(0)
             return send_file(buffer, as_attachment=True,download_name="video.mp4",mimetype="video/mp4")
        return redirect(url_for('home'))

if __name__=='__main__':
     app.run(debug=True)
