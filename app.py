from flask import Flask, request, render_template
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import requests

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_page():
    return render_template("index.html")


@app.route('/review', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            search_string = request.form['content'].replace(" ", "")
            flipkart_url = "https://www.flipkart.com/search?q=" + search_string
            uClient = uReq(flipkart_url)
            flipkart_page = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkart_page, "html.parser")
            bigboxes = flipkart_html.find_all("div", {"class": "_1AtVbE col-12-12"})
            del bigboxes[0:3]

            reviews = []
            for i in range(1,5):
                product_name = bigboxes[i].find_all("div", {"class": "_4rR01T"})[0].text
                productLink = "https://www.flipkart.com" + bigboxes[i].div.div.div.a['href']
                prodRes = requests.get(productLink)
                prodRes.encoding = 'utf-8'
                prod_html = bs(prodRes.text, "html.parser")

                comment_boxes = prod_html.find_all("div", {'class': "_16PBlm"})


                for commentbox in comment_boxes:
                    try:
                        name = commentbox.div.div.find_all("p", {"class": "_2sc7ZR _2V5EHH"})[0].text
                        rating = commentbox.div.div.div.div.text
                        comment_header = commentbox.div.div.div.p.text
                        comtag = commentbox.div.div.find_all('div', {'class': ''})
                        comment = comtag[0].div.text
                    except:
                        name = "No Name"
                        rating = "No Rating"
                        comment_header = "No Header"
                        comment = "No Review"
                    try:
                        my_dict = {"Product": product_name,
                                "Name": name,
                                "Rating": rating,
                                "Comment Header": comment_header,
                                "Review": comment}
                        reviews.append(my_dict)
                    except Exception as e:
                        print(e)

            return render_template('results.html', reviews=reviews[0:(len(reviews) - 1)])
        except Exception as e:
            print("error! : ", e)
            return 'something is wrong'
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
