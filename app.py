from flask import Flask, render_template, request
from flask_cors import cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

#create a flask app
# initialising the flask app with the name 'app'
app = Flask(__name__)

#create a route to access the function
#Base URL
@app.route('/', methods = ['GET'])
#cross_origin-It requires only for cloud deployment and not for local deployment
@cross_origin()
def homepage():
    return render_template("index.html")

#This route is responsible to show the reviews of the product
@app.route('/review',methods=['POST','GET'])
@cross_origin()
def index():
    # if it is a POST request then we can execute further
    if request.method == 'POST':
        try:
            """
            #Step1
            #here "form" is the tag which is available inside in our index.html
            #here "content" is whatever i'am giving inside the text box that is my content
            """
            searchString = request.form['content'].replace(" ", "")
            """
            #Step2
            #here the "searchstring" is the input we are getting from the form."""
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            """
            #Step3
            #Search the url and read the content
            #Ureq - Alias for urlopen and its responsible for to open any url
            #Ureq is the part of the package called urllib
            #here uClient variable gives some response - which simply means it open the url and initiate the search operation"""
            uClient = uReq(flipkart_url)
            """
            Step4
            # open the link and do the read operation and then i'vl get the entire html page of the website or search page
            """
            flipkartPage = uClient.read()
            """ Step5
            Close the connection"""
            uClient.close()
            """
            #Step6
            #Beautifulsoup - It tries to remove the unnecessary text or information and it create some date in the form of structured format
            #Not fully structured format, somehow structured format
            #bs4 will works fine for html parser, xml parser"""
            flipkart_html = bs(flipkartPage, "html.parser")
            """
            #Step7
            #Try to filter out the class that containing the review so we need to click the url of each and every product that listed out on the page
            #inside the div -- > class --> we  have the link(href)"""
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            """
            Step7
            #Delete some of the unwanted div classes which are not helpful for us.
            """
            del bigboxes[0:3]
            """
            Step8
            #inside the multiple div's we have the href link to open and exteact the reviews of the product
            #Append the extracted url with my base url
            """
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            """
            Step9
            #once i reached the product link now i want to extract the review of the particular product 
            """
            prodRes = requests.get(productLink)
            prodRes.encoding = 'utf-8'
            """
            Step10
            #we are using the beautiful soap for beautification
            """
            prod_html = bs(prodRes.text, "html.parser")
            print(prod_html)
            """
            Step11
            Extract the reviews from the comment boxes inside the div and class
            """
            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})
            """
            Step12
            #Open a new file and we are supposed to write or store the reviews inside the file
            """
            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
            reviews = []
            for commentbox in commentboxes:
                try:
                    # name.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text

                except:
                    name = 'No Name'

                try:
                    # rating.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text


                except:
                    rating = 'No Rating'

                try:
                    # commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    # custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ", e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                reviews.append(mydict)
            return render_template('results.html', reviews=reviews[0:(len(reviews) - 1)])
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')


if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=8001, debug=True)
    app.run(debug=True)


